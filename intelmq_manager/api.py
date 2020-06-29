"""HTTP-API backend of IntelMQ-Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>

This module implements the HTTP part of the API backend of
IntelMQ-Manager. The logic itself is in the runctl, files and pages
modules.
"""

import string
import typing

import hug  # type: ignore
from hug.middleware import SessionMiddleware  # type: ignore

import intelmq_manager.runctl as runctl
import intelmq_manager.files as files
import intelmq_manager.pages as pages
import intelmq_manager.config
import intelmq_manager.session as session


Levels = hug.types.OneOf(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL",
                          "ALL"])
Actions = hug.types.OneOf(["start", "stop", "restart", "reload", "status"])
Groups = hug.types.OneOf(["collectors", "parsers", "experts", "outputs",
                          "botnet"])
BotCmds = hug.types.OneOf(["get", "pop", "send", "process"])
Bool = hug.types.Mapping({"true": True, "false": False})
Pages = hug.types.OneOf(["configs", "management", "monitor", "check", "about",
                         "index"])


ID_CHARS = set(string.ascii_letters + string.digits + "-")
@hug.type(extend=hug.types.Text)
def ID(value):
    if not set(value) < ID_CHARS:
        raise ValueError("Invalid character in {!r}".format(value))
    return value


api_config: intelmq_manager.config.Config = intelmq_manager.config.Config()

runner: runctl.RunIntelMQCtl = runctl.RunIntelMQCtl(api_config.intelmq_ctl_cmd)

file_access: files.FileAccess = files.FileAccess(api_config)

# Add session middleware with a dummy store so that we can later
# initialize it properly in initialize_api. When initialize_api is
# called from a function registered with the hug.startup decorator it's
# too late to add new middleware, so we need to add it now and modify it
# in place later.
session_middleware = SessionMiddleware(session.NoOpStore())
hug.API(__name__).http.add_middleware(session_middleware)


def initialize_api(filename: typing.Optional[str] = None) -> None:
    """Initialize the API, optionally loading a configuration file.

    If a filename is given, this function updates the configuration in
    the module global variable api_config by loading a new configuration
    and assigning it to the variable.

    Then, regardless of whether a filename was given, it calls the
    update_from_runctl method of the file_access object so that it uses
    the files that IntelMQ actually uses.

    Note: Because of that last step this function should always be
    called when the server process starts even when no configuration
    needs to be read from a file.
    """
    global api_config, runner
    if filename is not None:
        api_config = intelmq_manager.config.load_config(filename)
    runner = runctl.RunIntelMQCtl(api_config.intelmq_ctl_cmd)
    file_access.update_from_runctl(runner.get_paths())

    session_file = api_config.session_store
    if session_file is not None:
        session_middleware.store = session.SessionStore(str(session_file))
        session_middleware.cookie_http_only = api_config.session_cookie_http_only
        session_middleware.cookie_secure = api_config.session_cookie_secure


def cache_get(*args, **kw):
    """Route to use instead of hug.get that sets cache headers in the response.
    """
    return hug.get(*args, **kw).cache(max_age=3)


@hug.exception(runctl.IntelMQCtlError)
def crlerror_handler(response, exception):
    response.status = hug.HTTP_500
    return exception.error_dict


@hug.get("/api/botnet")
@typing.no_type_check
def botnet(action: Actions, group: Groups = None):
    return runner.botnet(action, group)


@hug.get("/api/bot")
@typing.no_type_check
def bot(action: Actions, id: ID):
    return runner.bot(action, id)


@cache_get("/api/getlog")
@typing.no_type_check
def getlog(id: ID, lines: int, level: Levels = "DEBUG"):
    return runner.log(id, lines, level)


@cache_get("/api/queues")
def queues():
    return runner.list("queues")


@cache_get("/api/queues-and-status")
def queues_and_status():
    return runner.list("queues-and-status")


@hug.get("/api/version")
def version():
    return runner.version()


@hug.get("/api/check")
def check():
    return runner.check()


@hug.get("/api/clear")
@typing.no_type_check
def clear(id: ID):
    return runner.clear(id)


@hug.post("/api/run")
@typing.no_type_check
def run(bot: str, cmd: BotCmds, show: Bool = False, dry: Bool = False,
        msg: str = ""):
    return runner.run(bot, cmd, show, dry, msg)


@hug.get("/api/debug")
def debug():
    return runner.debug()


@hug.get("/api/config")
def config(response, file: str, fetch: bool=False):
    result = file_access.load_file_or_directory(file, fetch)
    if result is None:
        return ["Unknown resource"]

    content_type, contents = result
    response.content_type = content_type
    return contents


@hug.post("/api/save", parse_body=True,
          inputs={"application/x-www-form-urlencoded": hug.input_format.text})
def save(body, file: str):
    try:
        file_access.save_file(file, body)
        return "success"
    except files.SaveFileException as e:
        return str(e)


@hug.get("/", output=hug.output_format.html)
@typing.no_type_check
def page(response, page: Pages = "index"):
    return pages.render_page(page, api_config)

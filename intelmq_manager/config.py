"""Configuration for IntelMQ Manager

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

from typing import List, Optional
import json
from pathlib import Path


class Config:

    """Configuration settings for IntelMQ Manager"""

    intelmq_ctl_cmd: List[str] = ["sudo", "-u", "intelmq",
                                  "/usr/local/bin/intelmqctl"]

    allowed_path: Path = Path("/opt/intelmq/var/lib/bots/")

    session_store: Optional[Path] = None
    session_cookie_http_only: bool = True
    session_cookie_secure: bool = True


def load_config(filename: str) -> Config:
    """Load configuration from JSON file"""
    with open(filename) as f:
        raw = json.load(f)

    config = Config()

    if "intelmq_ctl_cmd" in raw:
        config.intelmq_ctl_cmd = raw["intelmq_ctl_cmd"]

    if "allowed_path" in raw:
        config.allowed_path = Path(raw["allowed_path"])

    if "session_store" in raw:
        config.session_store = Path(raw["session_store"])

    config.session_cookie_http_only = raw.get("session_cookie_http_only",
                                              config.session_cookie_http_only)
    config.session_cookie_secure = raw.get("session_cookie_secure",
                                           config.session_cookie_secure)

    return config

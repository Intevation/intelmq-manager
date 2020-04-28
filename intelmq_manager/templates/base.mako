<%!
    import collections

    Page = collections.namedtuple("Page", ["name", "title", "icon", "libraries"])
    pages = [Page("configs", "Configuration", "config.png",
                  ["plugins/vis.js/vis.js",
                   "js/runtime.js",
                   "js/pipeline.js",
                   "js/positions.js",
                   "js/defaults.js",
                   "js/network-configuration.js",
                   "js/configs.js",
                   ]),
             Page("management", "Management", "botnet.png",
                  ["js/runtime.js", "js/management.js"]),
             Page("monitor", "Monitor", "monitor.png",
                  ["js/runtime.js",
                   "js/pipeline.js",
                   "js/defaults.js",
                   "js/monitor.js"]),
             Page("check", "Check", "check.png", ["js/check.js"]),
             Page("about", "About", "about.png", ["js/about.js"])]

    common_libraries =  [
        "js/static.js",
        "js/sb-admin-2.js",
        ## XX this don't have to be on every page:
        "plugins/dataTables/jquery.dataTables.js",
        "plugins/dataTables/dataTables.bootstrap.js",
        ]

    page_map = {page.name: page for page in pages}
    page_map["index"] = Page("index", "", "", [])
%>

<!DOCTYPE html>
<html lang="en">

    <head>

        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="">
        <meta name="author" content="">

        <title>IntelMQ Manager</title>

        <!-- Bootstrap Core CSS -->
        <link href="plugins/bootstrap/bootstrap.min.css" rel="stylesheet">

        <!-- MetisMenu CSS -->
        <link href="plugins/metisMenu/metisMenu.min.css" rel="stylesheet">

        <!-- Vis.JS Plugin JavaScript (configs.html)-->
        <link href="plugins/vis.js/vis.css" rel="stylesheet" type="text/css">

        <!-- DataTables CSS (other files than configs.html) -->
        <link href="plugins/dataTables/dataTables.bootstrap.css" rel="stylesheet">

        <!-- Custom Fonts -->
        <link href="plugins/font-awesome-4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">

        <!-- Custom CSS -->
        <link href="css/sb-admin-2.css" rel="stylesheet">
        <link href="css/style.css" rel="stylesheet">

        <link rel="icon" type="image/png" href="images/logo2.png">

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
            <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->

    </head>

    <body>
        <div id="wrapper">

            <!-- Navigation -->
            <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
                <div class="navbar-header">
                    <a class="navbar-brand" href="page?page=index"><img height="24px"  style="margin-right:10px" src="./images/logo2.png"><img height="20px" src="./images/logo_no_margin_6.png"/></a>
                </div>
                <!-- /.navbar-header -->

                <ul class="nav navbar-top-links navbar-left">
                    % for page in pages:
                    <li class="${'active' if pagename == page.name else ''}">
                        <a href="?page=${page.name}">
                            <span class="top-menu-text"><img src="./images/${page.icon}" width="24px" height="24px">&nbsp;${page.title}</span>
                        </a>
                    </li>
                    % endfor
                </ul>
                <!-- /.navbar-top-links -->
                <div title="Click to expand, then escape to minimize again." id='log-window'>
                    <i role="close" class="fa fa-times"></i>
                    <div class="contents"></div>
                </div>
            </nav>

            ${next.body()}

            <!-- jQuery Version 1.11.0 -->
            <script src="plugins/jquery-1.11.0.js"></script>

            <!-- Bootstrap Core JavaScript -->
            <script src="plugins/bootstrap/bootstrap.min.js"></script>

            <!-- Metis Menu Plugin JavaScript -->
            <script src="plugins/metisMenu/metisMenu.js"></script>

            <!-- Custom Application JavaScript -->
            <script>CONTROLLER_CMD="${controller_cmd}";</script>
            % if allowed_path:
                <script>ALLOWED_PATH="${allowed_path}";</script>
            % endif
            % for lib in common_libraries + page_map[pagename].libraries:
                <script src="${lib}"></script>
            % endfor
            ?>

        </div>
        <div id="common-templates">
            <div class="control-buttons" data-bot-id="" data-botnet="">
                <button type="submit" class="btn btn-default" title="Start" data-status-definition="starting" data-url="start"><span class="glyphicon glyphicon-play"></span></button>
                <button type="submit" class="btn btn-default" title="Stop" data-status-definition="stopping" data-url="stop"><span class="glyphicon glyphicon-stop"></span></button>
                <button type="submit" class="btn btn-default" title="Reload" data-status-definition="reloading" data-url="reload"><span class="glyphicon glyphicon-repeat"></span></button>
                <button type="submit" class="btn btn-default" title="Restart" data-status-definition="restarting" data-url="restart"><span class="glyphicon glyphicon-refresh"></span></button>
                <button type="submit" class="btn btn-default" title="Status" data-url="status"><span class="glyphicon glyphicon-arrow-down"></span></button>
            </div>
        </div>
    </body>
</html>

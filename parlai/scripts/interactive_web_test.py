#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Talk with a model using a web UI.
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any

import json

HOST_NAME = 'localhost'
PORT = 8080

SHARED: Dict[Any, Any] = {}
STYLE_SHEET = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.3.1/js/all.js"
WEB_HTML = """
<html>
    <link rel="stylesheet" href={} />
    <script defer src={}></script>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title> Conversational Chatbot </title>
    </head>
    <body>
    <nav class="navbar navbar-dark bg-dark fixed-top">
        <a class="navbar-brand" href="/"> Conversational Chatbot </a>
    </nav>
        
    <main role="main" style="margin-top: 50px">
        <div class="jumbotron">
        <div class="container">         
            <h6>This conversational chatbot is operated by ParlAI platform and modified by IITP-CMU studio project team 3. Detailed information is explained in the github and github page.</h6>

            <p class="text-center">
            <a class="btn btn-secondary btn-md" href="https://github.com/yongkyung-oh/CMU-Studio-Project/" role="button"> <i class="fab fa-github"></i> Github</a>
            <a class="btn btn-info btn-md" href="https://yongkyung-oh.github.io/CMU-Studio-Project/" role="button"> <i class="fab fa-github"></i> Github Page</a></p>

            <h6> Magic Keywords
            <ul>
            <li><b>BEGIN</b>: Begin Chatbot Conversation </li>
            <li><b>INFORMATION</b>: Show brief information about this Chatbot </li>
            <li><b>GOOGLE</b>: Search Keyword through Google </li>
            </ul>
            </h6>

        </div>
        </div>

        <div class="container" style="height: 70%">
        <div class="my-2 p-2 bg-white rounded shadow-sm">
            <section class="container">
                <div id="parent" class="container" style="overflow: auto; height: calc(100% - 50px); padding-top: 1em; padding-bottom: 1em;">
                    <article class="media alert alert-light">
                        <div class="media-body">
                        <div>
                            <p>
                            <strong>Instructions</strong>
                            <br>
                            Enter your message to start conversation, and the bot will respond interactively.
                            </p>
                        </div>
                        </div>
                    </article>
                </div>
                <div class="container" style="height: 50px">
                    <form id = "interact">
                        <div class="input-group">
                            <input class="form-control" type="text" id="userIn" placeholder="Type in a message">
                            <button id="respond" type="submit" class="btn btn-dark btn-sm">
                            Submit
                            </button>
                            <button id="restart" type="reset" class="btn btn-light btn-sm">
                            Restart
                            </button>
                        </div>
                    </form>
                </div>
            </section>
        </div>
        </div>
    </main>

        <script>
            function createChatRow(agent, text, stamp) {{
                var article = document.createElement("article");
                if (agent == "Instructions") {{
                    article.className = "media alert alert-light";
                }} else if (agent == "YOU") {{
                    article.className = "media alert alert-primary";
                }} else if (agent == "BOT") {{
                    article.className = "media alert alert-danger";
                }};

                var figure = document.createElement("figure");
                if (agent == "BOT") {{
                    figure.className = "align-self-center ml-3";
                }} else {{
                    figure.className = "align-self-center mr-3";
                }};

                var span = document.createElement("span");
                span.className = "icon is-large";

                var icon = document.createElement("i");
                icon.className = "fas fas fa-lg" + (agent === "YOU" ? " fa-user " : agent === "BOT" ? " fa-robot" : "");

                var media = document.createElement("div");
                media.className = "media-body";

                var content = document.createElement("div");
                if (agent == "BOT") {{
                    content.className = "text-right";
                }} else {{
                    content.className = "text-left";
                }};

                var para = document.createElement("p");
                var paraText = document.createTextNode(text);

                // Using Magic Keywords
                if (agent == "YOU") {{
                    // Make magic word bold
                    if (paraText.data.includes("BEGIN")) {{
                        var paraText = document.createElement("a");
                        paraText.innerHTML += "<b> BEGIN </b>";
                    }} else if (paraText.data.includes("GOOGLE")) {{
                        var paraText = document.createElement("a");
                        paraText.innerHTML += "<b> GOOGLE </b> "+text.substr(6)+"";
                    }} else if (paraText.data.includes("INFORMATION")) {{
                        var paraText = document.createElement("a");
                        paraText.innerHTML += "<b> INFORMATION </b>";
                    }};

                }} else if (agent == "BOT") {{
                    // Make search link text to href 
                    if (paraText.data.includes("https://www.google.com")) {{
                        var paraText = document.createElement("a");
                        paraText.innerHTML += "Here is the <a href='"+text+"'> <u> <b> search link </b> </u> </a>.";
                    }} else if (paraText.data.includes("https://parl.ai")) {{
                        var paraText = document.createElement("a");
                        paraText.innerHTML += "This conversational chatbot is operated by ParlAI platform and modified by IITP-CMU studio project team 3. If you want to contact developer team, please click the github (or github page) button. <br> ParlAI is a unified platform for sharing, training and evaluating dialogue models across many tasks, developed by Facebook AI research team. If you want to know much more about ParlAI, click <a href='https://parl.ai/'> <u> <b> here </b> </u> </a>.";
                    }};
                }};

                var strong = document.createElement("strong");
                strong.innerHTML = agent;
                var br = document.createElement("br");

                para.appendChild(strong);
                if (agent !== "Instructions") {{
                    para.appendChild(stamp);
                }};
                para.appendChild(br);
                para.appendChild(paraText);
                
                content.appendChild(para);
                media.appendChild(content);

                span.appendChild(icon);
                figure.appendChild(span);

                if (agent == "Instructions") {{
                    article.appendChild(media);
                }} else if (agent == "YOU") {{
                    article.appendChild(figure);
                    article.appendChild(media);
                }} else if (agent == "BOT") {{
                    article.appendChild(media);
                    article.appendChild(figure);
                }};

                return article;
            }}
            document.getElementById("interact").addEventListener("submit", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";

                var stamp_in = document.createElement("stamp")
                stamp_in.innerHTML = " (" + new Date().toISOString() + " )";

                fetch('/interact', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                    body: text
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");

                    parDiv.append(createChatRow("YOU", text, stamp_in));

                    // Change info for Model response
                    var stamp_out = document.createElement("stamp")
                    stamp_out.innerHTML = " (" + new Date().toISOString() + " )";

                    parDiv.append(createChatRow("BOT", data.text, stamp_out));
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
            document.getElementById("interact").addEventListener("reset", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";

                fetch('/reset', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");

                    parDiv.innerHTML = '';
                    parDiv.append(createChatRow("Instructions", "Enter your message to start conversation, and the bot will respond interactively.", ""));
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
        </script>
    </body>
    <footer> 
    <br>
    <p class="text-center"> &copy; 2020. <a href='https://parl.ai/'> <u> ParlAI </u> </a> and <a href='https://yongkyung-oh.github.io/CMU-Studio-Project/'> <u> IITP CMU Studio Project Team 3 </u> </a>. Copyright all rights reserved. </p>
    </footer>
</html>
"""  # noqa: E501


class MyHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            model_response = self._interactive_running(
                SHARED.get('opt'), body.decode('utf-8')
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            SHARED['agent'].reset()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def setup_interactive(shared):
    """
    Build and parse CLI opts.
    """
    parser = setup_args()
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on.')
    parser.add_argument(
        '--host',
        default=HOST_NAME,
        type=str,
        help='Host from which allow requests, use 0.0.0.0 to allow all IPs',
    )

    SHARED['opt'] = parser.parse_args(print_args=False)

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    # show args after loading model
    parser.opt = agent.opt
    parser.print_args()
    return agent.opt


if __name__ == '__main__':
    opt = setup_interactive(SHARED)
    MyHandler.protocol_version = 'HTTP/1.0'
    httpd = HTTPServer((opt['host'], opt['port']), MyHandler)
    print('http://{}:{}/'.format(opt['host'], opt['port']))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

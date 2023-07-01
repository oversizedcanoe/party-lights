import os
import cherrypy
import utility

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head>
                <link href="/static/css/style.css" rel="stylesheet">
            </head>
            <body>
                <div id="loadingScreen">
                    <marquee id="marquee" height="100%" width="100%" behavior="alternate" direction="down" scrolldelay="20" truespeed><marquee scrolldelay="20" truespeed behavior="alternate">Connecting...</marquee></marquee>
                </div>

                <div id="gridContainer">
                    <button id="rainbowButton" onclick="sendPost('flashRandom')">Flash Random</button>
                    <button style="background-color:blue" onclick="sendPost('lavaLampMode')">Lava Lamp Mode</button>
                    <button style="background-color:red" onclick="sendPost('raveMode')">Rave Mode</button>
                    <button id="shrekButton" onclick="sendPost('shrek')"></button>
                    <button style="background-color:lightyellow" onclick="sendPost('reset')">Reset to Normal</button>
                    <button style="background-color:gray" onclick="sendPost('toggle')">On/Off</button>
                </div>
                
            </body>
            <script src="/static/js/script.js"></script>
        </html>
        
        """

if __name__ == '__main__':
    # override default of 127.0.0.1 so this is accessible on all devices on this network
    ip_address = utility.get_ip_address()
    cherrypy.config.update({'server.socket_host': ip_address,
                        'server.socket_port': 8080})
    conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
        }

    cherrypy.quickstart(HelloWorld(), '/', conf)

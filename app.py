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
                <button onclick="sendPost('flashRandom')">Flash Random</button>
                <hr/>
                <button onclick="sendPost('lavaLampMode')">Lava Lamp Mode</button>
                <button onclick="sendPost('raveMode')">Rave Mode</button>
                <button onclick="sendPost('reset')">Reset to Normal</button>
                <button onclick="sendPost('off')">Off</button>
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

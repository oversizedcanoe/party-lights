import cherrypy
import utility

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
            <body>
                <button>Flash Random</button>
                <hr/>
                <button>Lava Lamp Mode</button>
                <button>Rave Mode</button>
                <button>Reset to Normal</button>
                <button>Off</button>
            </body>
        </html>
        
        """

if __name__ == '__main__':
    # override default of 127.0.0.1 so this is accessible on all devices on this network
    ip_address = utility.get_ip_address()
    cherrypy.config.update({'server.socket_host': ip_address,
                        'server.socket_port': 8080})

    cherrypy.quickstart(HelloWorld())

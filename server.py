import cherrypy
import utility

@cherrypy.expose
class Server(object):
    def POST(self, behaviour = ''):
        print(f'POST with value: {behaviour}')

        try:
            self.HandlePost(behaviour)
            return 'success'
        except Exception as inst:
            print('An error occurred: ' + str(inst))
            return 'error'

    def HandlePost(self, behaviour = ''):
        if behaviour == 'flash lights etc...':
            pass # do something in main




if __name__ == '__main__':
        # override default of 127.0.0.1 so this is accessible on all devices on this network
    ip_address = utility.get_ip_address()
    cherrypy.config.update({'server.socket_host': ip_address,
                        'server.socket_port': 8081})

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(Server(), '/', conf)

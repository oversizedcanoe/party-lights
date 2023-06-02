import cherrypy
import cherrypy_cors
import utility

class Server(object):

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def changeLight(self, behaviour = ''):
        print(f'POST with value: {behaviour}')

        try:
            self.HandlePost(behaviour)
            return 'Successfully posted:' + behaviour
        except Exception as inst:
            error = 'Error occurred: ' + str(inst) 
            print(error)
            return error

    def HandlePost(self, behaviour = ''):
        if behaviour == 'flashRandom':
            pass # do something in main
        elif behaviour == 'lavaLampMode':
            raise Exception('Fuck nugget')



if __name__ == '__main__':
    cherrypy_cors.install()
        # override default of 127.0.0.1 so this is accessible on all devices on this network
    ip_address = utility.get_ip_address()
    cherrypy.config.update({'server.socket_host': ip_address,
                        'server.socket_port': 8081})
    
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    dispatcher.connect(name='changeLight',
                        route='/changeLight',
                        action='changeLight',
                        controller=Server(),
                        conditions={'method': ['POST']})
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'cors.expose.on': True,
        }
    }
    cherrypy.quickstart(Server(), '/', conf)

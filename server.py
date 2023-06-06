import asyncio
import cherrypy
import cherrypy_cors
import party_light
import utility

class Server(object):

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def changeLight(self):
        try:
            request = cherrypy.request.json
            behaviour = request['behaviour']
            print('HandlePost with ' + behaviour)
            self.HandlePost(behaviour)
            return 'Successfully posted:' + behaviour
        except Exception as inst:
            error = 'Error occurred: ' + str(inst) 
            print(error)
            return error

    def HandlePost(self, behaviour):
        asyncio.run(party_light.run_behaviour(behaviour))

if __name__ == '__main__':
    cherrypy_cors.install()
        # override default of 127.0.0.1 so this is accessible on all devices on this network
    ip_address = utility.get_ip_address()
    cherrypy.config.update({'server.socket_host': ip_address,
                        'server.socket_port': 8081})
    
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json'),  
                                               ('Access-Control-Allow-Origin', '*'),
                                               ("Access-Control-Allow-Headers", "Content-Type"),
                                               ("Access-Control-Allow-Methods", "POST")],
            'cors.expose.on': True,
        }
    }

    cherrypy.quickstart(Server(), '/', conf)



# The issue is that each request coming into the server spawns a new thread. So we can't easily use the same event loop.
# However in the current way (using asyncio.run(...)) each new request results in this error from the kasa library: Detected protocol reuse between different event loop
# It also does not log errors properly
# According to the docs "This means that you need to use the same event loop for subsequent requests".
# So I believe the solution is to have some global event loop startup on the server's startup, then access that on a different thread somehow.
# See here for more info: https://docs.python.org/3/library/asyncio-dev.html#asyncio-multithreading
import cherrypy, os
from controllers import auth, domaincontroller, mailboxcontroller, aliascontroller
from database import model
from configuration import urldispatching, settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

global db_engine

if __name__ == '__main__':
    
    db_engine = create_engine(settings.connection_string, echo=True)
    model.initialize(db_engine)
    
    db_session_maker = sessionmaker(bind=db_engine)
    
    cherrypy.server.socket_host = settings.listen_address

    default_auth_manager = auth.AuthManager(db_session_maker)
    urldispatching.configure(
        default_auth_manager,
        domaincontroller.DomainController(db_session_maker, default_auth_manager),
        mailboxcontroller.MailboxController(db_session_maker, default_auth_manager),
        aliascontroller.AliasController(db_session_maker, default_auth_manager),
        )
        
    dispatcher = urldispatching.route_dispatcher
    
    
    conf = {
         '/api': {
             'request.dispatch': dispatcher,
             'tools.sessions.on': True,
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         },
         '/': {
             'tools.staticdir.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd()),
             'tools.staticdir.dir': './html/app',
             'tools.staticdir.index': 'index.html'
         }
    }
    cherrypy.quickstart(None, '/', conf)
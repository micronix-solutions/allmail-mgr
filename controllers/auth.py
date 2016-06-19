import cherrypy
from database import model
from passlib.hash import sha512_crypt
import datetime
from configuration import settings

class AuthManager(object):
    
    def __init__(self, db_session_maker):
        self.db_session_maker = db_session_maker
    
    ##########################
    #####Request Handlers#####
    ##########################
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def login(self):
        try:
            the_email = cherrypy.request.json["user"]
            the_mailbox = the_email.split("@")[0]
            the_domain = the_email.split("@")[1]
            the_password = cherrypy.request.json["password"]
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")
        except IndexError:
            raise cherrypy.HTTPError("400 Bad Request", "Invalid parameters")
        
        db_session = self.db_session_maker()
        user_query = db_session.query(model.Mailbox) \
            .join(model.Domain) \
            .filter(model.Domain.domain_name == the_domain) \
            .filter(model.Mailbox.mailbox_name == the_mailbox) \
            .filter(model.Mailbox.active == True)
            
        if user_query.count() < 1:
            raise cherrypy.HTTPError("404 Not Found", "Bad username")
        
        if user_query.filter(model.Mailbox.password == settings.password_encryptor(the_password)).count() < 1:
            raise cherrypy.HTTPError("404 Not Found", "Bad username or password")
            
        the_user = user_query.one()
        
        if len(the_user.tokens) < 1:
            the_user.tokens.append(model.Token())
        
        the_token = the_user.tokens[0]
        
        the_token.token_value = settings.token_generator()
        
        the_token.last_used = datetime.datetime.now()
        
        db_session.commit()
        
        return {"user" : the_email, "token" : the_token.token_value}
    
    ##########################
    #######Auth Helpers#######
    ##########################
      
    def checkToken(self):
        try:
            token = cherrypy.request.headers["Authorization"]
        except KeyError:
            raise cherrypy.HTTPError("401 Unauthorized", "Missing auth token")
        
        db_session = self.db_session_maker()
        
        the_token_value = token.replace("Token ", "")
        
        the_token_query = db_session.query(model.Token) \
            .filter(model.Token.token_value == the_token_value)
        
        if the_token_query.count() < 1:
            raise cherrypy.HTTPError("401 Unauthorized", "Invalid auth token")
            
        the_token = the_token_query.one()
        
        if the_token.last_used < datetime.datetime.now() - settings.auth_token_timeout:
            raise cherrypy.HTTPError("401 Unauthorized", "Token has expired")
            
        the_token.last_used = datetime.datetime.now()
        
        db_session.commit()
        
        return the_token.mailbox
        
    def authenticateGlobalAdminOr403(self):
        the_user = self.checkToken()
        if not the_user.is_global_admin:
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
        
        return the_user
    
    def authenticateDomainAdminOr403(self, domain_name):
        the_user = self.checkToken()
        if not (the_user.is_global_admin or (the_user.is_domain_admin and the_user.domain.domain_name == domain_name)):
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
            
        return the_user
        
    def authenticateAnyAdminOr403(self):
        the_user = self.checkToken()
        if not the_user.is_global_admin or the_user.is_domain_admin:
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
            
        return the_user
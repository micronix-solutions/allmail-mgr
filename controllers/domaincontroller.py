import cherrypy
from database import model
from configuration import settings

class DomainController(object):
    
    def __init__(self, db_session_maker, auth_manager):
        self.db_session_maker = db_session_maker
        self.auth_manager = auth_manager
        
    ##########################
    #########DB Stuff#########
    ##########################
    
    def get_domain(self, db_session, domain_name):
        return db_session.query(model.Domain).filter(model.Domain.domain_name==domain_name).one()
        
    ##########################
    #####Request Handlers#####
    ##########################
    
    @cherrypy.tools.json_out()
    def list(self):
        the_user = self.auth_manager.authenticateAnyAdminOr403()
        db_session = self.db_session_maker()
        domains_query = db_session.query(model.Domain)
        if the_user.is_domain_admin and not the_user.is_global_admin:
            domains_query = domains_query.filter(model.Domain.id==the_user.domain.id)
            
        domains_json = map(
            lambda domain: {
                "domain_name" : domain.domain_name, 
                "active" : domain.active
            }, 
            domains_query.all()
        )
        return domains_json
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create(self):
        the_user = self.auth_manager.authenticateGlobalAdminOr403()
        db_session = self.db_session_maker()
        try:
            new_domain = model.Domain(
                domain_name = cherrypy.request.json["domain_name"].lower(), 
                active = cherrypy.request.json["active"]
            )
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")
        
        db_session.add(new_domain)
        db_session.commit()
        cherrypy.response.status = "201 Domain Created"
        return {
            "domain_name" : new_domain.domain_name, 
            "id" : new_domain.id
        }
    
    @cherrypy.tools.json_out()
    def get(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_domain = self.get_domain(db_session, domain_name)
        return {
            "domain_name" : the_domain.domain_name, 
            "active" : the_domain.active
        }
        
    @cherrypy.tools.json_in()
    def update(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        try:
            domain_active = cherrypy.request.json["active"]
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")
        
        db_session = self.db_session_maker()
        the_domain = get_domain(db_session, domain_name)
        the_domain.active = domain_active
        db_session.commit()
        cherrypy.response.status = "204 Domain Updated"
        return
    
    def delete(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_domain = self.get_domain(db_session, domain_name)
        db_session.delete(the_domain)
        db_session.commit();
        cherrypy.response.status = "204 Domain Deleted"
        return
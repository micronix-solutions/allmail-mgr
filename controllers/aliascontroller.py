import cherrypy
from database import model
from configuration import settings

class AliasController(object):
    
    def __init__(self, db_session_maker, auth_manager):
        self.db_session_maker = db_session_maker
        self.auth_manager = auth_manager
        
    ##########################
    #########DB Stuff#########
    ##########################
    
    def get_alias(self, db_session, domain_name, alias_name):
        return db_session.query(model.Alias) \
            .join(model.Domain) \
            .filter(model.Domain.domain_name == domain_name) \
            .filter(model.Alias.alias_name == alias_name) \
            .one()
    
    @cherrypy.tools.json_out()
    def list(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        aliases_query = db_session.query(model.Domain).filter(model.Domain.domain_name==domain_name).first().aliases
        aliases_json = map(
            lambda alias: {
                "alias" : alias.alias_name, 
                "targets" : alias.targets,
                "active" : alias.active
            }, 
            aliases_query
        )

        return aliases_json
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_domain = db_session.query(model.Domain).filter(model.Domain.domain_name==domain_name).one()
        try:
            new_alias = model.Alias(
                domain = the_domain,
                alias_name = cherrypy.request.json["alias_name"].lower(),
                active = cherrypy.request.json["active"],
                targets = cherrypy.request.json["targets"].lower()
            )
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")
        
        db_session.add(new_alias)
        db_session.commit()
        cherrypy.response.status = "201 Alias Created"
        return {
            "alias_name" : new_alias.alias_name, 
            "id" : new_alias.id
        }
    
    @cherrypy.tools.json_out()
    def get(self, domain_name, alias_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_alias = self.get_alias(db_session, domain_name, alias_name)
            
        return {
            "alias" : the_alias.alias_name, 
            "targets" : the_alias.targets,
            "active" : the_alias.active
        }
    
    @cherrypy.tools.json_in()
    def update(self, domain_name, alias_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_alias = self.get_alias(db_session, domain_name, alias_name)
        try:
            the_alias.targets = cherrypy.request.json["targets"].lower()
            the_alias.active = cherrypy.request.json["active"]
        
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")    
        
        db_session.commit()
        cherrypy.response.status = "204 Alias Updated"
        return
    
    def delete(self, domain_name, alias_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_alias = self.get_alias(db_session, domain_name, alias_name)
        db_session.delete(the_alias)
        db_session.commit();
        cherrypy.response.status = "204 Alias Deleted"
        return
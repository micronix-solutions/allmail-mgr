import cherrypy
from database import model
from configuration import settings

class MailboxController(object):
    
    ##########################
    #####Request Handlers#####
    ##########################
    
    def __init__(self, db_session_maker, auth_manager):
        self.db_session_maker = db_session_maker
        self.auth_manager = auth_manager
    
    @cherrypy.tools.json_out()
    def list(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        mailboxes_query = db_session.query(model.Domain).filter(model.Domain.domain_name==domain_name).first().mailboxes
        mailboxes_json = map(
            lambda mailbox: {
                "mailbox" : mailbox.mailbox_name, 
                "active" : mailbox.active, 
                "quota_gb" : mailbox.quota_gb, 
                "is_domain_admin" : mailbox.is_domain_admin, 
                "is_global_admin" : mailbox.is_global_admin 
            }, 
            mailboxes_query
        )

        return mailboxes_json
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create(self, domain_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_domain = db_session.query(model.Domain).filter(model.Domain.domain_name==domain_name).one()
        try:
            new_mailbox = model.Mailbox(
                domain = the_domain,
                mailbox_name = cherrypy.request.json["mailbox_name"].lower(),
                password = settings.password_encryptor(cherrypy.request.json["password"]),
                quota_gb = cherrypy.request.json["quota_gb"],
                is_global_admin = the_user.is_global_admin and cherrypy.request.json["is_global_admin"],
                is_domain_admin = cherrypy.request.json["is_domain_admin"],
                active = cherrypy.request.json["active"]
            )
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")
        
        db_session.add(new_mailbox)
        db_session.commit()
        cherrypy.response.status = "201 Mailbox Created"
        return {
            "mailbox_name" : new_mailbox.mailbox_name, 
            "id" : new_mailbox.id
        }

    @cherrypy.tools.json_out()
    def get(self, domain_name, mailbox_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_mailbox = self.get_mailbox(db_session, domain_name, mailbox_name)
            
        return {
            "mailbox" : the_mailbox.mailbox_name, 
            "active" : the_mailbox.active, 
            "quota_gb" : the_mailbox.quota_gb, 
            "is_domain_admin" : the_mailbox.is_domain_admin, 
            "is_global_admin" : the_mailbox.is_global_admin 
        }
    
    @cherrypy.tools.json_in()
    def update(self, domain_name, mailbox_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_mailbox = self.get_mailbox(db_session, domain_name, mailbox_name)
        if the_mailbox.is_global_admin and not the_user.is_global_admin:
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
        try:
            the_mailbox.quota_gb = cherrypy.request.json["quota_gb"]
            is_domain_admin = cherrypy.request.json["is_domain_admin"]
            the_mailbox.is_global_admin = cherrypy.request.json["is_global_admin"]
            the_mailbox.is_domain_admin = cherrypy.request.json["is_domain_admin"]
            the_mailbox.active = cherrypy.request.json["active"]
        
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")    
        
        db_session.commit()
        cherrypy.response.status = "204 Mailbox Updated"
        return
    
    @cherrypy.tools.json_in()
    def update_password(self, domain_name, mailbox_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_mailbox = self.get_mailbox(db_session, domain_name, mailbox_name)
        if the_mailbox.is_global_admin and not the_user.is_global_admin:
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
        try:
            the_mailbox.password = settings.password_encryptor(cherrypy.request.json["password"])
        except KeyError:
            raise cherrypy.HTTPError("400 Bad Request", "Improperly formatted request")    
        
        db_session.commit()
        cherrypy.response.status = "204 Password Updated"
        return
    
    def delete(self, domain_name, mailbox_name):
        the_user = self.auth_manager.authenticateDomainAdminOr403(domain_name)
        db_session = self.db_session_maker()
        the_mailbox = self.get_mailbox(db_session, domain_name, mailbox_name)
        if the_mailbox.is_global_admin and not the_user.is_global_admin:
            raise cherrypy.HTTPError("403 Forbidden", "Insufficient Permission")
        db_session.delete(the_mailbox)
        db_session.commit();
        cherrypy.response.status = "204 Mailbox Deleted"
        return
    
    ##########################
    #########DB Stuff#########
    ##########################
    
    def get_mailbox(self, db_session, domain_name, mailbox_name):
        return db_session.query(model.Mailbox) \
            .join(model.Domain) \
            .filter(model.Domain.domain_name == domain_name) \
            .filter(model.Mailbox.mailbox_name == mailbox_name) \
            .one()
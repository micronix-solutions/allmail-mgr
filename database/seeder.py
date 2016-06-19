import cherrypy
from database import model
from configuration import settings

def seed_db(db_session_maker):
    db_session = db_session_maker()
    if db_session.query(model.Domain).count() < 1:
        localhost_domain = model.Domain(domain_name="localhost", active=True)
        localhost_user = model.Mailbox(
            domain=localhost_domain, 
            mailbox_name="root", 
            password = settings.password_encryptor("12345"), 
            quota_gb=5, 
            is_global_admin=True, 
            is_domain_admin=False, 
            active=True
        )
        db_session.add_all([
            localhost_domain,
            localhost_user
        ])
        
        db_session.commit()
        
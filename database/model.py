from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Domain(Base):
    
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True)
    domain_name = Column(String, unique=True)
    active = Column(Boolean(create_constraint=True))
    
class Mailbox(Base):
    
    __tablename__ = "mailboxes"
    
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domains.id"))
    mailbox_name = Column(String)
    password = Column(String)
    active = Column(Boolean(create_constraint=True))
    is_domain_admin = Column(Boolean(create_constraint=False))
    is_global_admin = Column(Boolean(create_constraint=False))
    quota_gb = Column(Integer)
    
    domain = relationship("Domain", backref=backref("mailboxes", order_by=mailbox_name, cascade="all, delete, delete-orphan"), single_parent=True)
    
class Alias(Base):
    
    __tablename__ = "aliases"
    
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domains.id"))
    alias_name = Column(String)
    targets = Column(Text)
    active = Column(Boolean(create_constraint=True))
    
    domain = relationship("Domain", backref=backref("aliases", order_by=alias_name, cascade="all, delete, delete-orphan"), single_parent=True)
    
class Token(Base):
    
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    mailbox_id = Column(Integer, ForeignKey("mailboxes.id"), unique=True)
    token_value = Column(String)
    created = Column(DateTime, default = func.now())
    last_used = Column(DateTime)
    
    mailbox = relationship("Mailbox", backref=backref("tokens", order_by=created), cascade="all, delete, delete-orphan", single_parent=True)
    
def initialize(engine):
    Base.metadata.create_all(engine)
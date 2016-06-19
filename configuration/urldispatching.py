import cherrypy

route_dispatcher = cherrypy.dispatch.RoutesDispatcher()

def configure(auth_manager, domain_controller,mailbox_controller,alias_controller):
    route_dispatcher.connect("auth_mgr", "/api/login", controller=auth_manager, action="login", conditions=dict(method=['POST']))
    route_dispatcher.connect("domain_mgr", "/api/domains", controller=domain_controller, action='list', conditions=dict(method=['GET']))
    route_dispatcher.connect("domain_mgr", "/api/domains", controller=domain_controller, action='create', conditions=dict(method=['POST']))
    route_dispatcher.connect("domain_mgr", "/api/domains/{domain_name}", controller=domain_controller, action='get', conditions=dict(method=['GET']))
    route_dispatcher.connect("domain_mgr", "/api/domains/{domain_name}", controller=domain_controller, action='update', conditions=dict(method=['PUT']))
    route_dispatcher.connect("domain_mgr", "/api/domains/{domain_name}", controller=domain_controller, action='delete', conditions=dict(method=['DELETE']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes", controller=mailbox_controller, action='list', conditions=dict(method=['GET']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes", controller=mailbox_controller, action='create', conditions=dict(method=['POST']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes/{mailbox_name}", controller=mailbox_controller, action='get', conditions=dict(method=['GET']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes/{mailbox_name}", controller=mailbox_controller, action='update', conditions=dict(method=['PUT']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes/{mailbox_name}/password", controller=mailbox_controller, action='update_password', conditions=dict(method=['PUT']))
    route_dispatcher.connect("mailbox_mgr", "/api/domains/{domain_name}/mailboxes/{mailbox_name}", controller=mailbox_controller, action='delete', conditions=dict(method=['DELETE']))
    route_dispatcher.connect("alias_mgr", "/api/domains/{domain_name}/aliases", controller=alias_controller, action='list', conditions=dict(method=['GET']))
    route_dispatcher.connect("alias_mgr", "/api/domains/{domain_name}/aliases", controller=alias_controller, action='create', conditions=dict(method=['POST']))
    route_dispatcher.connect("alias_mgr", "/api/domains/{domain_name}/aliases/{alias_name}", controller=alias_controller, action='get', conditions=dict(method=['GET']))
    route_dispatcher.connect("alias_mgr", "/api/domains/{domain_name}/aliases/{alias_name}", controller=alias_controller, action='update', conditions=dict(method=['PUT']))
    route_dispatcher.connect("alias_mgr", "/api/domains/{domain_name}/aliases/{alias_name}", controller=alias_controller, action='delete', conditions=dict(method=['DELETE']))
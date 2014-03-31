"""
flask_cas.__init__
"""

from flask import current_app

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from . import routing

class CAS(object):
    """
    Required Configs:
    
    |Key             |
    |----------------|
    |CAS_SERVER      | 
    |CAS_AFTER_LOGIN |

    Optional Configs:

    |Key                      | Default      |
    |-------------------------|--------------|
    |CAS_TOKEN_SESSION_KEY    | _CAS_TOKEN   |
    |CAS_USERNAME_SESSION_KEY | CAS_USERNAME |
    """

    def __init__(self, app=None, url_prefix=None):
        self.app = app
        if app is not None:
            self.init_app(app, url_prefix)

    def init_app(self, app, url_prefix=None):
        # Configuration defaults
        app.config.setdefault('CAS_TOKEN_SESSION_KEY', '_CAS_TOKEN')
        app.config.setdefault('CAS_USERNAME_SESSION_KEY', 'CAS_USERNAME')
        
        # Register Blueprint
        app.register_blueprint(routing.blueprint, url_prefix=url_prefix)

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top

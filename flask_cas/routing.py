"""
flask_cas.routing
"""

import flask
from flask import current_app
from .cas_urls import \
    create_cas_login_url, \
    create_cas_logout_url, \
    create_cas_validate_url

import urllib

blueprint = flask.Blueprint('cas', __name__)

@blueprint.route('/login/')
def login():
    """
    This route is has two purposes. First, it is used by the user 
    to login. Second, it is used by the CAS to respond with the 
    `ticket` after the user logins in successfully.

    When the user accesses this url they are redirected to the CAS
    to login. If the login was successful the CAS will respond to this
    route with the ticket in the url. The ticket this then validated. 
    If validation was successful the logged in username is saved in 
    the user's session under the key `CAS_USERNAME_SESSION_KEY`.
    """
    
    cas_token_session_key = current_app.config['CAS_TOKEN_SESSION_KEY']

    redirect_url = create_cas_login_url(
        current_app.config['CAS_SERVER'],
        flask.url_for('.login', _external=True))

    if 'ticket' in flask.request.args:
        flask.session[cas_token_session_key] = flask.request.args['ticket']

    if cas_token_session_key in flask.session:

        if validate(flask.session[cas_token_session_key]):
            redirect_url = flask.url_for(
                current_app.config['CAS_AFTER_LOGIN'])
        else:
            del flask.session[cas_token_session_key]

    current_app.logger.debug('Redirecting to: {}'.format(redirect_url))

    return flask.redirect(redirect_url)

@blueprint.route('/logout/')
def logout():
    """
    When the user accesses this route they are logged out.
    """
    
    cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']

    if cas_username_session_key in flask.session:
        del flask.session[cas_username_session_key]
    redirect_url = create_cas_logout_url(current_app.config['CAS_SERVER'])
    current_app.logger.debug('Redirecting to: {}'.format(redirect_url))
    return flask.redirect(redirect_url)

def validate(ticket):
    """
    Will attempt to validate the ticket. If validation fails False 
    is returned. If validation is successful then True is returned 
    and the validated username is saved in the session under the 
    key `CAS_USERNAME_SESSION_KEY`.
    """

    cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']

    current_app.logger.debug("validating token {}".format(ticket))

    cas_validate_url = create_cas_validate_url(
        current_app.config['CAS_SERVER'], 
        flask.url_for('.login', _external=True),
        ticket)
    
    current_app.logger.debug("Making GET request to {}".format(
        cas_validate_url))

    try:
        (isValid, username) = urllib.urlopen(cas_validate_url).readlines()
        isValid = True if isValid.strip() == b'yes' else False
        username = username.strip().decode('utf8', 'ignore')
    except ValueError:
        current_app.logger.error("CAS returned unexpected result")
        isValid = False

    if isValid:
        current_app.logger.debug("valid")
        flask.session[cas_username_session_key] = username
    else:
        current_app.logger.debug("invalid")

    return isValid

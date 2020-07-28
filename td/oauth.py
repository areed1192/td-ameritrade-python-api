import os
import pathlib

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import render_template

from flask.json import jsonify
from td.app.auth import FlaskTDAuth
from configparser import ConfigParser

# Define the templates folder.
template_folder_path: pathlib.Path = pathlib.Path(__file__).parents[0]
template_folder_path: pathlib.Path = template_folder_path.joinpath('templates')

# Create the App.
app = Flask('TD_oAuth_App', template_folder=template_folder_path.resolve())


@app.route("/")
def home():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    return render_template("index.html")

@app.route("/login")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    # Build the authorization URL.
    auth_tuple = app.config['auth_client'].authorization_url()

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = auth_tuple[1]

    return redirect(auth_tuple[0])


@app.route("/login/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    # Grab the Refresh and Access Token.
    token_dict = app.config['auth_client'].grab_access_token_and_refresh_token(url=request.url)
    
    # Store it in the Session.
    session['oauth_token'] = token_dict

    if app.config['call_close']:
        return redirect(url_for('shutdown'))

    return jsonify(token_dict)

@app.route("/login/refresh", methods=["GET"])
def refresh():

    # Grab the Refresh Token.
    refresh_token_dict = app.config['auth_client'].grab_refresh_token()

    return jsonify(refresh_token_dict)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def run(flask_client: FlaskTDAuth, close_after: bool = False):

    certs_pem = pathlib.Path(__file__).parents[0].joinpath('certs/cert.pem')
    certs_key = pathlib.Path(__file__).parents[0].joinpath('certs/key.pem')

    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    app.config['auth_client'] = flask_client
    app.config['call_close'] = close_after
    app.run(
        ssl_context=(certs_pem, certs_key),
        host='localhost',
        port=5000,
        debug=True
    )


if __name__ == "__main__":

    # Grab configuration values.
    config = ConfigParser()
    config.read('config/config.ini')

    client_id = config.get('main', 'client_id')
    redirect_uri = config.get('main', 'redirect_uri')
    credentials = config.get('main','json_path')

    # Define the Secret Key.
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # Define the App Configurations.
    app.config['auth_client'] = FlaskTDAuth(
        client_id=client_id,
        redirect_uri=redirect_uri,
        credentials_file=pathlib.Path(credentials)
    )

    # Run the App.
    app.run(
        ssl_context=('td/certs/cert.pem', 'td/certs/key.pem'),
        host='localhost',
        port=5000,
        debug=True
    )

    # flask_td_app = FlaskAppTD(client_id=client_id, redirect_uri=redirect_uri, credentials_file=credentials)
    # flask_td_app.run()
    # This allows us to use a plain HTTP callback
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    # # app.run(ssl_context="adhoc")

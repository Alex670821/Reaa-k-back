from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "random secret"
oauth = OAuth(app)

# Configura tu proveedor OAuth aquí
google = oauth.register(
    name="google",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    client_kwargs={"scope": "email profile"},
    # Asegúrate de que la redirección coincida con la URI registrada en Google Console
    redirect_uri="http://127.0.0.1:5000/authorize",
)


@app.route("/")
def home():
    return "Welcome to the Flask OAuth Example"


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    resp = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
    user_info = resp.json()
    # Do something with the user info, like storing it in the session
    session["user"] = user_info
    return f"Hello, {user_info['name']}!"


if __name__ == "__main__":
    app.run(debug=True)
import os
import secrets
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request

app = Flask(__name__)

CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY", "").strip()
CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")

print("CLIENT_KEY carregada:", bool(CLIENT_KEY))
print("CLIENT_KEY tamanho:", len(CLIENT_KEY))

REDIRECT_URI = "https://noirflow-backend.onrender.com/auth/callback/"

TIKTOK_AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>NoirFlow Backend</title>
        </head>
        <body>
            <h1>NoirFlow Backend</h1>
            <p>Backend online.</p>
            <a href="/oauth">Connect with TikTok</a>
        </body>
    </html>
    """

@app.route("/oauth")
def oauth():
    state = secrets.token_urlsafe(32)

    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic,video.publish",
        "redirect_uri": REDIRECT_URI,
        "state": state
    }

    return redirect(
        TIKTOK_AUTHORIZE_URL + "?" + urlencode(params)
    )

@app.route("/auth/callback/")
def callback():
    error = request.args.get("error")

    if error:
        return f"TikTok authorization error: {error}"

    code = request.args.get("code")

    if not code:
        return "Authorization code not received."

    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(
        TIKTOK_TOKEN_URL,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=30
    )

    return f"""
    <h1>NoirFlow</h1>
    <h2>TikTok authorization completed</h2>
    <pre>{response.text}</pre>
    """

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

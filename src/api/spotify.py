from flask import Blueprint, jsonify, redirect, request, session, url_for
import base64
import json
import os
import requests


spotify = Blueprint('spotify', __name__)

SPOTIFY_API = "https://api.spotify.com"

@spotify.route('/api/spotify/')
def home():
    if session.get('auth_header'):
        return user_profile()
    else:
        return "Welcome to my Spotify API you aren't logged in!"

@spotify.route('/api/spotify/callback')
def callback():
    auth_str = bytes(f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}', 'utf-8')
    b64_auth = base64.b64encode(auth_str).decode('utf-8')
    header = {'Authorization': f'Basic {b64_auth}'}
    data = dict(
        grant_type='authorization_code',
        code=request.args.get('code'),
        redirect_uri='http://localhost:5000/api/spotify/callback')
    response = requests.request('POST', 'https://accounts.spotify.com/api/token', headers=header, data=data)
    
    response_data = json.loads(response.text)
    session['auth_header'] = {'Authorization': f'Bearer {response_data.get("access_token")}'}

    return redirect(url_for(home))

@spotify.route('/api/spotify/authenticate')
def authenticate():
    client_id = os.getenv('CLIENT_ID')

    payload = dict(
        client_id=client_id,
        response_type='code',
        redirect_uri='http://localhost:5000/api/spotify/callback',
        scope='playlist-read-private playlist-read-collaborative user-library-modify playlist-modify-private playlist-modify-public'
    )

    response = requests.request('GET', 'https://accounts.spotify.com/authorize', params=payload)
    
    
    return redirect(response.url)

@spotify.route('/api/spotify/user_name')
def user_profile():
    response = requests.request('GET', f"{SPOTIFY_API}/v1/me", headers=session.get('auth_header'))
    response_data = json.loads(response.text)

    return response_data


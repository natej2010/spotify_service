from flask import Blueprint, jsonify, make_response, redirect, request, session, url_for
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


# @spotify.route('/api/spotify/callback')
# def callback():
#     auth_header = get_auth_header()
#     return {'Authorization': f'Bearer {auth_header}'}


@spotify.route('/api/spotify/get_auth_header', methods = ['POST'])
def get_auth_header():
    request_data = json.loads(request.data)

    auth_str = bytes(f'{os.getenv("CLIENT_ID")}:{os.getenv("CLIENT_SECRET")}', 'utf-8')
    b64_auth = base64.b64encode(auth_str).decode('utf-8')
    header = {'Authorization': f'Basic {b64_auth}'}
    data = dict(
        grant_type='authorization_code',
        code=request_data.get('code'),
        redirect_uri=request_data.get('callback'))
    response = requests.request('POST', 'https://accounts.spotify.com/api/token', headers=header, data=data)
    
    response_data = json.loads(response.text)
    return {'Authorization': f'Bearer {response_data.get("access_token")}'}

              
@spotify.route('/api/spotify/authenticate')
def authenticate():
    client_id = os.getenv('CLIENT_ID')
    callback = request.args.get('callback', 'http://localhost:5000/api/spotify/callback')

    payload = dict(
        client_id=client_id,
        response_type='code',
        redirect_uri=callback,
        scope='playlist-read-private playlist-read-collaborative user-library-modify playlist-modify-private playlist-modify-public'
    )
 
    response = requests.request('GET', 'https://accounts.spotify.com/authorize', params=payload)
    return response.url

 
@spotify.route('/api/spotify/user_profile', methods = ['GET', 'POST'])
def user_profile():

    request_data = json.loads(request.data)
    headers = json.loads(request_data.get('headers'))

    response = requests.request('GET', f"{SPOTIFY_API}/v1/me", headers=headers)
    response_data = json.loads(response.text)

    return jsonify(response_data)

from flask import Blueprint, jsonify, request
import os
import requests


spotify = Blueprint('spotify', __name__)


@spotify.route('/api/spotify/authenticate')
def authenticate():
    client_id = os.getenv('CLIENT_ID')
    client_service = os.getenv('CLIENT_SECRET')

    payload = dict(
        client_id=client_id,
        response_type='code',
        redirect_uri='http://localhost/',
        scope='playlist-read-private playlist-read-collaborative user-library-modify playlist-modify-private playlist-modify-public'
    )

    response = requests.request('GET', 'https://accounts.spotify.com/authorize', headers=headers)
    
    return "token"

# Get Game Night Status
@game.route('/api/game/status', methods=['GET'])
def get_game_night_game_status():
    game_id = request.args.get('game_id')
    status_id = request.args.get('status_id')
    ds = get_client()
    game = ds.get(game_id)
    return game['status']

# Update Game Night Status
@game.route('/api/game/status/<int:id>', methods=['POST'])
def set_game_status():
    game_id = request.args.get('game_id')
    status_id = request.args.get('status_id')
    ds=get_client();
    game = ds.get(game_id)
    game['status']=status_id
    ds.put(game)


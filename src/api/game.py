from flask import Blueprint, jsonify, request
from google.cloud import datastore

game = Blueprint('game', __name__)

# Fetch the Datastore Client
def get_client():
   return datastore.Client('cachememorymillionaires')

@game.route('/api/game/<int:id>')
def get_game(id):
    games = {1: {'name': 'game1', 'details': 'game1_details'},
             2: {'name': 'game2', 'details': 'game2_details'}}
    return jsonify(games.get(id, 'Failed to find game.'))

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


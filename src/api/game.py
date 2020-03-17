from flask import Blueprint, jsonify

game = Blueprint('game', __name__)


@game.route('/api/game/<int:id>')
def get_game(id):
    games = {1: {'name': 'game1', 'details': 'game1_details'},
             2: {'name': 'game2', 'details': 'game2_details'}}
    return jsonify(games.get(id, 'Failed to find game.'))

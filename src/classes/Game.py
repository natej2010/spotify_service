import requests
import xmltodict

from time import sleep


class Game:
    def __init__(self, bgg_id, name, description=None, max_players=None, min_players=None, min_playtime=None, max_playtime=None, num_plays=None, image=None, thumbnail=None, year_published=None):
        self.bgg_id = bgg_id,
        self.name = name,
        self.description = description,
        self.max = max_players,
        self.min = min_players,
        self.min = min_playtime,
        self.max = max_playtime,
        self.num_plays = num_plays,
        self.image = image,
        self.thumbnail = thumbnail,
        self.year = year_published
        self.link = f'https://boardgamegeek.com/boardgame/{bgg_id}'
    

    @staticmethod
    def build_game_from_user_data(game_details):

        if type(game_details['name']) is list:
            name = game_details['name'][0]['@value']
        else:
            name = game_details['name']['@value']

        return Game(bgg_id=game_details['@id'], 
                    name=name,
                    description=game_details['description'], 
                    max_players=game_details['maxplayers']['@value'], 
                    min_players=game_details['minplayers']['@value'], 
                    min_playtime=game_details['minplaytime']['@value'],
                    max_playtime=game_details['maxplaytime']['@value'],
                    num_plays=game_details['numplays'], 
                    image=game_details['image'], 
                    thumbnail=game_details['thumbnail'], 
                    year_published=game_details['yearpublished']['@value']
)
    

    @staticmethod
    def get_game_details_from_bgg(api, game_id):
        tries = 0

        url = f'{api}/thing'

        querystring = {'id': game_id}
        response = requests.request("POST", url, data='payload', params=querystring)

        while response.status_code == 202: 
            sleep(5)
            response = requests.request("POST", url, data='payload', params=querystring)
            tries += 1

            if tries == 5:
                return None

        if response.status_code == 200:
            game_details = xmltodict.parse(response.text)
        else:
            game_details = None

        if not game_details:
            # TODO need to handle situation where we fail to get the game details
            pass

        return game_details

    # TODO: This code is used to get game collection detail from BGG
    def game_details(self):
        collection_details = Game.get_game_details_from_bgg(api, ",".join(game_ids))

        d = defaultdict(dict)
        for elem in chain(games, collection_details.get('items').get('item')):
            key = elem.get('@objectid') if elem.get('@objectid') else elem.get('@id')
            d[key].update(elem)
        game_details = list(d.values())
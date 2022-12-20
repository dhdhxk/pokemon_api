import requests


class Pokeapi:
    base_url: str = None

    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"

    def retrieve_pokemon(self, _name):
        """
        Retrieve pokemon base information

        :param _name: name of the pokemon
        :return: pokemon json response
        """
        try:
            response = requests.get(self.base_url + '/pokemon/' + _name)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return response

    def retrieve_pokemon_species(self, _species):
        """
        Retrieve pokemon species information

        :param _species: species object from pokemon
        :return: pokemon species json response
        """
        try:
            response = requests.get(_species["url"])
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return response

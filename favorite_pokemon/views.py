import random
import json
import statistics
from django.http.response import HttpResponse
from favorite_pokemon.libs.pokeapi import Pokeapi


# Create your views here.
def index_view(request):
    # Predefine Favorite Pokemon
    favorite_pokemon_list: list = ['pikachu', 'eevee', 'charmander', 'bulbasaur', 'mew']

    # Create dict for return value
    output: dict = {
        'pokemons': []
    }

    # Create list to store base_happiness
    base_happiness_list: list = []

    # If is_extended is True, show base_happiness Stat (Task 2)
    is_extended: bool = False

    # If the request has &get_happiness=true
    if request.GET.get('get_happiness') == "true":
        is_extended = True
        output['base_happiness_stat'] = {}

    try:
        pokeapi_inst = Pokeapi()  # Initialize Instance

        for pokemon_name in favorite_pokemon_list:
            # Get Base Pokemon data
            pokemon_data = pokeapi_inst.retrieve_pokemon(pokemon_name).json()

            # Get Pokemon Species data.
            species_data = pokeapi_inst.retrieve_pokemon_species(pokemon_data["species"]).json()

            # Get 2 Random move index
            move_list: list = random.sample(range(0, len(pokemon_data['moves'])-1), 2)

            # Store base happiness to get statistics (Task 2)
            base_happiness_list.append(species_data['base_happiness'])

            # Create Dict for Pokemon data
            pokemon_data: dict = {
                'name': pokemon_data['name'],
                'height': pokemon_data['height'],
                'weight': pokemon_data['weight'],
                'color': species_data['color']['name'],
                'moves': [
                    pokemon_data['moves'][move_list[0]],
                    pokemon_data['moves'][move_list[1]]
                ],
                'base_happiness': species_data['base_happiness']
            }
            output['pokemons'].append(pokemon_data)

        # If is_extended is True, calculate statistics for base_happiness and return it. (Task 2)
        if is_extended is True:
            # Sort list to get median
            base_happiness_list.sort()

            # Calculate Median
            mid_index: int = len(base_happiness_list) // 2
            output['base_happiness_stat']['median'] = (base_happiness_list[mid_index]
                                                       + base_happiness_list[~mid_index]) / 2

            # Calculate Mean
            output['base_happiness_stat']['mean'] = statistics.mean(base_happiness_list)

            # Calculate Average
            output['base_happiness_stat']['average'] = sum(base_happiness_list) / len(base_happiness_list)

        return HttpResponse(json.dumps(output))
    except Exception as e:
        return HttpResponse(e)

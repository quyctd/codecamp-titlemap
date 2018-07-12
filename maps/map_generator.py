import game_object
import json
from addict import Dict
from map_titles.platform import Platform
from map_titles.grass import Grass
from map_titles.spike import Spike
from map_titles.spikefake import SpikeFake

def load_map(json_file_url):
    #1. Load json file -> text
    text = open(json_file_url, 'r').read()
    # print(text)

    #2. Convert text into dictionary
    map_dict = json.loads(text)

    #3. Convert dictionary to object
    map = Dict(map_dict)
    data = map.layers[0].data #list
    width = map.width
    height = map.height

    # data = map_dict['layers'][0]['data']
    # width = map_dict['width']
    # height = map_dict['height']
    return (data, width, height)

def generate_map(json_file_url): #assets/maps/tut_lvl.json
    data, width, height = load_map(json_file_url)

    for index, title in enumerate(data):
        title_x = index % width
        title_y = index // width
        if title == 0:
            pass
        elif title == 1:
            game_object.add(Grass(title_x * 32, title_y * 32))
        elif title == 2:
            game_object.add(SpikeFake(title_x * 32, title_y * 32))
        elif title == 3:
            game_object.add(Spike(title_x * 32, title_y * 32))
        elif title == 4:
            game_object.add(Platform(title_x * 32, title_y * 32))


if __name__ == "__main__":
    generate_map("../assets/maps/map.json")
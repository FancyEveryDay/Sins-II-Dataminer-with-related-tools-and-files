from pathlib import Path
import json

TOP_DICT = Path(__file__).parent.parent.parent.resolve()

with open('.env', 'r') as env:
    SINS_DIRECTORY = Path(json.load(env)['sins2File'])

with open(SINS_DIRECTORY / 'uniforms' / 'planet.uniforms', 'r') as file:
    PLANET_UNIFORMS = json.load(file)

with open(SINS_DIRECTORY / 'localized_text' / 'en.localized_text', 'r') as file:
    LOCALIZED_TEXT = json.load(file)

ENTITIES = SINS_DIRECTORY / 'entities'
UNIFORMS = SINS_DIRECTORY / 'uniforms'

WIKIFILES_DICT = TOP_DICT / 'Strategy Wiki' / 'WikiFiles'

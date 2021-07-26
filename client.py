# deals with communication with PokeAPI
import pokebase as pb
import requests
import io

startingOptions = ['bulbasaur', 1, 'charmander', 4, 'squirtle', 7, 'pikachu', 25, 'eevee', 133, 'chikorita', 152, 'cyndaquil', 155, 'totodile', 158, 'treecko', 252, 'torchic', 255, 'mudkip', 258, 'turtwig', 387, 'chimchar', 390, 'piplup', 393, 'snivy', 495, 'tepig', 498, 'oshawott', 501, 'chespin', 650, 'fennekin', 653, 'froakie', 656, 'rowlet', 722, 'litten', 
725, 'popplio', 728, 'grookey', 810, 'scorbunny', 813, 'sobble', 816]

# input = id or name
def findPokemon(identifier):
    if identifier not in startingOptions:
        return '', None
    mon = pb.pokemon_species(identifier)
    try:
        mon.name
    except requests.exceptions.HTTPError:
        print(f'Caught error in findPokemon() method: {requests.exceptions.HTTPError}')
        return '', None
    if mon.id_ is None or mon.name is None:
        return '', None
    return mon.name.casefold().capitalize(), mon

# input = pokemon_species
def getExpRate(pokemon):
    return [growth.experience for growth in pokemon.growth_rate.levels]

def getBinary(url):
    response = requests.get(url)
    return io.BytesIO(response.content).getvalue()

def getPokemonSpriteBytes(name):
    # not using PokeAPI here because better gif sprite sources
    pixelurl = 'https://play.pokemonshowdown.com/sprites/gen5ani/'
    url = 'https://play.pokemonshowdown.com/sprites/ani/'
    img = f'{name.casefold()}.gif' 
    gen5check = requests.get(pixelurl + img)
    if gen5check.status_code == 200:
        return getBinary(pixelurl + img)
    else:
        print('using Gen 6+ image')
        return getBinary(url + img)


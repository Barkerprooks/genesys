#!/usr/bin/env python3
import random
import string
import math
import json

# useful sources:
# - https://en.wikipedia.org/wiki/Terrestrial_planet
# - https://en.wikipedia.org/wiki/Main_sequence
# - https://en.wikipedia.org/wiki/Binary_star
# - https://nssdc.gsfc.nasa.gov/planetary/factsheet
# - https://en.wikipedia.org/wiki/ROXs_42Bb
# - https://www.pnas.org/doi/10.1073/pnas.1812905116
# - http://exoplanet.eu/diagrams/
# - https://homepage.divms.uiowa.edu/~mbognar/applets/normal.html
# - https://www.daviddarling.info/encyclopedia/M/mass-radius_relation.html
# note: it appears most exo planets a lot of planets are larger than earth by 2 orders of magnitude (in Meaths) 


def random_string(length): # simple name generator for now
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length)) # TODO


def random_digits(length): # generate random digits in string form
    return ''.join(random.choice(string.digits) for _ in range(length)).zfill(length) # zfill for leading zeros


def generate_system():

    # first, we need to know the amount of mass that will be used to create the system
    mass = random.uniform(1e30, 1e31) # give enough material to create a star and then some
    star_mass = mass * 0.9997 # stars take up most of the mass in their system
    star_radius = ((star_mass / 1.989e30) ** 0.8) * 6.957e8 # equation for main seq star radius from mass
    name = random_string(3) # 3 letter random names are pretty classic

    # now we can use a while-loop to dish out the rest of the mass
    objects = [] # create an empty array to store all the stellar objects
    mass -= star_mass # subtract the star mass from the mass our planets will be made of
    while mass > 0: # while we still have usable mass, and have a hard cut at 8 objects
        object_name = f'{name}{random_digits(4)}' # object name is just system name with numbers
        object_mass = (0.1 + (15000 - 0.1) * random.betavariate(0.2, 8)) * 5.9e24 # RNG mass 5.9e24 is AROUND MEarth in kg. using normal distribution
        object_radius = (0.1 + (20 - 0.1) * random.betavariate(2, 2)) * 6.378e6 # RNG radius 6.378e6 is AROUND REarth in meters

        if object_mass > mass: # use up the rest of the mass if it overflows
            object_mass = mass
        
        mass = mass - object_mass # update usable mass

        # 1/1000 chance to mutate by mass and turn into a black hole
        if random.randint(0, 999) == 1:
            object_mass += random.uniform(1e64, 1e65) # add enough ghost mass to make it super dense

        density = object_mass / (0.75 * math.pi * object_radius ** 3) # calculate the density to see what it becomes in kg/m^3 

        object_type = 'Terrestrial'
        if density < 2000:
            object_type = 'Gas Giant'
        elif density > 2e19:
            object_type = 'Black Hole'

        # we are adding a dict to a list
        objects.append({
            'type': object_type,
            'density': density / 1000,
            'mass': object_mass,
            'name': object_name,
            'radius': object_radius
        })

    return name, { 'star': { 'mass': star_mass, 'radius': star_radius }, 'objects': objects }


# generate the whole galaxy
# lets just make a chunk of space, say... 200 x 200 'units' (we can make this bigger)
# each 'unit' can hold one and only one system, otherwise its 'empty'
galaxy_width = 200
galaxy_height = 200
galaxy = {}

print('generating output...')
for y in range(galaxy_height):
    for x in range(galaxy_width):
        # lets say 30% chance to add a system
        if random.randint(0, 100) <= 30:
            name, data = generate_system()
            galaxy[name] = { 'position': (x, y), 'data': data }

# overwrites on subsequent runs
print(json.dumps(galaxy), file=open('system.json', 'wt+'))

for name, system in galaxy.items():

    data = system['data']
    star = data['star']
    objects = data['objects']

    print('system: ', name)
    print('coordinates: (x: %s, y: %s)' % system['position'])
    print(' -   star mass: %0.4Ekg (%0.2f MSun)' % (star['mass'], star['mass'] / 1.9891e30))
    print(' - star radius: %0.4Em  (%0.2f RSun)' % (star['radius'], star['radius'] / 6.957e8))
    print('objects:', len(objects))
    for system_object in objects:
        print('  object:', system_object['name'])
        print('   -    type:', system_object['type'])
        print('   -    mass: %0.4Ekg (%0.2f MEarth)' % (system_object['mass'], system_object['mass'] / 5.9e24))
        print('   -  radius: %0.4Em  (%0.2f REarth)' % (system_object['radius'], system_object['radius'] / 6.378e6))
        print('   - density: %0.4f g/cm^3' % system_object['density'])
    print()

print('number of systems:', len(galaxy))
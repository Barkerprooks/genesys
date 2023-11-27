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
# - https://homepage.divms.uiowa.edu/~mbognar/applets/normal.html
# - https://www.daviddarling.info/encyclopedia/M/mass-radius_relation.html
# - https://www.livescience.com/do-gaseous-moons-exist
# note: it appears most exo planets a lot of planets are larger than earth by 2 orders of magnitude (in Meaths) 


# - http://exoplanet.eu/diagrams/


G = 6.674e-11
MEARTH_UNIT = 5.9e24
REARTH_UNIT = 6.378e6


def random_string(length, exists): # simple name generator for now
    rng = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
    if rng in exists:
        return random_digits(length, exists)
    exists.add(rng)
    return rng


def random_digits(length, exists): # generate random digits in string form
    rng = ''.join(random.choice(string.digits) for _ in range(length)).zfill(length) # zfill for leading zeros
    if rng in exists:
        return random_digits(length, exists)
    exists.add(rng)
    return rng

# convert one dimensional array index into a two dimensional array index
# imagine an array [0, 1, 2, 3, 4, 5]
# if it was converted into a 2d array with a width of 3 it would be:
# [[0, 1, 2],
#  [3, 4, 5]] you can think of this form like a grid, with the y values
# starting at the top, and growing towards the bottom. and x values that
# start on the left and grow towards the right.

# this function basically maps what the index in a 1D array would be in the 2D grid
def into_2d(i, width):
    # x is modulo width because it requires the repeating sequence of values up to the width
    # for each set of x values, there is one y value in this relationship (like an actual graph)
    # therefore we just need the closest floor rounded integer of how many times greater than
    # the width the y value is.
    return int(i % width), int(i // width) # duh!


# normalize parameter will renomralize RNG based on a passed in value (simply multiplies it by that value)
def rng(low, high, alpha, beta, normalize=None):
    return (low + (high - low) * random.betavariate(alpha, beta)) * (1 if normalize is None else normalize)


def generate_object(usable_mass):
        mass = rng(0.0001, 18000, 0.2, 10, normalize=MEARTH_UNIT) # range of 0.0001 to 18000 times earth
        radius = rng(0.01, 21, 2, 5, normalize=REARTH_UNIT) # range of 0.5 to 20 times earth
        density = mass / (0.75 * math.pi * radius ** 3) # calculate the density to see what it becomes in kg/m^3 
        return { # return a dict of the object
            'mass': mass if mass < usable_mass else usable_mass, # dont go over that usable mass
            'type': 'Terrestrial' if density > 1800 else 'Black Hole' if density > 2e19 else 'Gas Giant',
            'radius': radius,
            'density': density / 1000 # g/cm^2
        }


def generate_system(x, y, name):
    usable_mass = random.uniform(1e30, 1e31) # give enough material to create a star and then some
    core_mass = usable_mass * (0.997 + random.uniform(0.0001, 0.0009))
    star = { 'mass': core_mass, 'radius': ((core_mass / 1.989e30) ** 0.8) * 6.957e8 } # calculate radius of star from mass

    usable_mass -= core_mass # subtract the star mass from the mass our planets will be made of
    object_ids = set()
    objects = {} # create an empty array to store all the stellar objects
    while usable_mass > 0: # use up the remaining mass
        object_id = random_digits(4, object_ids) # 4 digit UNIQUE random number for the object created
        objects[object_id] = generate_object(usable_mass)
        usable_mass -= objects[object_id]['mass'] # update usable mass

    distance = rng(7000000, 90000000, 2, 8) # start from minimum of PROXIMA CENTAURI B to max of earth distance
    orbit_ids = list(objects.keys())
    orbits = { orbit_ids[0]: [] }
    objects[orbit_ids[0]]['distance'] = distance

    last_object_index = 0
    for i in range(1, len(orbit_ids)):

        last_object_id = orbit_ids[last_object_index]
        last_object = objects[last_object_id]

        distance += rng(200000, 1000000, 0.5, 0.5)

        object_id = orbit_ids[i]

        g_star = G * (objects[object_id]['mass'] * core_mass) / distance ** 2
        g_last = G * (objects[object_id]['mass'] * last_object['mass']) / (distance - last_object['distance']) ** 2

        if g_last > g_star and objects[object_id]['mass'] < last_object['mass']:
            objects[object_id]['distance'] = distance - last_object['distance']
            orbits[last_object_id].append(object_id)
        else:
            objects[object_id]['distance'] = distance
            orbits[object_id] = []
            last_object_index = i

    return { 'name': name, 'coordinates': (x, y), 'star': star, 'objects': objects, 'orbits': orbits }


def random_spiral(diameter, phi):
    # https://arxiv.org/ftp/arxiv/papers/0908/0908.0892.pdf
    # scroll to the very bottom of the doc to see the magic equation
    radius = random.uniform(0, diameter // 2)
    angle = random.uniform(0, 2 * math.pi)
    return angle, (radius / (1 - (phi*math.tan(phi))*math.log(angle/phi))) # pg. 13, A11


def generate_galaxy(stars, diameter, sigma):
    system_coordinates = set()
    system_names = set()
    galaxy = []
    
    for _ in range(stars):
        
        angle, radius = random_spiral(diameter, sigma)

        # map star by decomposing polar coordinates (angle, radius) into linear (x, y)
        x1, y1 = (math.cos(angle) * radius), (math.sin(angle) * radius)

        # create a mirror star with a little offset
        offset_x = random.uniform(math.pi - 0.02, math.pi + 0.02)
        offset_y = random.uniform(math.pi - 0.02, math.pi + 0.02)
        x2, y2 = (math.cos(angle + offset_x) * radius), (math.sin(angle + offset_y) * radius)

        if (x1, y1) not in system_coordinates:
            system_coordinates.add((x1, y1))
            galaxy.append(generate_system(x1, y1, random_string(5, system_names)))
        
        if (x2, y2) not in system_coordinates:
            system_coordinates.add((x2, y2))
            galaxy.append(generate_system(x2, y2, random_string(5, system_names)))

    return json.dumps(galaxy)
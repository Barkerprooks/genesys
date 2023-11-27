# Genesys

## changes
- output is now named `galaxy.json`, this makes more sense
- orbits lists now included
- changed some key names around, and object list is now a dict
- added distance key that represents the distance from the parent orbit


Run the generator and view the output
```
python3 ./src/genesys.py
```
this will output a file named `system.json` with all the system info
```
"""A helper file to load presets for display paramaters.
"""

import json

OBJECT_MAP = ['earth', 'sun', 'moon', 'barycenter']
SIZE_MAP = ["small", "large"]

def preset(path: str):
	with open(f"presets/{path}.json") as f:
		dat = json.load(f)
		dat['center'] = OBJECT_MAP.index(dat['center'])
		dat['ndims'] = 2 if dat['mode'] == 'polar' else len(list(filter(lambda x:x, dat['dims'])))

		if 'dims' in dat:
			dat['dims']  = {k: SIZE_MAP.index(dim) for k, dim in zip(['x', 'y', 'z'], dat['dims']) if dim}

		return dat

if __name__ == "__main__":
	print(preset("moon-pov"))
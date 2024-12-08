"""A helper file to load presets for display paramaters.
"""

import json

OBJECT_MAP = ['earth', 'sun', 'moon', 'barycenter']
SIZE_MAP = ["small", "large"]

def preset(path: str):
	with open(f"presets/{path}.json") as f:
		dat = json.load(f)
		dat['center'] = OBJECT_MAP.index(dat['center'])
		dat['ndims'] = len(list(filter(lambda x:x, dat['dims'])))

		temp = {k: SIZE_MAP.index(dim) for k, dim in zip(['x', 'y', 'z'], dat['dims']) if dim}
		# for n, dim in zip(['x', 'y', 'z'], dat['dims']):
		# 	if dim:
		# 		temp.append(SIZE_MAP.index(dim)) 
		
		dat['dims'] = temp
		
		return dat

if __name__ == "__main__":
	print(preset("earth-moon-xy"))
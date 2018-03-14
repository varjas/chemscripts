import os
import json
from uncertainties import ufloat


def main():
	filesToProcess = set()
	paths = os.listdir('.')
	for p in paths:
		if os.path.isfile(p) and p.endswith('.json'):
			filesToProcess.add(p)

	for file in filesToProcess:
		# Open input file
		inputFile = open(file, 'r')

		# Copy lines of input file to variable
		lines = inputFile.readlines()

		# Close input file
		inputFile.close()

		# Output data
		output = {}

		for line in lines:
			data = json.loads(line)
			for key in data:
				if type(data[key]) is dict:
					output[key] = {}
					for measurementKey in list(data[key].keys()):
						value = data[key][measurementKey]
						if len(value) > 1:
							output[key][measurementKey] = ufloat(value[0], value[1])
						else:
							output[key][measurementKey] = ufloat(value[0])
				else:
					output[key] = data[key]

		# dataName = input('Data name (identifer): ')

		# output = {dataName: output}
		print(file.rstrip('json'))
		print(output)


if __name__ == '__main__':
	main()

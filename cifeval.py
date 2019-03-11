'''
Functions for analyzing metrical parameters directly from cif files
Christopher Varjas (March 2018)
'''
import os
import re
import tau
import json
from uncertainties import ufloat
from pprint import pprint
import decimal
from types import SimpleNamespace


def find(molecule, keywords, programmatic=False):
	output = {}
	# Iterate through molecule
	# Set bonds, angles, torsions that match keywords to output
	# {k: v for (k, v) in molecule.items() if 'N2 Mo1 N1' in k}

	if programmatic is False:
		pprint(output)
		return
	else:
		return output


def processFile(filename, focus, programmatic=False, dotSyntax=False):
	# Open input file
	inputFile = open(filename, 'r')

	# Copy lines of input file to variable
	lines = inputFile.readlines()

	# Clost input file
	inputFile.close()

	# Read section
	saveLine = False

	# Track section type
	section = ''

	lineCondense = re.compile('^(.*\d\)?)')
	textSelect = re.compile('(.*) -?\d.*')
	numberSelect = re.compile('.* (-?\d.*)')
	centralAtom = re.compile('^\w+\s(' + focus + ').*')
	angles = []
	data = {}

	for line in lines:
		if '_geom_bond' in line or '_geom_angle' in line or '_geom_torsion' in line:
			saveLine = True
		elif saveLine is True:
			# Deactivate saving if a blank line is reached
			if line.isspace():
				saveLine = False
		elif saveLine is False:
			# If later sections of the file are reached, stop processing
			if 'TITL' in line:
				break
		if '_geom_bond' in line:
			data['bond'] = {}
			section = 'bond'
		elif '_geom_angle' in line:
			data['angle'] = {}
			data['tau'] = None
			section = 'angle'
		elif '_geom_torsion' in line:
			data['torsion'] = {}
			section = 'torsion'
		if saveLine is True:
			if focus in line:
				condensed = lineCondense.match(line)
				number = numberSelect.match(condensed[1])[1]
				number = number.split('(')
				if len(number) > 1:
					number[1] = int(number[1].rstrip(')'))
					number[1] = number[1] * pow(10, decimal.Decimal(str(number[0])).as_tuple().exponent)
				number[0] = float(number[0])
				if section == 'angle':
					# Include angle if the target atom is centered
					if centralAtom.match(condensed[1]):
						angles.append(float(number[0]))
				if programmatic is True:
					print(number)
					if len(number) > 1:
						data[section][textSelect.match(condensed[1])[1]] = ufloat(number[0], number[1])
					else:
						data[section][textSelect.match(condensed[1])[1]] = number[0]
				else:
					data[section][textSelect.match(condensed[1])[1]] = number

	data['tau'] = tau.tau(angles)
	if dotSyntax is True:
		data = SimpleNamespace(**data)
	print(pprint(data))
	return data


# def compare(category, data, mol1, mol2):
def compare(category, mol1, mol2):
	data = main(True)
	print(mol1 + ' - ' + mol2)
	for angle in data[mol1][category]:
		print(angle)
		try:
			print(data[mol1][category][angle] - data[mol2][category][angle])
		except Exception:
			pass
		print('')


def saveFile(filename, data, fileType=['json', 'txt']):

	if 'txt' in fileType:
		outputNameTXT = filename.replace('.cif', 'Metrics.txt')
		outputFileTXT = open(outputNameTXT, 'w')
		for key in data:
			outputFileTXT.write(str(key) + '\n')
			if type(data[key]) is dict:
				for elementKey in list(data[key].keys()):
					measurement = data[key][elementKey]
					combinedNumber = str(measurement[0])
					if len(measurement) > 1:
						combinedNumber += '(' + str(measurement[1]) + ')'
					outputFileTXT.write(str(elementKey + '\t' + combinedNumber) + '\n')
			else:
				outputFileTXT.write(str(data[key]) + '\n')
		outputFileTXT.close()

	if 'json' in fileType:
		outputNameJSON = filename.replace('.cif', 'Metrics.json')
		# Open output file for writing
		outputFileJSON = open(outputNameJSON, 'w')
		outputFileJSON.write(json.dumps(data))
		outputFileJSON.close()


def main(programmatic=False, dotSyntax=False):
	# Prompt user for input file name
	inputFileName = input('Input file name with extension (.cif) or (ALL): ')
	inputAtomFocus = input('Input central atom for focus (Mo1): ')

	if inputFileName.lower() in ['', 'all']:
		filesToProcess = set()
		paths = os.listdir('.')
		for p in paths:
			if os.path.isfile(p) and p.endswith('.cif'):
				filesToProcess.add(p)

		allData = {}

		for file in filesToProcess:
			# Process file
			data = processFile(file, inputAtomFocus, programmatic, dotSyntax)
			allData[file.rstrip('.cif')] = data

		if programmatic is True:
			if dotSyntax is True:
				allData = SimpleNamespace(**allData)
			return allData
		else:
			# Save combined file
			saveFile('consolidated.cif', allData, ['json'])

	elif inputFileName.lower().endswith('.cif') is False:
		print('Incorrect file extension')
	else:
		# Process file
		data = processFile(inputFileName, inputAtomFocus)
		# Save file
		saveFile(inputFileName, data)


if __name__ == '__main__':
	main()

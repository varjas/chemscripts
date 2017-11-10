# A CLI program to find and output metrical parameters from a cif file.
# Bond distances, bond angles, and torsion angles will be saved to a text or csv file.
# Christopher Varjas (April 2017)

# Prompt user for input file name
inputFileName = input('Input file name with extension (.cif): ')

if inputFileName.lower().endswith('.cif') is False:
	print('Incorrect file extension')
else:
	# Open input file
	inputFile = open(inputFileName, 'r')

	# Copy lines of input file to variable
	lines = inputFile.readlines()

	# Clost input file
	inputFile.close()

	# Prompt user for output file type
	outputFileType = input('Output file type (txt/csv): ')

	# Generate output name based on input file name
	if outputFileType == 'csv':
		outputFileName = inputFileName.replace('.cif', 'Metrics.csv')
	else:
		outputFileName = inputFileName.replace('.cif', 'Metrics.txt')

	# Open output file for writing
	outputFile = open(outputFileName, 'w')

	# Variable for tracking whether lines should be saved
	saveLine = False

	# Variable for tracking if the header has been saved
	saveHeader = False

	# Combined header line variable
	headerLine = ''

	# Go through lines individually
	for line in lines:
		# Active saving if in the correct section of the file
		if '_geom_bond' in line or '_geom_angle' in line or '_geom_torsion' in line:
			saveLine = True
			if outputFileType == 'csv':
				saveHeader = True
				headerLine += line.strip() + ','
				continue

		elif saveLine is True:
			# Deactivate saving if a blank line is reached
			if line.isspace():
				saveLine = False

		elif saveLine is False:
			# If later sections of the file are reached, stop processing
			if 'TITL' in line:
				break

		if outputFileType == 'csv' and saveHeader is True:
			outputFile.write(headerLine[:-1] + '\n')
			saveHeader = False
			headerLine = ''

		# If located in the correct section of a file
		if saveLine is True:
			if outputFileType == 'csv':
				outputFile.write(line.lstrip().replace(' ', ','))
			else:
				outputFile.write(line.lstrip())

	outputFile.close()
	print('Metrics saved to: ', outputFileName)

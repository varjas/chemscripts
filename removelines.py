# A CLI program to remove lines from a file and save the result as a new file.
# The text used to filter out specific lines is user defined.
# Christopher Varjas (May 2016)

# Prompt user for input file name
inputFileName = input('The input file name with extension: ')

# Open input file
inputFile = open(inputFileName, 'r')

# Copy lines of input file to variable
lines = inputFile.readlines()

# Clost input file
inputFile.close()

# Prompt user for identifying text for line removal
filterText = input('Identifying text for lines to be removed: ')

# Prompt user for output file name
outputFileName = input('The output file name with extension: ')

# Open output file for writing
outputFile = open(outputFileName, 'w')

# Set line monitoring variables
linesWritten = 0

# Go through lines individually
for line in lines:
	# Search for the absence of the string in the line
	if filterText not in line:
		# Increase sum of lines written
		linesWritten += 1
		# If the line does not contain the string, write it to output file
		outputFile.write(line)

outputFile.close()
print('Lines added: ', linesWritten)
print('Out of: ', len(lines))

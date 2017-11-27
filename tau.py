# Functions for calculating tau parameters from coordination angles
# The functions can be used directly for calculations or the combined 'tau' function can be used
# Christopher Varjas (November 2017)
import math

theta = math.degrees(math.acos(-1 / 3))
# theta = 109.5

def tau5(b, a):
	return (b - a) / 60

def tau4(b, a):
	return (360 - (a + b)) / (360 - (2 * theta))

def tau4prime(b, a):
	return ((b - a) / (360 - theta)) + ((180 - b) / (180 - theta))

# Angles expects a list
# If all angles are defined, the correct tau 4 or 5 function will be selected
# Or the number of ligands can be defined with the second parameter as an integer with only a few angles included in the list
def tau(angles, ligands=None):
	# Sort angles that were input
	angles.sort(reverse=True)
	# If ligands is defined, use the appropriate function
	if ligands == 5:
		return tau5(angles[0], angles[1])
	elif ligands == 4:
		return tau4prime(angles[0], angles[1])

	# If ligand count was not defined, try to determine if all angles are defined
	if len(angles) == 10:
		return tau5(angles[0], angles[1])
	elif len(angles) == 6:
		return tau4prime(angles[0], angles[1])
	else:
		print('Need to define all complex angles, or set the calculation type to 4 or 5')
		return False

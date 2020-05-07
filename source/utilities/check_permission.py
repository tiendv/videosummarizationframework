import os
import argparse
def check_permission_to_write(outdir):
	"""[This function to check permission to write file before save file]
    Arguments:
        outdir {string} -- [Output directory of the file to write]
    Returns:
        [BOOLEAN] -- [True - if can write]
    Author: thinhplg - 20/04/2020
    """
    
	path = os.path.join(outdir,'check.txt')
	print('Checking permission to write file at path: %s'%(outdir))
	with open(path,'w') as file:
		file.write('checked')
		file.close()
	if (os.path.isfile(path)) is True:
		os.remove(path)
		print('\tCHECK STATUS: True (can write file).')
		return True
	else:
		print('\tCHECK STATUS: Faile (check your directory again.')
		return False

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('outdir',
					help='Path to check')
	args = parser.parse_args()
	check_permission_to_write(args.outdir)

if __name__ == '__main__':
    main()
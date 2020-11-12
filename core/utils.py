import os

def get_files_from_directory(directory) :
	files = os.listdir(directory)
	fileNum = len(fileSet)
	return files, fileNum


import os

def get_fileList_from_directory(dirPath) :
	fileList = os.listdir(dirPath)
	return fileList

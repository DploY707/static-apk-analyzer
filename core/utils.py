import os

def get_fileList_from_directory(dirPath) :
	fileList = os.listdir(dirPath)
	fileNum = len(fileList)
	return fileList, fileNum

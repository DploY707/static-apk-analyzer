import os, subprocess

def get_fileList_in_directory(dirPath) :
	return os.listdir(dirPath)

def get_leafNodes(dirPath) :
	subDirList = get_subDirectoryList_in_directory(dirPath)
	leafNodeList = list()

	for subDir in subDirList :

		if is_leaf(subDir) :
			leafNodeList.append(subDir)

	return leafNodeList

def get_subDirectoryList_in_directory(dirPath) :
	findSubDir = subprocess.check_output("find " + dirPath + " -type d 2>/dev/null", shell=True)
	resultStr = translate_subprocess_output_to_str(findSubDir)
	subDirList = trim_newLines(resultStr)[:-1]

	return subDirList

def generate_directories_to_endpoint(endpointPath) :
	if not is_path_exists(endpointPath) :
		os.makedirs(endpointPath)

def replace_string_in_list(targetList, srcStr, destStr) :
	replacedList = list()

	for target in targetList :
		replacedList.append(target.replace(srcStr, destStr))

	return replacedList

def translate_subprocess_output_to_str(outputByte) :
	resultStr = str(outputByte)
	resultStr = trim_quotation_marks(resultStr)[1]

	return resultStr

def trim_quotation_marks(inputStr) :
	return inputStr.split("'")

def trim_newLines(inputStr) :
	return inputStr.split("\\n")

def is_leaf(filePath):
	subFileList = get_fileList_in_directory(filePath)

	for subFile in subFileList :
		subFilePath = filePath + '/' + subFile

		if is_directory(subFilePath) :
			return False

	return True

def is_directory(targetPath) :
	return os.path.isdir(targetPath)

def is_path_exists(path) :
	return os.path.exists(path)

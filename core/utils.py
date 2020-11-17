import os, subprocess

def get_fileList_in_directory(dirPath) :
	return os.listdir(dirPath)

def get_leafNodes_in_directory(dirPath) :
	findSubDir = subprocess.check_output("find " + dirPath + " -type d 2>/dev/null", shell=True)
	resultStr = translate_subprocess_output_to_str(findSubDir)
	resultPathList = trim_newLines(resultStr)[:-1]

	return resultPathList

def translate_subprocess_output_to_str(outputByte) :
	resultStr = str(outputByte)
	resultStr = trim_quotation_marks(resultStr)[1]

	return resultStr

def trim_quotation_marks(inputStr) :
	return inputStr.split("'")

def trim_newLines(inputStr) :
	return inputStr.split("\\n")


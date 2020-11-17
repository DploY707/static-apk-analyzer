import sys, os, pickle
from code_extractor import CodeExtractor
from utils import DirStruct

DATASET_ROOT_PATH = '/root/workDir/data'
RESULT_ROOT_PATH = '/root/results/methodLists'

def print_analyzing_status(index, dataSetSize, dataSetDir, targetAPK) :
	print('\033[92m[' + str(index+1) + ' / ' + str(dataSetSize) + ']\033[0m' + ' in "' + dataSetDir + '" Analyzing......  "' + targetAPK + '"')

def print_progress_directories(index, totalDirList) :
	print('\n\033[92m[' + totalDirList[index] + ']\033[0m' +' in ' + str(totalDirList))

def save_methodList(resultPath, methodInfoList) :
	methodList = open(resultPath, 'wb')
	pickle.dump(methodInfoList, methodList)
	methodList.close()

def generate_methodLists_from_dataSet(dataDir, resultDir) :
	dataSet = os.listdir(dataDir)
	apkNum = len(dataSet)

	for i in range(0, apkNum) :
		print_analyzing_status(i, apkNum, dataDir, dataSet[i])

		APKFilePath = dataDir + '/' + dataSet[i]
		resultFilePath = resultDir + '/' + str(i) + '_' + dataSet[i]

		ce = CodeExtractor(APKFilePath)

		save_methodList(resultFilePath, ce.get_methodInfoList())

	print('Complete analyzing for ' + str(apkNum) + ' apks :)')

def generate_directories_to_endpoint(endpointPath) :
	if not is_path_exists(endpointPath) :
		os.makedirs(endpointPath)

def is_path_exists(path) :
	return os.path.exists(path)

def replace_string_in_list(targetList, srcStr, destStr) :
	replacedList = list()

	for target in targetList :
		replacedList.append(target.replace(srcStr, destStr))

	return replacedList

if __name__ == '__main__' :
	ds = DirStruct(DATASET_ROOT_PATH)
	dataDirAllList = ds.get_all_subDirectory()
	dataDirList = ds.get_directoryList_include_file(dataDirAllList)
	resultDirAllList = replace_string_in_list(dataDirAllList, DATASET_ROOT_PATH, RESULT_ROOT_PATH)
	resultDirList = replace_string_in_list(dataDirList, DATASET_ROOT_PATH, RESULT_ROOT_PATH)

	for resultDir in resultDirAllList :
		generate_directories_to_endpoint(resultDir)



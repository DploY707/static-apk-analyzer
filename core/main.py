import sys, os, pickle, utils
from code_extractor import CodeExtractor

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

if __name__ == '__main__' :
	datasetDirList = utils.get_leafNodes_in_directory(DATASET_ROOT_PATH)
	resultDirList = utils.replace_string_in_list(datasetDirList, DATASET_ROOT_PATH, RESULT_ROOT_PATH)

	for resultDir in resultDirList :
		utils.generate_directories_to_endpoint(resultDir)

	for i in range(len(datasetDirList)) :
		print_progress_directories(i, datasetDirList)
		generate_methodLists_from_dataSet(datasetDirList[i], resultDirList[i])

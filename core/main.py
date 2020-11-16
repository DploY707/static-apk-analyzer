import sys, os, pickle
from code_extractor import CodeExtractor
from utils import DirStruct

DATASET_ROOT_PATH = '/root/workDir/data'
RESULT_ROOT_PATH = '/root/results/methodLists'

def print_analyzing_status(index, dataSetSize, dataSetDir, targetAPK) :
	print('[' + str(index+1) + ' / ' + str(dataSetSize) + '] in "' + dataSetDir + '" Analyzing......  "' + targetAPK + '"')

def print_progress_directories(index, totalDirList) :
	print('\n[' + totalDirList[index] + '] in ' + str(totalDirList))

def save_methodList(resultPath, methodInfoList) :
	methodList = open(resultPath, 'wb')
	pickle.dump(methodInfoList, methodList)
	methodList.close()

def generate_methodLists_from_dataSet(dataDir, resultDir) :
    dataSet = get_only_files_in_directory(dataDir)
    apkNum = len(dataSet)

    for i in range(0, apkNum) :
        print_analyzing_status(i, apkNum, dataDir, dataSet[i])

        APKFilePath = dataDir + '/' + dataSet[i]
        resultFilePath = resultDir + '/' + str(i) + '_' + dataSet[i]

        ce = CodeExtractor(APKFilePath)

        if not is_savable_path(resultDir):
            generate_midPoint_directory_to_endpoint(resultDir)

        save_methodList(resultFilePath, ce.get_methodInfoList())

    print('Complete analyzing for ' + str(apkNum) + ' apks :)')

def is_savable_path(filePath) :
    return os.path.exists(filePath)

def generate_midPoint_directory_to_endpoint(endpointPath) :
    os.makedirs(endpointPath)

def get_only_files_in_directory(dirPath) :
	fileList = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
	return fileList

def preprocess_directory_path(dataRootPath, resultRootPath) :
	ds = DirStruct(dataRootPath)
	dataDirPathList = ds.get_directory_include_file(ds.get_directory_hierarchy())

	resultDirPathList = replace_string_in_list(dataDirPathList, dataRootPath, resultRootPath)

	return dataDirPathList, resultDirPathList

def replace_string_in_list(targetList, srcStr, destStr) :
	replacedList = list()

	for target in targetList :
		replacedList.append(target.replace(srcStr, destStr))

	return replacedList

if __name__ == '__main__' :
	dataSetPathList, resultPathList = preprocess_directory_path(DATASET_ROOT_PATH, RESULT_ROOT_PATH)

	for i in range(len(dataSetPathList)) :
		print_progress_directories(i, dataSetPathList)
		generate_methodLists_from_dataSet(dataSetPathList[i], resultPathList[i])



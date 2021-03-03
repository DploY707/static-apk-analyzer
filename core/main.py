import os
import pickle
import utils
from code_extractor import CodeExtractor

DATASET_ROOT_PATH = '/root/workDir/data'
RESULT_ROOT_PATH = '/root/result'

def print_analyzing_status(index, dataSetSize, dataSetDir, targetAPK) :
    print(utils.set_string_colored('[' + str(index+1) + ' / ' + str(dataSetSize) + ']', utils.Color.GREEN.value) + ' in "' + dataSetDir + '" Analyzing......  "' + targetAPK + '"')

def print_progress_directories(index, totalDirList) :
    print('\n' + utils.set_string_colored('[' + totalDirList[index] + ']', utils.Color.GREEN.value) + ' in ' + str(totalDirList))

def print_count_completed_apk(apkNum) :
    print('Complete analyzing for ' + str(apkNum) + ' apks :)')

def save_result(resultPath, data) :
    result = open(resultPath, 'wb')
    pickle.dump(data, result)
    result.close()

def generate_methodLists_from_dataSet(dataDir, resultDir) :
    dataSet = os.listdir(dataDir)
    apkNum = len(dataSet)
    
    for i in range(0, apkNum) :
        print_analyzing_status(i, apkNum, dataDir, dataSet[i])
        
        APKFilePath = dataDir + '/' + dataSet[i]
        resultFilePath_methodList = resultDir + '/methodInfo/' + str(i) + '_' + dataSet[i] + '_byte_method.pickle'
        resultFilePath_referenceList = resultDir + '/referenceInfo/' + str(i) + '_' + dataSet[i] + '_byte_call.pickle'
        
        ce = CodeExtractor(APKFilePath)
        
        save_result(resultFilePath_methodList, ce.get_methodInfoList())
        save_result(resultFilePath_referenceList, ce.get_referenceInfoList())
        
    print_count_completed_apk(apkNum)
    
if __name__ == '__main__' :
    datasetDirList = utils.get_endpointDirList(DATASET_ROOT_PATH)
    resultDirList = utils.replace_string_in_list(datasetDirList, DATASET_ROOT_PATH, RESULT_ROOT_PATH)
    
    for resultDir in resultDirList :
        utils.generate_directories_to_endpoint(resultDir)
        
        for i in range(len(datasetDirList)) :
            print_progress_directories(i, datasetDirList)
            generate_methodLists_from_dataSet(datasetDirList[i], resultDirList[i])


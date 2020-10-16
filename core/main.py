import sys, os
from code_extractor import parse_methods_from_APK
from code_extractor import generate_methodList

APK_SET_PATH = '/root/workDir/data'
RESULT_PATH = '/root/results/methodLists'

def print_analyzing_status(index, dataSetSize, targetAPK) :
    print('[' + str(index+1) + ' / ' + str(dataSetSize) + ']' +  ' Analyzing......  ' + targetAPK)

def save_methodList(resultPath, contents) :
    methodList = open(resultPath, 'w')
    methodList.write(contents)
    methodList.close()

def generate_methodLists_from_dataSet(dataDir, resultDir) :
    dataSet = os.listdir(dataDir)
    apkNum = len(dataSet)

    for i in range(0, apkNum) :
        print_analyzing_status(i, apkNum, dataSet[i])

        APKFilePath = dataDir + '/' + dataSet[i]
        resultFilePath = resultDir + '/' + str(i) + '_' + dataSet[i]

        #TODO : modify code for readability (easy to read)
        save_methodList(resultFilePath, generate_methodList(parse_methods_from_APK(APKFilePath)))

    print('Complete analyzing for ' + str(apkNum) + ' apks :)')

if __name__ == '__main__' :
    generate_methodLists_from_dataSet(APK_SET_PATH, RESULT_PATH)

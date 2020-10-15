from code_extractor import parse_methodList_from_APK
import sys, os

APK_SET_PATH = '/root/workDir/data'
RESULT_PATH = '/root/results/methodLists'

def generate_methodLists_from_dataSet(dataDir, resultDir) :
    dataSet = os.listdir(dataDir)
    apkNum = len(dataSet)

    for i in range(0, apkNum) :
        print('[' + str(i+1) + ' / ' + str(apkNum) + ']' +  ' Analyzing......  ' + dataSet[i])
        parse_methodList_from_APK(dataSet[i], dataDir, resultDir)

    print('Complete analyzing for ' + str(apkNum) + ' apks :)')

if __name__ == '__main__' :
    generate_methodLists_from_dataSet(APK_SET_PATH, RESULT_PATH)

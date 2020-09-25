from cg_parser import parse_call_reference
from cg_parser import concat_call_chain
from cg_parser import convert_id_to_apiName
from itf_androguard import androcg
import sys, os

APK_SET_PATH = '/root/workDir/data'
GML_RESULTS_PATH = '/root/results/cg'
REF_RESULTS_PATH = '/root/results/ref'

def generate_cf_gmls(dataDir, resultDir) :
    dataSet = os.listdir(dataDir)
    apkNum = len(dataSet)

    for i in range(0, apkNum) :
        print('[' + str(i+1) + ' / ' + str(apkNum) + ']' +  ' Analyzing......  ' + dataSet[i])
        androcg(dataSet[i], dataDir, resultDir)

    print('Complete analyzing for ' + str(apkNum) + ' apks :)')

def generate_call_references(dataDir, resultsDir) :
    dataSet = os.listdir(dataDir)
    gmlNum = len(dataSet)

    for i in range(0, gmlNum) :
        print('[' + str(i+1) + '/' + str(gmlNum) + ']' + ' Generate References...... ' + dataSet[i])
        parse_call_reference(dataSet[i], resultsDir)

    print('Complete Generating References for ' + str(gmlNum) + ' apks :)')

if __name__ == '__main__' :
    generate_cf_gmls(APK_SET_PATH, GML_RESULTS_PATH)
    generate_call_references(GML_RESULTS_PATH, REF_RESULTS_PATH)

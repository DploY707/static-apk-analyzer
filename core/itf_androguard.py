import os

def androcg(targetAPK, dataPath, resultPath) :
    os.system('androcg ' + dataPath + '/' + targetAPK + ' -o ' + resultPath + '/' + targetAPK.split('.apk')[0] + '.gml')

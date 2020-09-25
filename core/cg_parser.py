import os

def save_result_file(filePath, contents) :
    file = open(filePath, 'w')
    file.write(contents)
    file.close()

def parse_call_reference(gmlDir, gmlName, resultPath) :
    file = open(gmlDir + '/' + gmlName, 'r')

    for line in file.readlines() :
        if 'id ' in line :
            print(line)
        elif 'label ' in line :
            print(line)
        elif 'entrypoint ' in line :
            print(line)

    save_result_file(resultPath + '/' + gmlName.split('.')[0] + '.ref', 'something\n')
    print('parse_call_reference')

def concat_call_chain() :
    print('concat_call_chain')

def convert_id_to_apiName() :
    print('convert_id_to_apiName')    print('convert_id_to_apiName')

import os
from collections import OrderedDict
from androguard.core.bytecodes.apk import APK as openAPK
from androguard.core.bytecodes.dvm import DalvikVMFormat as getDEX
from androguard.core.analysis.analysis import Analysis as an

def method_info_to_dict(className, methodName, metaInfo, accessFlags, methodIndex, codeSize, instructions) :
    methodDict = OrderedDict()

    methodDict['className'] = str(className)
    methodDict['methodName'] = str(methodName)
    methodDict['returnType'] = metaInfo['return']
    methodDict['registers'] = metaInfo['registers']
    methodDict['paramList'] = metaInfo['params']
    methodDict['accessFlagList'] = accessFlags.split(' ')
    methodDict['methodIndex'] = methodIndex
    methodDict['codeSize'] = codeSize
    methodDict['instructions'] = instructions

    return methodDict

def optimize_instruction_format(inst) :
    if '-payload' not in inst :
        instChars = list(inst)

        splited = False

        optimized = ''

        for i in range(len(instChars)) :
            if not splited and str(instChars[i]).isspace() and str(instChars[i+1]).isspace() :
                optimized += '||'
                splited = True
            else :
                optimized += instChars[i]

        optimized = (
                optimized
                .replace(' ', '')
                .replace(',', ', ')
                .split('||')
                )

        dictInst = OrderedDict()

        dictInst['bytecode'] = optimized[0]
        dictInst['smali'] = optimized[1]

        return dictInst

    else :
        return inst

def get_instructions_from_method(method) :
    instructions = list()

    for n, inst in enumerate(method.get_instructions()) :
        instructions.append(optimize_instruction_format(inst.disasm()))

    return instructions

def parse_methods_from_APK(targetAPK) :
    apk = openAPK(targetAPK)
    dex = getDEX(apk.get_dex())
    methods = dex.get_methods()

    return methods

def list_to_string_with_newline(listData) :
    return '\n'.join(listData)

def make_method_meta_info_inform(metaInfo) :
    metaInfoDict = OrderedDict()
    registerDict = OrderedDict()

    if bool(metaInfo) :
        metaInfoDict['return'] = str(metaInfo['return'])

        if (-1) in metaInfo['registers'] :
            metaInfoDict['registers'] = ''
        else :
            registerDict['begin'] = metaInfo['registers'][0]
            registerDict['size'] = metaInfo['registers'][1] - metaInfo['registers'][0] + 1
            metaInfoDict['registers'] = registerDict

        metaInfoDict['params'] = list()  # Params is a tuple-list

        if len(metaInfo) == 2 :
            pass
        elif len(metaInfo) == 3 :
            for regNum, dataType in metaInfo['params'] :
                metaInfoDict['params'].append((regNum, str(dataType))) # Params is a tuple list
        else :
            print('meta info error')

    else :
        metaInfoDict['return'] = ''
        metaInfoDict['registers'] = ''
        metaInfoDict['params'] = list()

    return metaInfoDict

def generate_methodList(methods) :
    methodInfoList = list()

    for method in methods :
        methodInfoList.append(method_info_to_dict(
            method.get_class_name(),
            method.get_name(),
            make_method_meta_info_inform(method.get_information()),
            method.get_access_flags_string(),
            method.get_method_idx(),
            method.get_length(),
            get_instructions_from_method(method)
            ))

    print('Parse Method Lists from APK')

    return methodInfoList

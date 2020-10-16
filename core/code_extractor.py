import os
from collections import OrderedDict
from androguard.core.bytecodes.apk import APK as openAPK
from androguard.core.bytecodes.dvm import DalvikVMFormat as getDEX
from androguard.core.analysis.analysis import Analysis as an

def method_info_to_dict(className, methodName, metaInfo, accessFlags, methodIndex, codeSize, instructions) :
    dictString = OrderedDict()

    dictString['className'] = className
    dictString['methodName'] = methodName
    dictString['metaInfo'] = metaInfo
    dictString['accessFlags'] = accessFlags
    dictString['methodIndex'] = methodIndex
    dictString['codeSize'] = codeSize
    dictString['instructions'] = instructions

    return str(dictString)

def get_instructions_from_method(method) :
    instructions = ''

    for n, inst in enumerate(method.get_instructions()) :
        instructions = instructions + inst.disasm().replace('  ','') + '////'

    return instructions

def parse_methods_from_APK(targetAPK) :
    apk = openAPK(targetAPK)
    dex = getDEX(apk.get_dex())
    methods = dex.get_methods()

    return methods

def list_to_string_with_newline(listData) :
    return '\n'.join(listData)

def generate_methodList(methods) :
    methodInfoList = list()

    for method in methods :
        methodInfoList.append(method_info_to_dict(
            method.get_class_name(),
            method.get_name(),
            method.get_information(),
            method.get_access_flags_string(),
            method.get_method_idx(),
            method.get_length(),
            get_instructions_from_method(method)
            ))

    print('Parse Method Lists from APK')

    return list_to_string_with_newline(methodInfoList)


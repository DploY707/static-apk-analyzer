import os, re
from collections import OrderedDict
from androguard.core.bytecodes.apk import APK as openAPK
from androguard.core.bytecodes.dvm import DalvikVMFormat as getDEX
from androguard.core.analysis.analysis import MethodAnalysis as methAnalysis
from androguard.decompiler.dad.decompile import DvMethod

class CodeExtractor :

    def __init__(self, target) :
        self.apk = openAPK(target)
        self.dex = getDEX(self.apk.get_dex())
        self.methods = self.dex.get_methods()
        
        self.methodInfoList = None
        self.referenceInfoList = None
        
    def method_info_to_dict(self, className, methodName, metaInfo, accessFlags, methodIndex, codeSize, instructions, sourceCode) :
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
        methodDict['sourceCode'] = sourceCode

        return methodDict

    def optimize_instruction_format(self, inst) :
        if '-payload' not in inst :
            instSep = re.sub("  +", "||", inst)

            optimized = (
                    instSep
                    .replace(' ', '')
                    .replace(',', ', ')
                    .split('||')
                    )

            dictInst = OrderedDict()

            dictInst['bytecode'] = optimized[0]
            dictInst['smali'] = ' '.join(optimized[1:])

            return dictInst

        else :
            return inst

    def get_instructions_from_method(self, method) :
        instructions = list()

        for n, inst in enumerate(method.get_instructions()) :
            instructions.append(self.optimize_instruction_format(inst.disasm()))

        return instructions

    def make_method_meta_info_inform(self, metaInfo) :
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

    def generate_methodList(self) :
        self.methodInfoList = list()

        for method in self.methods :
            self.methodInfoList.append(self.method_info_to_dict(
                method.get_class_name(),
                method.get_name(),
                self.make_method_meta_info_inform(method.get_information()),
                method.get_access_flags_string(),
                method.get_method_idx(),
                method.get_length(),
                self.get_instructions_from_method(method),
                self.decompile_method(method)
                ))

        print('Parse Method Lists from APK')

    def get_methodInfoList(self) :
        if self.methodInfoList is None :
            self.generate_methodList()

        return self.methodInfoList

    def decompile_method(self, method) :
        if 'native' in method.get_access_flags_string() :
            self.native_to_cpp(method)
        else :
            methInfo = methAnalysis(self.dex, method)

            if methInfo.is_external() :
                # External methods don't have any bytecodes in current dex file
                # TODO : Link codes in other dex / jar / so / etc . . .
                print("This method is external method")
                return 'NO-CODES'
            elif not methInfo.exceptions.exceptions :
                return self.bytecode_to_java(methInfo)
            else :
                # TODO : Implement decompiling sequence of the methods that include exception & exception-handling sequence
                return

    def bytecode_to_java(self, methInfo) :
        dv = DvMethod(methInfo)
        dv.process()
        return dv.get_source()

    def referenceInfo_to_dict(self, callerClass, callerMethod, calleeClass, calleeMethod) :
        # TODO : Call-type should be concerned
        referenceInfoDict = OrderedDict()

        referenceInfoDict['callerClass'] = callerClass
        referenceInfoDict['callerMethod'] = callerMethod
        referenceInfoDict['calleeClass'] = calleeClass
        referenceInfoDict['calleeMethod'] = calleeMethod

        return referenceInfoDict

    def generate_referenceInfoList(self) :
        # In this version, just consider about call reference
        # TODO : implement data reference parsing module
        if self.methodInfoList is not None :
            print('Start generate referenceInfoList')

            callReferenceList = list()

            for methodInfo in self.methodInfoList :
                for inst in methodInfo['instructions'] :
                    if '-payload' not in inst and 'invoke' in inst['smali'] :
                        calleeInfo = inst['smali'].split(', ')[-1]

                        if '->' in calleeInfo :
                            callReferenceList.append(self.referenceInfo_to_dict(
                                methodInfo['className'],
                                methodInfo['methodName'],
                                calleeInfo.split('->')[0],
                                calleeInfo.split('->')[1]
                                ))
                        else :
                            # TODO : this case should be handled for full coverage of code extraction
                            print(calleeInfo)

            self.referenceInfoList = callReferenceList

        else:
            print('methodList is not initialized')
            return

    def get_referenceInfoList(self) :
        if self.referenceInfoList is None :
            self.generate_referenceInfoList()

        return self.referenceInfoList

    # TODO : implement or porting new decompiiler for asm to cpp/c code
    def native_to_cpp(self, methInfo) :
        return

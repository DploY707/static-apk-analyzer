from collections import OrderedDict
from irparser import CodeParser
from utils import load_pickle


class CallReferencer :

    def __init__(self) :
        self.defineList = list()
        self.callRefList = None
        self.funcInfoList = None

    def load_funcInfo(self, funcInfoPath) :
        self.funcInfoList = load_pickle(funcInfoPath)

    def get_callRefList(self) :

        if self.callRefList is None :
            self.callRefList = list()
            self.generate_callRefList(self.funcInfoList)

        return self.callRefList

    def generate_defineList(self, funcInfoList) :
        indexList = list()

        for funcInfo in funcInfoList :
            indexList.append(funcInfo['functionIndex'])

        indexList.sort()
        return indexList

    def generate_callRefList(self, funcInfoList) :

        for funcInfo in funcInfoList :
            caller = funcInfo['libraryName'] + ';' + funcInfo['functionName']
            calleeList = self.extract_calleeList(funcInfo['IRCodes'], caller)

            for callee in calleeList :
                callRef = OrderedDict()
                callRef['caller'] = caller
                callRef['callee'] = callee

                self.callRefList.append(callRef)

    def extract_calleeList(self, codeList, caller) :
        ip = CodeParser(codeList, caller)
        calleeList = ip.get_callee()
        return calleeList


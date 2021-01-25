import pickle
from collections import OrderedDict
from irparser import InstructionParser

class Referencer :

	def __init__(self) :
		self.defineList = list()
		self.callRefList = list()


	def generate_defineList(self, funcInfoList) :
		indexList = list()

		for funcInfo in funcInfoList :
			indexList.append(funcInfo['functionIndex'])

		indexList.sort()
		return indexList

	def load_callRef(self, funcInfoList) :
		callRefList = list()

		for funcInfo in funcInfoList :
			caller = funcInfo['functionName']
			codeList = self.load_codeList(funcInfo)
			calleeList = self.extract_callRef(codeList, caller)
			self.match_caller_callee(callRefList, caller, calleeList)

		return callRefList

	def load_codeList(self, funcInfo) :
		IRCodes = funcInfo['IRCodes']
		codeList = list()

		for i in range(len(IRCodes)) :
			codeList.append(IRCodes[str(i+1)])

		return codeList

	def extract_callRef(self, codeList, caller) :
		ip = InstructionParser(codeList, caller)
		calleeList = ip.get_callee()
		return calleeList


	def match_caller_callee(self, callRefList, caller, calleeList) :

		if len(calleeList) < 1 :
			return

		for callee in calleeList :
			matchList = OrderedDict()
			matchList['caller'] = caller
			matchList['callee'] = callee
			callRefList.append(matchList)

def load_funcInfoList(filePath) :
	funcInfoFile = open(filePath, "rb")
	funcInfoList = pickle.load(funcInfoFile)
	return funcInfoList


import pickle
from collections import OrderedDict
from irparser import InstructionParser
from utils import load_pickle as load_funcInfo

class Referencer :

	def __init__(self, funcInfoPath) :
		self.defineList = list()
		self.callRefList = None
		self.funcInfoList = load_funcInfo(funcInfoPath)

	def get_callRefList(self) :

		if self.callRefList is None :
			self.callRefList = self.generate_callRefList(self.funcInfoList)

		return self.callRefList

	def generate_defineList(self, funcInfoList) :
		indexList = list()

		for funcInfo in funcInfoList :
			indexList.append(funcInfo['functionIndex'])

		indexList.sort()
		return indexList

	def generate_callRefList(self, funcInfoList) :
		callRefList = OrderedDict()

		for funcInfo in funcInfoList :
			caller = funcInfo['functionName']
			codeList = self.load_codeList(funcInfo)
			calleeList = self.extract_callRef(codeList, caller)
			callRefList[str(caller)] = calleeList

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


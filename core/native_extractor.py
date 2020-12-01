# native_extractor.py
# llvm ir parse (in now, cover only function)
# RetDec supports configure file in json type
# contributed by kordood

from collections import OrderedDict
from enum import Enum
from sys import exit

class Delimiter(Enum) :
	PARENL = '('
	PARENR = ')'
	BRACEL = '{'
	BRACER = '}'
	DEFINE = 'define'
	DECLARE = 'declare'
	COMMA = ','
	AT = '@'
	PERCENT = '%'


class Function :

	def __init__(self, functionName, returnType, params, functionIndex, codeSize, IRCodes) :
		self.functionName = functionName
		self.returnType = returnType
		self.params = params
		self.functionIndex = functionIndex
		self.codeSize = codeSize
		self.IRCodes = IRCodes

	def get_name(self) :
		return self.functionName

	def get_returnType(self) :
		return self.returnType

	def get_params(self) :
		return self.params

	def get_functionIndex(self) :
		return self.functionIndex

	def get_codeSize(self) :
		return self.codeSize

	def get_IRCodes(self) :
		return self.IRCodes


class NativeExtractor :

	def __init__(self, targetPath, lexFlag=0) :
		self.IRFile = self.open_IRFile(targetPath)
		self.lexFlag = lexFlag
		self.functionIndex = 0

		self.functionList = None 

	def make_function_info_to_dict(self, functionName, returnType, params, functionIndex, codeSize, IRCodes) :
		functionDict = OrderedDict()

		functionDict['functionName'] = str(functionName)
		functionDict['returnType'] = str(returnType)
		functionDict['paramList'] = params
		functionDict['functionIndex'] = self.functionIndex
		functionDict['codeSize'] = codeSize
		functionDict['IRCodes'] = IRCodes

		return functionDict

	def make_indexList_to_dict(self, targetList) :
		targetListDict = OrderedDict()

		if bool(targetList) :

			for index in range(len(targetList)) :
				number = index + 1
				targetListDict[str(number)] = targetList[index]

		return targetListDict

	def generate_functionList(self) :
		self.functionList = list()
		functions = self.lex_function()

		for function in functions :
			self.functionList.append(self.make_function_info_to_dict(
				function.get_name(),
				function.get_returnType(),
				self.make_indexList_to_dict(function.get_params()),
				function.get_functionIndex(),
				function.get_codeSize(),
				self.make_indexList_to_dict(function.get_IRCodes())
				))

		print('Parse function Lists from so file')

	def get_functionList(self) :
		if self.functionList is None :
			self.generate_functionList()

		return self.functionList

	def open_IRFile(self, IRFilePath) :
		IRFile = open(IRFilePath, 'r')
		return IRFile

	def readline_IRFile(self) :
		IRStr = self.IRFile.readline()
		return IRStr

	def readlines_IRFile(self) :
		IRStrList = self.IRFilereadlines()
		return IRStrList

	# lexer flag(default: 0)
	# 0: lex line by line, 1: lex full line in one time
	def lex_function(self) :
		lexFlag = self.lexFlag

		functions = None

		if lexFlag is None :
			lexFlag = 0

		if lexFlag is 0 :
			functions = self.lex_line_by_line()

		elif lexFlag is 1 :
			functions = self.lex_full_line()

		else :
			print("Warning: lex_function - lexFlag is invalid. (" + str(lexFlag) + ")")
			functions = self.lex_line_by_line()

		return functions

	def lex_line_by_line(self) :
		functions = list()
		line = None
		isInBrace = False

		while line != '' :
			line = self.readline_IRFile()

			if not isInBrace :

				if self.is_function_define(line) :
					functionName, returnType, params = self.parse_function_define(line)
					IRCodeList = list()
					self.functionIndex += 1
					isInBrace = True

			else :

				if line[0] is Delimiter.BRACER.value : 
					isInBrace = False
					IRCodes = IRCodeList[:]		# shallow copy
					codeSize = len(IRCodes)
					func = Function(functionName, returnType, params, self.functionIndex, codeSize, IRCodes)
					functions.append(func)

				else :
					code = line.strip()
					IRCodeList.append(code)

		return functions

	def lex_full_line(self) :
		functions = list()
		lines = self.readlines_IRFile()
		isInBrace = False

		for line in lines :

			if not isInBrace :

				if self.is_function_define(line) :
					functionName, returnType, params = self.parse_function_define(line)
					IRCodeList = list()
					self.functionIndex += 1
					isInBrace = True

			else :

				if line[0] is Delimiter.BRACER.value : 
					isInBrace = False
					IRCodes = IRCodeList[:]		# shallow copy
					codeSize = len(IRCodes)
					func = Function(functionName, returnType, params, self.functionIndex, codeSize, IRCodes)
					functions.append(func)

				else :
					code = line.strip()
					IRCodeList.append(code)

		return functions

	def is_function_define(self, targetStr) :
		if Delimiter.DEFINE.value in targetStr :
			self.prevent_comma_space_split(targetStr)
			firstWord = targetStr.split(' ')[0]

			if firstWord == Delimiter.DEFINE.value :
				return True

		return False

	def prevent_comma_space_split(self, targetStr) :
		targetStr = targetStr.replace(', ', ',')

	def parse_function_define(self, targetStr) :
		splitStr = targetStr.split(" ")
		attrLen = len(splitStr)
		functionName = None
		returnType = None
		params = None

		funcAttrList = self.get_function_Attribute_List(targetStr)
		format = self.check_format(funcAttrList[0])

		
		if bool(format) :

			attrLeftList = funcAttrList[0]
			returnType = attrLeftList[-1]
			functionName = funcAttrList[1]
			params = funcAttrList[2]

			# formatA
			# ex) define i32 @function_cf0() local_unnamed_addr {
			if format == 'A' :
				pass

				# Not implemented
				# ex) local_unnamed_addr
				# attrRightList = funcAttrList[-1].split(' ')
				# address = attrRightList[1]

			# formatB
			# ex) define dso_local i32 @main() #0 {
			elif format == 'B' :
				pass

				# Not implemented
				# ex) dso_local
				# location = attrLeftList[-2]

		else :
			self.error_wrong_format(targetStr)

		return functionName, returnType, params

	def get_function_Attribute_List(self, targetStr) :
		attrList = list()
		funcNameLeftStr = targetStr.split(Delimiter.AT.value)[0].strip()
		funcNameRightStr = targetStr.split(Delimiter.PARENR.value)[-1].strip()
		funcNameMidStr = targetStr.split(funcNameLeftStr)[-1].split(funcNameRightStr)[0].strip()

		funcNameLeftList = funcNameLeftStr.split(' ')
		funcNameRightList = funcNameRightStr.split(' ')
		
		functionName = funcNameMidStr.split(Delimiter.PARENL.value)[0]
		
		funcArgStr = funcNameMidStr.split(functionName)[1]
		funcArgList = self.parse_function_argument(funcArgStr)

		attrList.append(funcNameLeftList)
		attrList.append(functionName)
		attrList.append(funcArgList)
		attrList.append(funcNameRightList)

		return attrList

	def parse_function_argument(self, targetStr) :
		argsList = list()
		argsStr = targetStr.strip(Delimiter.PARENL.value + Delimiter.PARENR.value)
		argStrList = argsStr.split(Delimiter.COMMA.value)

		for argStr in argStrList :
			argList = list()
			argStr = argStr.strip()
			argSplitStr = argStr.split(Delimiter.PERCENT.value)
			
			argType = argSplitStr[0].strip()
			argName = argSplitStr[-1]

			argList.append(argType)
			argList.append(argName)

			argsList.append(argList)

		return argsList

	def check_format(self, funcNameLeftList) :
		attrLeftLen = len(funcNameLeftList)

		if attrLeftLen == 2 :
			return 'A'
		
		elif attrLeftLen == 3 :
			return 'B'

		else :
			return False

	def error_wrong_format(self, causeStr) :
			print("Error: parse_function_define - Wrong format is in LLVM IR function definition ")
			print(causeStr)
			exit(-1)

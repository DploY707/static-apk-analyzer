# IrParser.py
# llvm ir parse (in now, cover only function define)
# RetDec supports configure file in json type
#
# contributed by kordood

from delimiter import Delimiter as Delim
from collections import OrderedDict
from sys import exit
from utils import get_regex_index

class Function :

	def __init__(self, functionName, returnType, params, functionIndex, codeSize, IRCodes) :
		self.functionName = functionName
		self.returnType = returnType
		self.params = params
		self.functionIndex = functionIndex
		self.codeSize = codeSize
		self.IRCodes = IRCodes

	def get_functionName(self) :
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

class CodeParser :

	def __init__(self, codeList, currentFunction) :
		self.codeList = codeList
		self.currentFunction = currentFunction
		self.callee = list()

		self.start_parsing()

	def get_currentFunction(self) :
		return self.currentFunction

	def get_callee(self) :
		return self.callee

	def start_parsing(self) :
		for codeStr in self.codeList :
			if self.is_call_instruction(codeStr) :
				callee = self.parse_code(codeStr)
				if callee is not None :
					self.callee.append(callee)

	def is_call_instruction(self, codeStr) :
		index = codeStr.find(' ' + Delim.CALL.value + ' ')

		return True if index > -1 else False

	def parse_code(self, codeStr) :
		lexemeList = codeStr.split(' ')
		funcName = self.find_calleeName(lexemeList)
		callee = funcName
		return callee

	def find_calleeName(self, lexemeList) :
		indexs = get_regex_index(lexemeList, '@.*\(')
		funcName = None

		try :
			funcName = lexemeList[indexs[0]].split(Delim.PARENL.value)[0]
		except IndexError:
			print(lexemeList)
			print(indexs)

		return funcName

	def print_error(self, msg) :
		print("Error: Invalid arrange of string - \"" + msg + "\"")

	def print_warning_arrange(self, msg) :
		print("Warning: Invalid arrange of string - \"" + msg + "\"")


class IRParser :

	def __init__(self, IRFilePath) :
		self.IRFile = open(IRFilePath, 'rb')
		self.functionIndex = 0
		self.functionList = None 
		self.defineList = list()
		self.declareList = list()

	def make_function_info_to_dict(self, functionName, returnType, params, functionIndex, codeSize, IRCodes) :
		functionDict = OrderedDict()

		functionDict['functionName'] = str(functionName)
		functionDict['returnType'] = str(returnType)
		functionDict['paramList'] = params
		functionDict['functionIndex'] = int(functionIndex)
		functionDict['codeSize'] = codeSize
		functionDict['IRCodes'] = IRCodes

		return functionDict

	def generate_functionList(self) :
		self.functionList = list()
		functions = self.lex_function()

		for function in functions :
			self.functionList.append(self.make_function_info_to_dict(
				function.get_functionName(),
				function.get_returnType(),
				function.get_params(),
				function.get_functionIndex(),
				function.get_codeSize(),
				function.get_IRCodes()
				))

		print('Parse function Lists from so file')

	def get_functionList(self) :
		if self.functionList is None :
			self.generate_functionList()

		return self.functionList

	def readLine_IRFile(self) :
		IRStr = self.IRFile.readline()

		return IRStr

	def lex_function(self) :
		functions = list()
		line = None
		isInBrace = False

		while line != '' :
			line = self.readLine_IRFile().decode('utf-8')

			if not isInBrace :

				if self.is_function_define(line) :
					functionName, returnType, params = self.parse_function_define(line)
					IRCodeList = list()
					self.functionIndex += 1
					isInBrace = True

			else :

				if line[0] is Delim.BRACER.value : 
					isInBrace = False
					IRCodes = IRCodeList[:]		# shallow copy
					codeSize = len(IRCodes)
					func = Function(functionName, returnType, params, self.functionIndex, codeSize, IRCodes)
					functions.append(func)

				else :
					code = line.strip()
					IRCodeList.append(code)

		return functions

	def is_function_define(self, expr) :
		if Delim.DEFINE.value in expr :
			self.prevent_comma_space_split(expr)
			firstWord = expr.split(' ')[0]

			if firstWord == Delim.DEFINE.value :
				return True

		return False

	def is_function_declare(self, expr) :
		if Delim.DECLARE.value in expr :
			self.prevent_comma_space_split(expr)
			firstWord = expr.split(' ')[0]

			if firstWord == Delim.DECLARE.value :
				return True

		return False

	def prevent_comma_space_split(self, targetStr) :
		targetStr = targetStr.replace(', ', ',')

	def parse_function_define(self, definition) :
		funcAttrList = self.get_function_Attribute_List(definition)

		attrLeftList = funcAttrList[0]
		returnType = attrLeftList[-1]
		functionName = funcAttrList[1]
		params = funcAttrList[2]

		# Todo: check format & parse
		'''
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
		'''
		return functionName, returnType, params

	def parse_function_declare(self, declaration) :
		splitByAt = declaration.split(Delim.AT.value)[1]
		splitByPARENL = splitByAt.split(Delim.PARENL.value)[0]
		functionName = Delim.AT.value + splitByPARENL

		return functionName

	def get_function_Attribute_List(self, targetStr) :
		attrList = list()
		funcNameLeftStr = targetStr.split(Delim.AT.value)[0].strip()
		funcNameRightStr = targetStr.split(Delim.PARENR.value)[-1].strip()
		funcNameMidStr = targetStr.split(funcNameLeftStr)[-1].split(funcNameRightStr)[0].strip()

		funcNameLeftList = funcNameLeftStr.split(' ')
		funcNameRightList = funcNameRightStr.split(' ')
		
		functionName = funcNameMidStr.split(Delim.PARENL.value)[0]
		
		funcArgStr = funcNameMidStr.split(functionName)[1]
		funcArgList = self.parse_function_argument(funcArgStr)

		attrList.append(funcNameLeftList)
		attrList.append(functionName)
		attrList.append(funcArgList)
		attrList.append(funcNameRightList)

		return attrList

	def parse_function_argument(self, targetStr) :
		argsList = list()
		argsStr = targetStr.strip(Delim.PARENL.value + Delim.PARENR.value)
		argStrList = argsStr.split(Delim.COMMA.value)

		for argStr in argStrList :
			argList = OrderedDict()
			argStr = argStr.strip()
			argSplitStr = argStr.split(Delim.PERCENT.value)
			
			argType = argSplitStr[0].strip()
			argName = argSplitStr[-1]

			argList[argType] = argName

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


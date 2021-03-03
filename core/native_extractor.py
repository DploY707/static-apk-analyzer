# NativeExtractor.py
#
# contributed by kordood

import os
import shutil
import utils
from argparse import ArgumentParser
from collections import OrderedDict
from subprocess import call, DEVNULL
from irparser import IRParser
from referencer import CallReferencer
from retdec import RetDec


class NativeExtractor :

	def __init__(self, APKPath, resultDir="/root/result", retdecDir="/home/retdec", forceRun=False) :
		self.APKPath = APKPath
		self.APKName = APKPath.split("/")[-1].replace(".apk",'')
		self.dirDict = self.initialize_dirList(resultDir, retdecDir)
		self.soPathList = list()
		self.funcPathList = list()
		self.defPathList = list()
		self.decPathList = list()
		self.retdec = RetDec()
		self.run_extractor(forceRun)

	def initialize_dirList(self, resultDir, retdecDir) :
		dirDict = OrderedDict()
		dirDict['result'] = resultDir
		dirDict['functionInfo'] = resultDir + "/functionInfo"
		dirDict['referenceInfo'] = resultDir + "/referenceInfo"
		dirDict['tmp'] = resultDir + "/tmp"
		dirDict['retdec'] = retdecDir
		dirDict['retdec_input'] = retdecDir + "/input"
		dirDict['retdec_output'] = retdecDir + "/output"

		return dirDict

	def run_extractor(self, forceRun) :

		if self.is_decompiled(self.APKName) or forceRun:
			self.collect_funcPath()
			return

		self.move_soFiles()
		self.decompile_binary()

		retdecOutPath = self.dirDict['retdec_output']
		outFileList = os.listdir(retdecOutPath)
		llFileList = self.add_llFile(outFileList)

		for llFile in llFileList :
			llFilePath = retdecOutPath + '/' + llFile
			parser = IRParser(llFilePath)
			functionList = parser.get_functionList()
			defineList = parser.defineList
			declareList = parser.declareList

			self.save_functionInfo(llFile, "_native_function", functionList, self.funcPathList)
			self.save_functionInfo(llFile, "_native_define", defineList, self.defPathList)
			self.save_functionInfo(llFile, "_native_declare", declareList, self.decPathList)

		utils.remove_files(self.dirDict['retdec_input'] + "/")
		utils.remove_files(self.dirDict['retdec_output'] + "/")

	def is_decompiled(self, APKName) :

		try :
			infoFiles = os.listdir(self.dirDict['functionInfo'] + "/" + APKName)
		except FileNotFoundError :
			return False

		checkList = ["_native_function", "_native_define", "_native_declare"]
		checkStatus = [False, False, False]

		for infoFile in infoFiles :

			for i in range(len(checkList)) :

				if checkList[i] in infoFile :
					checkStatus[i] = True

		for i in range(len(checkStatus)) :
			if checkStatus[i] is False :
				return False

		return True

	def collect_funcPath(self):
		funcDir = self.dirDict['functionInfo'] + "/" + self.APKName
		fileNameList = os.listdir(funcDir)

		for fileName in fileNameList :
			if "_native_function" in fileName :
				funcPath = funcDir + "/" + fileName
				self.funcPathList.append(funcPath)

	def save_functionInfo(self, llFile, extension, info, pathList=None) :
		saveDir = self.dirDict['functionInfo'] + "/" + self.APKName

		if os.path.exists(saveDir) is False :
			os.mkdir(saveDir)

		fileName = llFile.replace(".ll", extension)
		path = saveDir + "/" + fileName + ".pickle"

		utils.save_pickle(path, info)

		if pathList is not None :
			pathList.append(path)

	def move_soFiles(self) :
		soSrcList = self.get_so_from_APK(self.APKPath)
		soDstPath = self.dirDict['retdec_input']

		for soSrc in soSrcList :
			shutil.copy(soSrc, soDstPath)
			self.soPathList.append(soDstPath)

	def decompile_binary(self) :
		targetList = os.listdir(self.dirDict['retdec_input'])
		rd = self.retdec

		for target in targetList :
			inputPath = self.dirDict['retdec_input'] + "/" + target
			outputPath = self.dirDict['retdec_output'] + "/" + target

			rd.set_paths(inputPath, outputPath)
			rd.run_retdec()

	def get_so_from_APK(self, APKPath) :
		soPathList = list()
		outPath = self.extract_APK(APKPath)
		filePathList = self.find_fileList(outPath)

		for filePath in filePathList :

			if self.is_elf(filePath) :
				soPathList.append(filePath)

		return soPathList

	def extract_APK(self, APKPath) :
		extractPath = self.dirDict['result'] + '/tmp/' + self.APKName
		cmd = "unzip -u -d " + extractPath + ' ' + APKPath

		self.print_extract_APK(self.APKName, extractPath)
		call(cmd, shell=True, stdout=DEVNULL)

		return extractPath

	def find_fileList(self, targetPath) :
		command = "find " + targetPath + " -type f"

		outputStr = utils.run_shell_command(command)
		fileList = outputStr.split("\\n")[:-1]		# truncate ''(empty) element

		return fileList

	def is_elf(self, targetPath) :
		elfType = "ELF"
		command = "file " + targetPath

		outputStr = utils.run_shell_command(command)
		fileType = outputStr.split(' ')[1]

		if elfType == fileType :
			return True

		return False

	def parse_arch(self, fileStr) :
		if ',' in fileStr :
			arch = fileStr.split(',')[1]

			# Todo set architecture
			# if arch is "" :
		else :
			return "Unknown"

	def add_llFile(self, fileList) :
		llFileList = list()
		llType = ".ll"

		for file in fileList :

			if llType in file :
				llFileList.append(file)

		return llFileList

	def print_extract_APK(self, APKPath, extractPath) :
		print("Extract APK:" + str(APKPath) + "to" + str(extractPath))


def set_arguments(parser) :
	parser.add_argument('-i', '--input', required=False, help='Input APK path.')
	parser.add_argument('-o', '--output', required=False, help='Output directory path.')
	parser.add_argument('-f', '--force', required=False, help='Force-run decompiler.')


def check_arguments(args, APKFILEPATH, RESULTPATH, forceRun) :

	if args.input is not None:
		APKFILEPATH = args.input

	if args.output is not None:
		RESULTPATH = args.output

	if args.force is not None:
		forceRun = True


if __name__=="__main__" :
	parser = ArgumentParser(description="Processing Native Extractor")
	set_arguments(parser)
	args = parser.parse_args()

	APKFILEPATH = "/root/workDir/data/app-x86-debug.apk"
	RESULTPATH = "/root/result"
	forceRun = False

	check_arguments(args, APKFILEPATH, RESULTPATH, forceRun)

	ne = NativeExtractor(APKPath=APKFILEPATH, resultDir=RESULTPATH, forceRun=forceRun)
	funcPathList = ne.funcPathList

	cr = CallReferencer()
	callRefList = OrderedDict()

	for funcPath in funcPathList :
		cr.load_funcInfo(funcPath)
		# Todo: Support multi-so
		# callRefList.update(cr.get_callRefList())

	# Todo: Save call-reference
	# crefPath = funcPath.replace('.func', '.cref')

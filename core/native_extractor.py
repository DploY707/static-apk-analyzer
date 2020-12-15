# NativeExtractor.py
#
# contributed by kordood

import utils, shutil, os, pickle
from subprocess import check_output, call, DEVNULL
from retdec import RetDec
from irparser import IRParser

class NativeExtractor:

	def __init__(self, target, result="/tmp") :
		self.APKPath = target
		self.result = result
		self.soFileList = list()
		self.retdec = RetDec()
		self.retdecPath = "/home/retdec"


	def print_extract_APK(self, APKPath) :
		print("Extract APK:" + str(APKPath))

	def get_so_from_APK(self, APKPath) :
		soFileList = list()
		outPath = self.extract_APK(APKPath)
		filePathList = self.find_fileList(outPath)

		for filePath in filePathList :

			if self.is_elf(filePath) :
				soFileList.append(filePath)

		return soFileList

		# 1. extract APK
		# 2. gethering so files
		# 3. move so files

	def extract_APK(self, APKPath) :
		outdirPath = APKPath.split(".apk")[0]
		cmd = "unzip -f -d " + outdirPath + ' ' + APKPath

		self.print_extract_APK(APKPath)
		call(cmd, shell=True, stdout=DEVNULL)

		return outdirPath

	def find_fileList(self, targetPath) :
		command = "find " + targetPath + " -type f"
		
		outputStr= utils.run_shell_command(command)
		fileList = outputStr.split("\\n")[:-1]	# truncate ''(empty) element

		return fileList

	def is_elf(self, targetPath) :
		elfType = "ELF"
		command = "file " + targetPath

		outputStr = utils.run_shell_command(command)
		fileType = outputStr.split(' ')[1]

		if elfType == fileType :
			return True

		return False

	def run_extractor(self) :
		soFileList = list()
		soSrcList = self.get_so_from_APK(self.APKPath)
		soDestPath = self.retdecPath + "/input"

		for soSrc in soSrcList :
			shutil.copy(soSrc, soDestPath)
			soFileList.append(soDestPath)

		self.soFileList = soFileList

		self.decompile_binary()
		self.generate_functionInfo()


	def decompile_binary(self) :
		targetList = os.listdir(self.retdecPath + "/input")
		rd = self.retdec

		for target in targetList :
			inputPath = self.retdecPath + "/input/" + target
			outputPath = self.retdecPath + "/output/" + target

			rd.set_paths(inputPath, outputPath)
			rd.run_retdec()

	def generate_functionInfo(self) :
		outputPath = self.retdecPath + "/output"
		fileList = os.listdir(outputPath)
		llFileList = self.add_llFile(fileList)

		for llFile in llFileList :
			llFilePath = outputPath + '/' + llFile

			parser = IRParser(llFilePath)
			functionList = parser.get_functionList()

			outFileName = llFile.replace(".ll", ".func")
			resultPath = self.result + '/' + outFileName
			self.save_functionInfo(resultPath, functionList)

	def add_llFile(self, fileList) :
		llFileList = list()
		llType = ".ll"

		for file in fileList :

			if llType in file :
				llFileList.append(file)

		return llFileList

	def save_functionInfo(self, resultPath, functionInfoList) :
		functionInfoFile = open(resultPath, 'wb')
		pickle.dump(functionInfoList, functionInfoFile)
		functionInfoFile.close()


if __name__=="__main__" :
	IRFILEPATH = "/home/liberty/Code_Extractor/Code-Extractor/data/hello.ll"
	APKFILEPATH = "/root/workDir/data/app-x86-debug.apk"
	ne = NativeExtractor(APKFILEPATH)
	ne.run_extractor()

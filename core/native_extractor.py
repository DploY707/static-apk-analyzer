# NativeExtractor.py
#
# contributed by kordood

import utils, shutil, os, pickle, sys
from subprocess import check_output, call, DEVNULL
from retdec import RetDec
from irparser import IRParser
from referencer import Referencer

class NativeExtractor:

	def __init__(self, target, resultDir="/tmp") :
		self.APKPath = target
		self.resultDir = resultDir
		self.soPathList = list()
		self.funcPathList = list()
		self.retdec = RetDec()
		self.retdecPath = "/home/retdec"
		self.run_extractor()

	def run_extractor(self) :
		self.move_soFiles()

		self.decompile_binary()
		self.generate_functionInfo()
		utils.remove_files(self.retdecPath + "/input/")
		utils.remove_files(self.retdecPath + "/output/")

	def move_soFiles(self) :
		soFileList = list()
		soSrcList = self.get_so_from_APK(self.APKPath)
		soDestPath = self.retdecPath + "/input"

		for soSrc in soSrcList :
			shutil.copy(soSrc, soDestPath)
			self.soPathList.append(soDestPath)
			

	def get_so_from_APK(self, APKPath) :
		soPathList = list()
		outPath = self.extract_APK(APKPath)
		filePathList = self.find_fileList(outPath)

		for filePath in filePathList :

			if self.is_elf(filePath) :
				soPathList.append(filePath)

		return soPathList

	def extract_APK(self, APKPath) :
		outdirPath = APKPath.split(".apk")[0]
		cmd = "unzip -u -d " + outdirPath + ' ' + APKPath

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

	def decompile_binary(self) :
		targetList = os.listdir(self.retdecPath + "/input")
		rd = self.retdec

		for target in targetList :
			inputPath = self.retdecPath + "/input/" + target
			outputPath = self.retdecPath + "/output/" + target

			rd.set_paths(inputPath, outputPath)
			rd.run_retdec()

	def generate_functionInfo(self) :
		retdecOutPath = self.retdecPath + "/output"
		outFileList = os.listdir(retdecOutPath)
		llFileList = self.add_llFile(outFileList)

		for llFile in llFileList :
			llFilePath = retdecOutPath + '/' + llFile

			parser = IRParser(llFilePath)
			functionList = parser.get_functionList()

			outFileName = llFile.replace(".ll", ".func")
			funcInfoPath = self.resultDir + '/' + outFileName
			self.save_functionInfo(funcInfoPath, functionList)
			self.funcPathList.append(funcInfoPath)

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

	def print_extract_APK(self, APKPath) :
		print("Extract APK:" + str(APKPath))



if __name__=="__main__" :
	APKFILEPATH = "/root/workDir/data/app-x86-debug.apk"
	FUNCLISTPATH = "/root/results/functionLists"

	if len(sys.argv) > 1 :
		APKFILEPATH = sys.argv[1]

	ne = NativeExtractor(APKFILEPATH, FUNCLISTPATH)

	funcPathList = ne.funcPathList

	for funcPath in funcPathList :
		rf = Referencer(funcPath)
		print(rf.get_callRefList())


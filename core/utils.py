import os

class DirStruct:

	def __init__(self, path) :
		self.path = path

	def get_fileList_from_directory(self, dirPath) :
		return os.listdir(dirPath)

	def get_directory_hierarchy(self) :
		subDirPathList = list()

		self.parse_directory_hierarchy(subDirPathList, self.path)
		return subDirPathList

	# Todo: make directoryList which is including APK(s)
	def get_directory_include_file(self, dirPathList) :
		resultDirList = list()

		for dirPath in dirPathList :
			fileList = self.get_fileList_from_directory(dirPath)

			for fileName in fileList :
				filePath = dirPath + '/' + fileName

				if self.is_file(filePath) :
					resultDirList.append(dirPath)
					break

		return resultDirList

	# if useless : delete this method
#def get_APKs_in_directory(self, dirPath) :

	def parse_directory_hierarchy(self, dirPathList, dirPath) :
		fileList = self.get_fileList_from_directory(dirPath)

		for fileName in fileList :
			filePath = dirPath + '/' + fileName

			if self.is_directory(filePath) :
				self.add_and_find_subDirectory(dirPathList, filePath)

	def is_directory(self, dirPath) :
		return os.path.isdir(dirPath)

	def is_file(self, filePath) :
		return os.path.isfile(filePath)

	def add_and_find_subDirectory(self, resultPathList, dirPath) :
		resultPathList.append(dirPath)
		self.parse_directory_hierarchy(resultPathList, dirPath)

if __name__ == "__main__" :
	# testcode of get_dir_include_file
	TEST_DIR_PATH = "/home/liberty/Code_Extractor/testDir"
	ds = DirStruct(TEST_DIR_PATH)
	testDirList = ds.get_directory_hierarchy()
	fileDirList = ds.get_directory_include_file(testDirList)
	print(testDirList)
	print(fileDirList)


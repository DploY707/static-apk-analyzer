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

	def parse_directory_hierarchy(self, dirPathList, dirPath) :
		fileList = self.get_fileList_from_directory(dirPath)

		for fileName in fileList :
			filePath = dirPath + '/' + fileName

			if self.is_directory(filePath) :
				self.add_and_find_subDirectory(dirPathList, filePath)

	def is_directory(self, dirPath) :
		return os.path.isdir(dirPath)

	def add_and_find_subDirectory(self, resultPathList, dirPath) :
		resultPathList.append(dirPath)
		self.parse_directory_hierarchy(resultPathList, dirPath)

if __name__=="__main__" :
	TEST_DIR_PATH = "/home/liberty/Code_Extractor/testDir"
	f = DirStruct(TEST_DIR_PATH)
	dirList = f.get_directory_hierarchy()
	print(dirList)

# retdec.py
#
# contributed by kordood

import utils
from argparse import ArgumentParser
from subprocess import check_output, call

class RetDec :

	def __init__(self, inputPath=None, outputPath=None) :
		self.decompiler = self.get_decompiler_path()
		self.inputPath = inputPath
		self.outputPath = None

		if outputPath :
			self.outputPath = outputPath

	def get_decompiler_path(self) :
		outputByte = check_output("which retdec-decompiler", shell=True)
		decompilerPath = utils.convert_subprocess_output_to_str(outputByte).split('\\n')[0]

		return decompilerPath

	def get_filePath_llvm_IR(self) :
		llFilePath = self.get_filePath_from_extension("ll")

		return llFilePath

	def get_filePath_llvm_bc(self) :
		bcFilePath = self.get_filePath_from_extension("bc")

		return bcFilePath

	def get_filePath_with_extension(self, extension) :
		irFilePath = None

		if self.outputPath :
			irFilePath = self.outputPath + '.' + extension

		else :
			irFilePath = self.inputPath + '.' + extension

		return irFilePath

	def set_paths(self, inputPath, outputPath) :
		self.set_inputPath(inputPath)
		self.set_outputPath(outputPath)

	def set_inputPath(self, inputPath) :
		self.inputPath = inputPath

	def set_outputPath(self, outputPath) :
		self.outputPath = outputPath

	def run_retdec(self) :
		cmd = self.decompiler + " " + self.inputPath

		if self.outputPath :
			cmd += " -o " + self.outputPath

		outputByte = call(cmd, shell=True)


def set_arguments(parser) :
	parser.add_argument('-i', '--input', required=True, help='Input file path. Format: ELF, PE, Mach-O, COFF, AR (archive), Intel HEX, and raw machine code')
	parser.add_argument('-o', '--output', required=False, help='Output file path')

if __name__=="__main__" :
	parser = ArgumentParser(description="Processing RetDec Decompiler")
	set_arguments(parser)
	args = parser.parse_args()

	rd = RetDec(args.input, args.output)
	rd.run_retdec()

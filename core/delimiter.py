# delimiter.py
#
# contributed by kordood

from enum import Enum


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
	CALL = 'call'
	ARM = 'ARM'
	MIPS = 'MIPS'
	x86_64 = 'x86-64'
	x86 = 'Intel 80386'


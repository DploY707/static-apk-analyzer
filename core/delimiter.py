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

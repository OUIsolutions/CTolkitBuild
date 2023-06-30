
from .string_type import StringType
from .element import Element
from .element_pointer import ElementPointer

INT = Element('int')
CHAR = Element('char')
LONG = Element('long')
FLOAT = Element('float')
DOUBLE = Element('Double')
BOOL = Element('bool')
STRING = StringType()
VOID = ElementPointer('void *')

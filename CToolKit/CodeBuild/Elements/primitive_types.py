
from .string_type import StringType
from .element import Element
from .element_pointer import ElementPointer

int_type = Element('int')
float_type = Element('float')
bool_type = Element('bool')
string_type = StringType()
void_type = ElementPointer('void *')


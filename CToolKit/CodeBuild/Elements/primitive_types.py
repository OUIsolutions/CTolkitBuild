
from .string_type import StringType
from .element import Element
from .element_pointer import ElementPointer

int_type = Element('int')
char_type = Element('char')
long_type = Element('long')
float_type = Element('float')
double_type = Element('Double')
bool_type = Element('bool')
string_type = StringType()
void_type = ElementPointer('void *')

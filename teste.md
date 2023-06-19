is An Python Package to manipulate C/C++ buildings and PipeLines providing
easy automation tools to increase your code pipelines with amalgamations, 
black box testing, and readme replacment

## source:
https://github.com/OUIsolutions/CTolkitBuild
## pip:
https://pypi.org/project/CToolKit/
## use case:
https://github.com/OUIsolutions/CTextEngine

https://github.com/WacoderForever/clinput

### Instalation 
```shell
pip install CToolKit
```
### Usage 
amalgamating an lib 
```python
import CToolKit as ct

STARTER  = f'CTextEngine/CTextEngineMain.h'
OUTPUT = 'amalgamated.h'
amalgamated_code = ct.generate_amalgamated_code(STARTER,OUTPUT)
```

copiling an file and generating a full valgrind checking

```python
import CToolKit as ct

COPILER = 'gcc'
FILE = 'test.c'
OUTPUT = 'test.out'
ct.compile_project(
    COPILER,
    FILE,
    OUTPUT,
    raise_errors=True,
    raise_warnings=True
)

FLAGS = ['-libcur']
ct.test_binary_with_valgrind(OUTPUT, FLAGS) 
```



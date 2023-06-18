# CToolkit
 is An Python Package to manipulate C/C++ buildings and  PipeLines
 providing easy automation tools to increase your code pipelines 
 with amalgamations, black box testing, and readme replacment

### Installation from scratch

clone the repo into your machine with:

~~~shell
git clone https://github.com/OUIsolutions/CTolkitBuild.git
~~~
Then install with:
~~~shell
pip install .
~~~

### Installation from github
type the following comand to install from github
~~~shell
pip install git+https://github.com/OUIsolutions/CTolkitBuild.git
~~~

### Amalgamation System

for amalgamate an C lib its super easy, just call 
~~~python
import CToolKit as ct

STARTER  = f'test.h'
OUTPUT = 'amalgamated.h'
amalgamated_code = ct.generate_amalgamated_code(STARTER)
with open(OUTPUT,'w') as arq:
    arq.write(amalgamated_code)
~~~
or even more implicit:
~~~python

import CToolKit as ct

STARTER  = f'CTextEngine/CTextEngineMain.h'
OUTPUT = 'amalgamated.h'
amalgamated_code = ct.generate_amalgamated_code(STARTER,OUTPUT)

~~~

### Comand Line Operations

#### Copile an Project 
it wil copile the given file 

~~~python


import CToolKit as ct
COPILER = 'gcc'
FILE = 'test.c'
OUTPUT = 'test.out'
ct.copile_project(
    COPILER,
    FILE,
    OUTPUT,
    raise_errors=True,
    raise_warnings=True
    )
~~~







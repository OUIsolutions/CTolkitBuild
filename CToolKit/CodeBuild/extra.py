import os


def save_file(content:str,output:str):
    elements = output.split('/')
    if len(elements) > 1:
        dirs = '/'.join(elements[0:-1])
        os.makedirs(dirs)

    with open(output,'w')  as arq:
        arq.write(content)


import os
def save_file(content:str,output:str):
    os.makedirs(output)
    with open(output,'w')  as arq:
        arq.write(output)

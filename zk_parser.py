import markdown
import pandas as pd
from os import listdir
from os.path import isfile, join

mypath = '..'
filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
filelist = [f for f in filelist if '.md' in f]
cols = ['id', 'title', 'author' , 'tags' ,'links']
zk = pd.DataFrame(columns=cols)

for f in filelist:
    with open("../"+f, "r", encoding="utf-8") as input_file:
        print(f)
        text = input_file.read()


    title = text.split('#title ')[1].split('\n')[0]
    author = text.split('#author ')[1].split('\n')[0]
    file_id = text.split('ID: ')[1].split('\n')[0]
    heads = [text.split('#')[i].split('\n')[0] for i in range(len(text.split('#')))]
    tags = []; reserved = ['literature ', 'reference', ' Metadata', '', ' ']
    for t in heads:
        if t.split(' ')[0] not in reserved:
            if title not in t and author not in t:
                tags.append(t.split(' ')[0])

    links = [text.split('[[')[i].split(']]')[0] for i in range(1, len(text.split('[[')))]

    row = [file_id, title, author, tags, links]
    zk.loc[len(zk)] = row

zk

from pyzotero import zotero
zotero_user = 7404811
zotero_key = 'CfBLE4xzHEMo8bMsufYVR8ql'
zot = zotero.Zotero(zotero_user, 'user', zotero_key)
zot.add_parameters(format='bib')
bibliography = zot.items()

#todo - parse HTML result from zotero bibliography and match citations based on title to dataframe
#pyzotero docs: https://pyzotero.readthedocs.io/en/latest/
#jupyter notebook for visualization: https://nbviewer.jupyter.org/github/jkbren/presilience/blob/master/code/01_Intro_Network_Resilience.ipynb
import os,re

root=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))

excludedir = (
    ".git",
    ".github",
    ".idea",
    "__pycache__",
    "data",
    "dist",
    "font",
    "img",
    "font",
     "installer")

p=re.compile(r'_[vV][0-9.\-_]+[.]py$$|[.]old[.]py$')

def getsrclist(dir=None):
    if dir==None:
        dir=root
    rst=[]
    lst = os.listdir(dir)
    for f in lst:
        if f in excludedir:
            continue
        file=os.path.join(dir,f)
        if os.path.isfile(file):
            if f.endswith(".py"):
                if(p.search(f)==None):
                    rst.append(os.path.relpath(file,root))
        elif os.path.isdir(file):
            subdir=file
            rst.extend(getsrclist(subdir))
    return rst
            
fs=getsrclist()
os.chdir(root)
print(fs)
s="pylupdate5 {} -ts {}".format(" ".join(fs),os.path.join(os.path.dirname(__file__),"English.ts"))
os.system(s)
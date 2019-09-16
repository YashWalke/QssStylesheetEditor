import shutil
import os
import py_compile
# import compileall as com
# com.compile_dir(dir,optimize=2)
from py_compile import compile

# 源代码根文件夹 数据文件夹
root = os.path.join(os.path.dirname(__file__), "..")
pydir=os.path.join(root,"dist/libs/libpython")
dlldir=os.path.join(root,r"dist/libs/DLLs")
libdir=os.path.join(root,"dist/libs/Lib")
datadir = os.path.join(root, "data")
resdir = os.path.join(root, "res")
distroot = os.path.join(root, "dist/build")
# 不编译的文件夹，文件后缀
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

# 删除dist/build文件夹下所有文件
print("remove all files in dist/build.")

if not os.path.exists(distroot):
    os.mkdir(distroot)

def clearDir(path):
    delList = os.listdir(path)
    for f in delList:
        filePath = os.path.join(path, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
            print("  remove "+f)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
            print("  remove "+f)


clearDir(distroot)

# 拷贝data和img文件夹到dist/build/scripts文件夹
print("\ncopy data dir to dist/build.")


def copypath(path, distdir):
    name = os.path.basename(path)
    #print(path+ "is file?"+ str(os.path.isfile(path)))
    if os.path.isfile(path):
        shutil.copy(path, distdir)
        print("  copy "+os.path.relpath(path,root))
    elif os.path.isdir(path):
        out = os.path.join(distdir, name)
        os.makedirs(out)
        for f in os.listdir(path):
            p=os.path.join(path,f)
            copypath(p, out)

def copyfiles(path, distdir,exclude=[".py"]):
    files = os.listdir(path)
    if(not os.path.exists(distdir)):
        os.mkdir(distdir)
    for fname in files:
        f=os.path.join(path,fname)
        if os.path.isfile(f):
            ext=os.path.splitext(f)[1]
            if(ext not in exclude):
                shutil.copy(f, distdir)
                print("  copy "+os.path.relpath(path,root))


copypath(datadir, os.path.join(distroot,"scripts"))
copypath(libdir,distroot)
copypath(pydir, distroot)

copyfiles(resdir, os.path.join(distroot,"scripts/res"),[".py",".qrc"])
copyfiles(dlldir,distroot)
copyfiles(os.path.join(root,r"dist/libs"),distroot)#copy app.exe
#shutil.copy(os.path.join(root,"dist/libs/QssStylesheetEditor.exe"),distroot)

# compile python 脚本并copy到目标文件夹
print("\ncompile all scripts and copy to dist/build.")
copyexts=(".zip",".bat",".qm",".toml",".conf")
import re 
pexclude=re.compile(r'_[vV][0-9.\-_]+[.]py$$|[.]old[.]py$')
def compile_copy(path, distdir):
    list = os.listdir(path)
    copyfiles = False
    for name in list:
        file=os.path.join(path,name)
        if os.path.isfile(file):
            if name.endswith(".py") and pexclude.search(name)==None:
                print("  compile "+name)
                compile(file, optimize=2, cfile=os.path.join(distdir,name+"c"))
                copyfiles = True
            elif os.path.splitext(file)[-1] in copyexts:
                shutil.copy(file, distdir)
                print("  copy "+name)
                copyfiles = True
        elif os.path.isdir(file):
            if name in excludedir:
                continue
            out = os.path.join(distdir,name)
            if(not os.path.exists(out)):
                os.makedirs(out)
            empty=compile_copy(file, out)
            if empty:
                os.rmdir(out)
    nofilecompileandcopy= not copyfiles
    return nofilecompileandcopy

compile_copy(root, os.path.join(distroot,"scripts"))
#compile main.py
compile_copy(os.path.join(pydir,"../scripts"),os.path.join(distroot,"scripts"))

# os.chdir(os.path.join(dir,"__pycache__"))
# list=os.listdir(".")
# for f in list:
    # o=f.replace(".cpython-37.opt-2","")
    # os.rename(f,o)

print("\nok, all scripts compiled, press any key to close")
input()

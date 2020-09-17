import os, shutil , _thread, zipfile
from tkinter import *
from tkinter import filedialog
from opencc import OpenCC

def epubs2t():
    root = Tk()
    root.withdraw()

    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

    # 获取当前文件夹路径
    current_path = os.getcwd()

    # 选择文件
    file = filedialog.askopenfilename(
        title = '選擇Epub文件',
        filetype = [('Epub電子書', '*.epub')],
        initialdir = desktop_path
        )

    # opencc t2s
    cc = OpenCC('s2t')

    # Epub解压文件夹
    # foldername是epub名，folder是文件夹名
    foldername = os.path.basename(file)
    folder = os.path.splitext(foldername)[0]

    t_foldername = cc.convert(foldername)
    t_folder = cc.convert(folder)

    # 解压Epub到同名文件夹
    unzipf = zipfile.ZipFile(file, 'r')
    unzipf.extractall(t_folder)
    unzipf.close()

    # 遍历解压的Epub文件夹里的所有文件
    def get_zip_file(input_path, result):
        files = os.listdir(input_path)
        for file in files:
            if os.path.isdir(input_path + '/' + file):
                get_zip_file(input_path + '/' + file, result)
            else:
                result.append(input_path + '/' + file)

    filelist = []
    get_zip_file(t_folder, filelist)

    # OpenCC处理文件
    convert_list = []
    for path in filelist:
        suffix = os.path.splitext(path)[1]
        text_suffix_list = ['.opf', '.ncx', '.xhtml']
        for i in text_suffix_list:
            if(i == suffix):
                convert_list.append(path)

    for path in convert_list:
        CCcmd = 'python -m opencc -c s2t -i ' + path + ' -o ' + path
        os.system(CCcmd)

    # 打包文件夹为Epub
    zipf = zipfile.ZipFile(current_path + '/' + t_foldername, 'w', zipfile.ZIP_DEFLATED)

    for file in filelist:
        zipf.write(file)

    zipf.close()
    
    shutil.rmtree(t_folder)

_thread.start_new_thread(epubs2t, ())

input()
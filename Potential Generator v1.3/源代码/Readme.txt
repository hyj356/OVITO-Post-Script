如果想要对代码进行一定程度的修改,之后再重新编译成.exe文件,首先安装python3.8以上的版本,
然后使用pip下载pyinstaller:
          pip install pyinstaller
默认的pip下载速度较慢, 建议使用国内的如清华的镜像源,通过在cmd输入如下命令设置:
          pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
在含有3个.py文件和.ico图标文件的目录下打开cmd或者powershell窗口,输入如下命令:
          pyinstaller -F -w -i gear.ico Gui_test.py
之后在生成的dist目录下可以找到对应的.exe文件,其余产生的文件均可删除.
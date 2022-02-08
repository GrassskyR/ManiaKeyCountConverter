import os
import re
import sys

def KeyConvert(osu_path):

        '''
        去掉路径中的双引号 UwU我太菜了 只能这样
        '''
        if osu_path.startswith('"') and osu_path.endswith('"'):
            osu_path = osu_path[1:-1]

        '''
        读入osu文件
        '''

        osu_files = open(osu_path,"r",encoding='UTF-8')

        osu_content = osu_files.read()

        '''
        删空 处理谱面
        '''

        if re.search(r'[^\n]*256[^\n]*\n?',osu_content,re.M)  or osu_content.find("CircleSize:7") != -1:
            osu_content = re.sub(r'[^\n]*256[^\n]*\n?','',osu_content)
            osu_content = re.sub("CircleSize:7","CircleSize:6",osu_content)
            osu_files.close()
            osu_files = open(osu_path,"w",encoding='UTF-8')
            osu_files.write(osu_content)
            print("转换完成")
        else :
            print("你打开的好像不是7K谱捏")

        osu_files.close()

'''
获取拖入程序的osu文件绝对路径
'''

osu_list = list(sys.argv)

for i in range (1,len(osu_list)) :
    try:
        KeyConvert(osu_list[i])
    except UnicodeDecodeError:
        print("请不要直接打开osz文件! >_<")
    except:
        print("Unexpected error:", sys.exc_info()[0])

if len(osu_list) == 1:
    print("请将osu文件直接拖到程序上 不要直接点开!支持拖拽多个osu文件")

os.system("pause")
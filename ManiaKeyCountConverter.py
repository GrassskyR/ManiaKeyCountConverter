import shutil
import os
import re
import sys
import tempfile
import zipfile

def OsuConvert(Map_path):

        regex = r"[^\n]*^(22[2-9]|2[3-8][0-9]|29[0-5])[^\n]*\n?"

        if Map_path.startswith('"') and Map_path.endswith('"'):     #去除路径中的双引号（如果有）
            Map_path = Map_path[1:-1]

        osu_files = open(Map_path,"r",encoding='UTF-8')     #读取osu文件

        osu_content = osu_files.read()

        if osu_content.find("Mode: 3") and osu_content.find("CircleSize:7") != -1:
            index_pos = osu_content.find('[TimingPoints]')
            end_pos = osu_content.find('\n',index_pos) + 1      #Start index of the Timing info
            timing_pos = osu_content.find('\n',end_pos)     #End index of the Timing info
            TimingInfo = osu_content[end_pos:timing_pos]    #获取Timing Info

            osu_content = re.sub(regex,'',osu_content,0,re.M)   #这个正则花了我一个多小时
            osu_content = re.sub("CircleSize:7","CircleSize:6",osu_content)     #正则删空

            if(osu_content[end_pos] == '\n'):
                osu_content = osu_content[:end_pos] + TimingInfo + osu_content[end_pos + 1:]    #防止错误替换Timing info

            osu_basename = os.path.basename(Map_path)
            osu_curdir = os.path.dirname(Map_path)
            osu_newname = "7_to_6_" + osu_basename
            New_MapPath = os.path.join(osu_curdir,osu_newname)
            print(New_MapPath)

            osu_files.close()
            osu_files = open(New_MapPath,"w",encoding='UTF-8')
            osu_files.write(osu_content)
            print("转换完成")
        else :
            print("这个谱面不是7k谱面！")

        osu_files.close()

def OszConvert(Map_path):
    print(Map_path)
    tempdir = os.path.join(os.getcwd(),"tmp")   #生成临时文件夹存放解压的osu
    oszfile = zipfile.ZipFile(Map_path,"r")
    
    oszfile.extractall(tempdir)     #解压所有文件到临时文件夹
    oszfile.close()
    
    for osufile in os.listdir(tempdir):     #遍历临时文件夹获取osu文件绝对路径
        temposufile = os.path.join(tempdir,osufile)     
        try:
            if(temposufile.endswith(".osu")):
                print(osufile)
                OsuConvert(temposufile)     #删空
        except:
            print("Unexpected error:", sys.exc_info()[0])
    
    oszfile = zipfile.ZipFile(Map_path,"w")

    for osufile in os.listdir(tempdir):
        temposufile = os.path.join(tempdir,osufile)
        oszfile.write(temposufile,osufile)     #创建新的osz文件

    oszfile.close()
    shutil.rmtree(tempdir)    #删除临时文件夹

if __name__ == "__main__":

    Map_list = list(sys.argv)   #获取拖入文件的绝对路径

    for i in range (1,len(Map_list)) :
        FilePath = Map_list[i]
        try:
            if(FilePath.endswith(".osu")):
                OsuConvert(FilePath)
            elif(FilePath.endswith(".osz")):
                OszConvert(FilePath)
                
        except:
            print("Unexpected error:", sys.exc_info()[0])

    if len(Map_list) == 1:
        print("请将osu或osz文件直接拖到程序上 不要直接点开程序！支持拖拽多个文件一起转换！")

    os.system("pause")
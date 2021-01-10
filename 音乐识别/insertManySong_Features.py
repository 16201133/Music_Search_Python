import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

from 音乐识别.语音识别.数据库 import MySQLUtil
from 音乐识别.旋律识别.MP3旋律特征 import getOneMelody
from 音乐识别.原声识别.特征数据库 import getOneBeat

# 读取txt文件，得到字符串列表
def readFile(path):
    with open(path, 'r',encoding="utf-8") as f:
        list = f.read().splitlines()
    return list

if __name__ == "__main__":
    '''
        批量添加特征数据，将songs表中没有提取特征的全部提取特征，添加到数据库中
    '''
    # 第一步、得到待提取特征的歌曲列表
    path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/manyMP3Pathes.txt"
    list = readFile(path)
    # print("待插入的列表：",list)
    # 第二步、提取旋律特征、节奏特征，得到的Features对象列表（列表-元组）
    listFeature = [] # 将特征数据存储在 [(),()] 列表-元组中
    for item in list:
        id = int(item.split(";")[0])
        address = item.split(";")[1]
        # 2.1 提取旋律特征
        melody = getOneMelody.Main(address)
        if (melody=="该文件不是MP3文件"):
            melody = ""
        # 2.2 提取节奏特征
        beat = getOneBeat.Main(address)
        if (beat=="该文件不是MP3文件"):
            beat = ""
        tuple = (id,address,melody,beat)
        listFeature.append(tuple)
    # 第三步、插入数据库
    sql = "insert into song_feature (song_id,song_address,song_melody,song_beat) values (%s,%s,%s,%s)"
    data = MySQLUtil.read_config()  # 读取数据库配置信息
    db = MySQLUtil.DBUtil(data)  # 创建对象
    db.insert_feature_many(sql=sql, list_tuple=listFeature)

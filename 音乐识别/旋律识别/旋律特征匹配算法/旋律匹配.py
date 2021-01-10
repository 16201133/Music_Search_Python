import difflib
import numpy as np
from 音乐识别.语音识别.数据库 import MySQLUtil
import 音乐识别.旋律识别.哼唱特征提取.哼唱提取特征

def Similarity_Matching(str1,str2):
    """
    字符串相似度匹配算法
    :param str1: 字符串1（字符串类型）
    :param str2: 字符串2（字符串类型）
    :return: rate相似度
    """
    # 相似度
    rate = difflib.SequenceMatcher(None,str1,str2).quick_ratio()
    return rate

def Search_Match(pitch,top_num=5):
    """
    旋律匹配，默认返回前5个相似度较高的
    :param pitch: 哼唱音高轮廓特征(字符串)
    :param top_num: 返回前top_num位，默认前5位
    :return: list歌曲列表
    """
    data = MySQLUtil.read_config() # 读取数据库配置文件
    db = MySQLUtil.DBUtil(data)    # 创建对象
    # 匹配“音高轮廓”——字符串相似度匹配
    if pitch == '':  # 判断有无 哼唱音高轮廓特征
        print("哼唱未识别出音高轮廓特征！！！")
        return None
    # 首先,查询melody表下song_melody音高轮廓不为空的所有数据
    sql = "select * from song_feature,songs where song_melody != '' and songs.song_id=song_feature.song_id"
    results = db.QueryMany_Concise(sql)
    # 然后,数据传给 搜索匹配算法 返回相似度'song_rate':0.9
    # 再将数据整理成 列表-字典 格式, 即 [{},{}]
    list = []
    if results != '':
        for item in results:
            rate = Similarity_Matching(str1=pitch,str2=item[2])
            dict = {'song_id': item[0], 'song_address': item[1],'song_name': item[5], 'song_singer': item[6], 'song_rate': rate}
            list.append(dict)
    else:
        print("song_feature特征表song_melody为空(旋律识别)")
    # 最后,返回相似度前top_num名(默认返回前5名)
    list = sorted(list, key=lambda keys:keys['song_rate'], reverse=True) # 降序：reverse=True;升序：reverse=False
    if top_num < len(list):
        list = list[:top_num]

    return list

def list_To_Str(list):
    """
    将 音高特征 转换成 相对音高特征 作为旋律表示
    :param list:一维数组(float类型)
    :return: str 相对音高轮廓(U、S、D字符串表示)
    """
    str = ""
    for i in np.arange(len(list)-1):
        compare = list[i+1]-list[i]
        if compare>0:
            str += "U"
        elif compare < 0:
            str += "D"
        else:
            str += "S"
    return str

if __name__ == "__main__":
    # 1、哼唱旋律特征提取
    filepath = "D:/Python/data/sings_data/一次就好16k.wav"  # 哼唱录制的文件路径(一次就好16k.wav)
    pitch_list = 音乐识别.旋律识别.哼唱特征提取.哼唱提取特征.get_features(filepath)  # 获取音高特征 (待修改完善？？？)
    str1 = list_To_Str(pitch_list)

    # 2、旋律匹配
    list = Search_Match(str1,top_num=5)
    print("旋律匹配结果：")
    for i in list:
        print("匹配度:{}，歌曲地址:{}".format(i['song_rate'],i['song_address']))
        # Music_Intelligent_Search

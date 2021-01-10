import numpy as np
from dtw import dtw
from numpy.linalg import norm
from 音乐识别.语音识别.数据库 import MySQLUtil
from 音乐识别.原声识别.原声片段特征提取 import original_voice_Feature

def Search_Match(list_feature,top_num=5):
    """
    原声识别匹配，默认返回前5个相似度较高的
    :param list_feature: 原声特征(list类型)
    :param top_num: 返回前top_num位，默认前5位
    :return: list歌曲列表
    """
    # 先将list_feature转换成DTW算法需要的数据
    x = np.array(list_feature).reshape(-1, 1)

    data = MySQLUtil.read_config() # 读取数据库配置文件
    db = MySQLUtil.DBUtil(data)    # 创建对象
    # 匹配“节奏”——dtw算法
    if list_feature is None:  # 判断有无 哼唱音高轮廓特征
        print("原声片段没有提取到特征！！！")
        return None
    # 首先,查询original_voice表下song_beat节奏特征不为空的所有数据
    sql = "select * from song_feature,songs where song_beat != '' and songs.song_id=song_feature.song_id"
    results = db.QueryMany_Concise(sql)
    # 然后,数据传给 搜索匹配算法 返回相似度'song_rate':0.9
    # 再将数据整理成 列表-字典 格式, 即 [{},{}]
    list = [] # 匹配结果
    if results != '':
        for item in results:
            # 列表转换成字符串（用于插入SQL数据库）
            # str_beat_frames = ','.join(str(x) for x in beat_frames)  # 通过json转换成字符串，用于写入SQL数据库
            # 将字符串 还原 列表
            beat_frames = [float(i) for i in (item[3].split(','))]  # 从数据库中的字符串 转换成 list
            y = np.array(beat_frames).reshape(-1,1)                 # 转换成dtw需要的数据格式
            rate, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
            dict = {'song_id': item[0], 'song_address': item[1], 'song_name': item[5], 'song_singer': item[6], 'song_rate': rate}
            list.append(dict)
    else:
        print("song_feature特征表的song_beat为空(原声识别)")
    # 最后,返回相似度前top_num名(默认返回前5名)
    list = sorted(list, key=lambda keys:keys['song_rate'], reverse=False) # 降序：reverse=True;升序：reverse=False
    if top_num < len(list):
        list = list[:top_num]

    return list

if __name__ == "__main__":
    # 1、原声特征提取
    # filepath = "D:/Python/PyCharm/workspace/Learning/原声识别/data/recording.wav" # 原声录制（有杂音）
    filepath = "D:/Python/PyCharm/workspace/Learning/原声识别/data/原声片段.wav" # 原声片段
    list = original_voice_Feature.get_Original_Voice_Feature(filepath)

    # 2、旋律匹配
    results = Search_Match(list, top_num=15) # 返回前5名
    print("旋律匹配结果：")
    for i in results:
        print("匹配度:{}，歌曲地址:{}".format(i['song_rate'], i['song_address']))
import difflib
from 音乐识别.语音识别.数据库 import MySQLUtil

# 搜索匹配
def Search_Match(Speech_Recognition,top_num=5):
    """
    搜索匹配，默认返回前5个相似度较高的
    :param Speech_Recognition: 语音识别的文字(字符串)
    :param top_num: 返回前top_num位，默认前5位
    :return: list歌曲列表
    """
    list = [] # 返回的结果

    data = MySQLUtil.read_config()
    db = MySQLUtil.DBUtil(data)  # 创建对象
    if Speech_Recognition == '':  # 判断有无 语音识别结果
        print("语音输入为空|没有声音信号源")
        return None
    # 1、匹配“歌名”
    claim = {'song_name':Speech_Recognition[:-1]}  # (eg.“光辉岁月。” 删除最后的标点符号)
    results = db.QueryMany(tablename="songs",claim=claim)
    if results != '':
        i = 0
        for item in results:
            i += 1
            rate = Similarity_Matching(Speech_Recognition=Speech_Recognition, song_lyrics=item[3])
            dict = {'song_id': item[0], 'song_name': item[1], 'song_singer': item[2], 'song_lyrics': item[3],
                    'song_address': item[6], 'song_rate': rate}
            list.append(dict)
        # 最后,返回相似度前top_num名(默认返回前5名)
        list = sorted(list, key=lambda keys: keys['song_rate'], reverse=True)  # 降序：reverse=True;升序：reverse=False
        list = list[:top_num]
        return list

    # 2、匹配“歌手”
    claim = {'song_singer': Speech_Recognition[:-1]}
    results = db.QueryMany(tablename="songs", claim=claim)
    if results != '':
        i = 0
        for item in results:
            i += 1
            rate = Similarity_Matching(Speech_Recognition=Speech_Recognition, song_lyrics=item[3])
            dict = {'song_id': item[0], 'song_name': item[1], 'song_singer': item[2], 'song_lyrics': item[3],
                    'song_address': item[6], 'song_rate': rate}
            list.append(dict)
        # 最后,返回相似度前top_num名(默认返回前5名)
        list = sorted(list, key=lambda keys: keys['song_rate'], reverse=True)  # 降序：reverse=True;升序：reverse=False
        list = list[:top_num]
        return list
    # 3、匹配“歌词”——字符串相似度匹配
    # 首先,查询songs表下lyrics歌词不为空的所有数据
    sql = "select * from songs where song_lyrics != ''"
    results = db.QueryMany_Concise(sql)
    # print("歌词不为空的歌曲：",results)
    # 然后,数据传给 搜索匹配算法 返回相似度'song_rate':0.9
    # 再将数据整理成 列表-字典 格式, 即 [{},{}]
    if results != '':
        i = 0
        for item in results:
            i+=1
            rate = Similarity_Matching(Speech_Recognition=Speech_Recognition,song_lyrics=item[3])
            dict = {'song_id': item[0], 'song_name': item[1], 'song_singer': item[2], 'song_lyrics': item[3],
                    'song_address': item[6], 'song_rate': rate}
            list.append(dict)
        # 最后,返回相似度前top_num名(默认返回前5名)
        list = sorted(list, key=lambda keys:keys['song_rate'], reverse=True) # 降序：reverse=True;升序：reverse=False
        list = list[:top_num]
        return list

def Similarity_Matching(Speech_Recognition,song_lyrics):
    """
    字符串相似度匹配算法
    :param Speech_Recognition: 语音识别（字符串类型）
    :param song_lyrics: 歌词（字符串类型）
    :return: rate相似度
    """
    # 相似度
    rate = difflib.SequenceMatcher(None,Speech_Recognition,song_lyrics).quick_ratio()
    return rate


if __name__ == "__main__":
    # 语音识别出来的文字
    Speech_Recognition = "年月把拥有变做失去"
    print("语音信号：",Speech_Recognition)
    # 返回相似度最高的 前2名
    result = Search_Match(Speech_Recognition=Speech_Recognition, top_num=2)
    print("匹配结果：",result)
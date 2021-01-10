import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

from 音乐识别.语音识别.MP3 import 解析MP3
from 音乐识别.语音识别.数据库 import MySQLUtil
from 音乐识别.语音识别.歌曲搜索匹配算法 import 搜索匹配

def read_file(filepath):
    str = ""
    with open(filepath, 'r', encoding='utf-8') as read:
        lines = read.readlines()  # 整行读取数据
        for line in lines:
            if line:
                str += line
    return str

if __name__ == "__main__":
    # 第1步：获取MP3歌曲数据,并构建songs表
    '''
    path = "D:/Python/data/MP3_data/"
    file_type = "*.mp3"
    mp3List, notMp3List = 解析MP3.listDirectory(path, file_type)
    print("MP3列表:", mp3List)
    insert_list = []
    for i in mp3List:
        item = 解析MP3.GetMp3Info(i) # 返回字典类型
        tuple = (item['title'],item['artist'],item['lyrics'],item['address'])
        insert_list.append(tuple)
    # 插入歌曲数据
    sql = "insert into songs (song_name, song_singer, song_lyrics, song_address) values (%s,%s,%s,%s)"
    print("待插入的歌曲信息列表:",insert_list)
    data = MySQLUtil.read_config() # 读取数据库配置信息
    print("MySQL数据库:",data)
    db = MySQLUtil.DBUtil(data)    # 创建对象
    db.operate_dateByCount(sql=sql,count=insert_list)  # 插入数据(批量)
    '''

    # 第2步：语音识别：输入语音,识别用户输入的语音
    #       歌曲识别：讯飞API识别不准确(暂不采用)

    # Mp3 转换为 16k 16bit 单声道 pcm（使用ffmpeg工具转换 符合讯飞需求的pcm格式音频）
    # os.system(
    #     "ffmpeg -y -f s16le -ar 48000 -ac 1 -i D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.pcm -acodec pcm_s16le -f s16le -ac 1 -ar 16000 D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.pcm")
    # os.system(
    #     "ffmpeg -y -i D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.mp3 -acodec pcm_s16le -f s16le -ac 1 -ar 16000 D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.pcm")

    print("开始运行语音识别...")
    # 语音识别
    os.system("python D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/语音识别Demo.py")
    # 读取语音识别的文字结果
    Speech_Recognition = read_file("D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/result.txt")
    # 第3步：歌曲匹配算法,通过“歌名、歌手、歌词”等信息 进行 搜索匹配数据库中的歌曲
    list = 搜索匹配.Search_Match(Speech_Recognition)
    print("语音识别结果：",list)

    # 测试单首歌曲插入
    # path = "D:/Python/data/MP3_data/Beyond - 光辉岁月.mp3"
    # bools,flag = 解析MP3.isMp3Format(path) # 判断是否属于MP3格式
    # dict = {}
    # if bools == True:
    #     if flag == 1:
    #         dict.update({'ID3V1': path})
    #     elif flag == 2:
    #         dict.update({'ID3V2': path})
    #     else:
    #         dict.update({'frame': path})
    # else:
    #     print("不是MP3格式")
    # item = 解析MP3.GetMp3Info(dict)  # 返回字典类型
    # tuple = (item['title'],item['artist'],item['lyrics'])
    # data = MySQLUtil.read_config() # 读取mysql配置文件
    # db = MySQLUtil.DBUtil(data)    # 创建数据库工具类对象
    # sql = "insert into songs (song_name, song_singer, song_lyrics) values (%s,%s,%s)"
    # db.operate_dateByCount(sql=sql, count=tuple)  # 插入数据(单首歌曲)

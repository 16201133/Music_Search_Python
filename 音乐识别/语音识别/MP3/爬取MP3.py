import requests
import re
from multiprocessing import Pool
import urllib

headers = {
    'Referer': 'https://music.163.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 "
                  "Safari/537.36"
}


def get_page(url):
    res = requests.get(url, headers=headers)
    data = re.findall('<a title="(.*?)" href="/playlist\?id=(\d+)" class="msk"></a>', res.text)
    print(data)

    pool = Pool(processes=4)
    pool.map(get_songs, data[:len(data) - 1])
    print("下载完毕！")


def get_songs(data):
    print(data[1])
    playlist_url = "https://music.163.com/playlist?id=%s" % data[1]
    res = requests.get(playlist_url, headers=headers)
    for i in re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res.text):

        try:
            print(i)
            print("Downing--" + i[1])
            ID = i[0]
            url = 'https://music.163.com/song/media/outer/url?id='
            req = requests.get(url + ID, headers=headers, allow_redirects=False)
            musicLink = req.headers['Location']
            urllib.request.urlretrieve(musicLink, 'D:/Python/data/MP3_data/' + i[1] + '.mp3')
            print("Dend Downing + " + i[1])

        except FileNotFoundError:
            pass
        except OSError:
            pass


if __name__ == '__main__':
    # hot_url = "https://music.163.com/discover/playlist/?order=hot"
    for i in range(0, 100000000, 35):
        hot_url = 'https://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' + str(i)
        get_page(hot_url)
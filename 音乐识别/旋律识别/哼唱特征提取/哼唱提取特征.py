# 导入Librosa模块
import librosa
import librosa.display
# 导入 滤波器
from scipy import signal
# 导入 python_speech_features 模块
from python_speech_features.sigproc import preemphasis
import matplotlib.pyplot as plt
import numpy as np
import math

# 巴特沃斯滤波器（高通、低通、带通、带阻）
def butter_filter(N,lowcut,highcut,fs,btype,data):
    """
    实现 巴特沃斯滤波器
    N:滤波器的阶数()
    lowcut:需滤除的低频率
    highpass:需滤除的高频率
    fs:采样频率
    btype:类型(高通highpass、低通lowpass、带通bandpass、带阻bandstop)
    data:数据
    :return: data
    """
    # Wn：归一化截止频率。计算公式Wn=2*截止频率/采样频率。当构造带通滤波器或者带阻滤波器时，Wn为长度为2的列表。
    # 这里假设采样频率为1000hz,信号本身最大的频率为500hz,要滤除10hz以下和400hz以上频率成分,即截至频率为10hz和400hz,则wn1=2*10/1000=0.02,wn2=2*400/1000=0.8。Wn=[0.02,0.8]
    low_Wn = 2*lowcut/fs
    high_Wn = 2*highcut/fs
    if btype == 'lowpass':       # 1、滤除高频,取中低频
        b,a = signal.butter(N,high_Wn,btype)
        data = signal.filtfilt(b,a,data)  # data为要过滤的信号
    elif btype == 'highpass':    # 2、滤除高频,取中低频
        b, a = signal.butter(N, low_Wn, btype)
        data = signal.filtfilt(b, a, data)
    elif btype == 'bandpass':    # 3、滤除高低频,取中间频
        b, a = signal.butter(N, [low_Wn,high_Wn], btype)
        data = signal.filtfilt(b, a, data)
    else:                        # 4、删除中间频,取高低频
        b, a = signal.butter(N, [low_Wn,high_Wn], btype)
        data = signal.filtfilt(b, a, data)
    return data

def show_wav(path):
    """
    显示wav文件的各属性信息
    :return: 属性信息
    """
    data, fs = librosa.load(path, sr=None)
    print("采样频率：",fs)
    print("wav文件类型：",data.dtype)
    print("采样点数和通道数：", data.shape)
    return None

def plt_wave(path):
    """
    绘制声音的波形图(单通道)
    :return:None
    """
    """
    load(path,[sr,mono,offset,duration])函数功能：
    读取音频文件,path是音频文件路径,其他参数：
    sr:采频率(默认22050,但是有重采样功能,设置为None会以原始采频率读取音频文件);
    mono:设置为true是单通道,否则是双通道;
    offset:音频读取时间;
    duration:获取音频时长
    """
    data,sr = librosa.load(path,sr=None) # sr设置为原始采频率
    plt.figure()
    librosa.display.waveplot(data,sr)
    plt.title("波形图",fontproperties='STKAITI',fontsize=15)
    plt.xlabel('Time')       # 时间
    plt.ylabel('Amplitude')  # 振幅
    plt.show()
    return None

def enframe(signals,wlen,inc,window):
    """
    将音频信号转化为为 帧并加窗(分帧加窗)
    参数含义：
    signals:原始音频信号
    wlen:帧长(采样频率 * 时间间隔)
    inc:帧移(相邻帧的间隔)
    window:加窗
    :return:帧信号矩阵
    """
    signal_len = signals.size # 信号总长度
    if signal_len<=wlen:      # 若信号长度小于一个帧的长度，则帧数定义为1
        nf = 1
    else:                     # 否则，计算帧的总长度
        nf = int(np.ceil((1.0*signal_len-wlen+inc)/inc))
    pad_length = int((nf - 1) * inc + wlen)        # 所有帧加起来总的铺平后的长度
    zeros = np.zeros((pad_length - signal_len,))   # 不够的长度使用0填补，类似于FFT中的扩充数组操作
    pad_signal = np.concatenate((signals, zeros))  # 填补后的信号记为pad_signal
    indices = np.tile(np.arange(0, wlen), (nf, 1)) + np.tile(np.arange(0, nf * inc, inc), (wlen, 1)).T  # 相当于对所有帧的时间点进行抽取，得到nf*nw长度的矩阵
    indices = np.array(indices, dtype=np.int32)    # 将indices转化为矩阵
    frames = pad_signal[indices]    # 得到帧信号
    # win = np.tile(window, (nf, 1))  # window窗函数，这里默认取1
    return frames*window   #返回帧信号矩阵

def plt_frame(Frame, n, wlen, fs):
    """
    绘制 分帧加窗 后的 单帧的图像
    参数含义：
    Frame：音频分帧后的矩阵数据
    n：表示音频的第n帧
    wlen：帧长
    :return: None
    """
    data1 = np.reshape(Frame, (1, -1))[0]
    time = np.arange(0, len(data1)) * (1.0 / fs)
    cur_time = np.arange(0, wlen) * (1.0 / fs)   # 分帧数据
    num = Frame.shape[0]
    if 0 <= n < num:
        data2 = Frame[n]
        plt.figure(figsize=(10, 4))
        plt.subplot(3,1,1)
        plt.plot(time, data1, c='g')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title("分帧加窗图", fontproperties='STKAITI', fontsize=10)
        plt.grid()

        plt.subplot(3, 1, 3)
        plt.plot(cur_time, data2, c="g")
        plt.xlabel('Time')       # 时间
        plt.ylabel('Amplitude')  # 振幅
        plt.title("第{}帧的图".format(n), fontproperties='STKAITI', fontsize=10)
        plt.grid()

        plt.show()
    else:
        print("\033[1;31m参数n范围在[0~%d]之间\033[0m!" % num)
    return None

def pick_peaks(arr):
    """
    求峰值(除去两端端点)
    :param arr: 一维数组
    :return: pos坐标位置；peaks各个峰值
    """
    pos = []
    peaks = []
    for i in range(0,len(arr)):
        if i == 0 or i == len(arr)-1:
            pass
        elif arr[i] > arr[i-1] and arr[i] > arr[i+1]:
            pos.append(i)
            peaks.append(arr[i])
        elif arr[i] > arr[i-1] and arr[i] == arr[i+1]:
            for j in range(i,len(arr)):
                if arr[j] < arr[i]:
                    pos.append(i)
                    peaks.append(arr[i])
                if arr[j] != arr[i]:
                    i = j
                    break
    return {"pos":pos,"peaks":peaks}

def get_pitch(rate):
    """
    根据基音频率 求得 音高
    :param rate: 基音频率
    :return: 音高
    """
    pitch = 69 + math.log(rate/440,2)
    return pitch

def get_pitch_list(Peak_values,fs):
    """
    根据基音周期 提取 音高序列
    :param Peak_values: 基音周期 列表[]
    :param fs: 采样率
    :return: 音高序列 pitch_list
    """
    frames = len(Peak_values) # 帧数
    pitch_list = [] # 音高序列列表
    for n in np.arange(frames):
        pos = Peak_values[n]
        rate = fs/pos # 第n帧的基音频率
        pitch = 69 + math.log(rate/440,2) # 第n帧的音高值
        pitch_list.append(pitch)
    return pitch_list

def get_Peak_values(data):
    """
    获取所有帧的 基音周期列表
    :param data:帧数据，多维数组[[],[],[]]
    :return:基音周期列表 Peak_values
    """
    frames = data.shape[0]  # 帧数
    Peak_values = []  # 基音周期列表(峰值)
    for n in np.arange(frames):
        peaks = pick_peaks(data[n])  # 获取第n帧峰值信息
        pos = peaks['pos'][0]  # 第n帧的基音周期(峰值)        (?存在小疑惑?)共振峰影响、求每个峰的平均值
        Peak_values.append(pos)
    return Peak_values

def calEnergy(frames):
    """
    求短时能量
    :param frames:所有帧数据
    :return: 短时能量列表、平均短时能量
    """
    energy_list = [] # 短时能量列表
    frames = np.square(frames)
    for i in np.arange(frames.shape[0]):
        energy_list.append(sum(frames[i]))
    energy_avg = np.mean(energy_list) # 平均短时能量
    return energy_list,energy_avg

def mute_filter(frames,energy_list,energy_avg):
    """
    过滤静音段————(短时能量用于区分清音浊音)
    :param frames: 所有帧数据
    :param energy_list: 短时能量列表
    :param energy_avg: 平均短时能量
    :return: Frames帧数据
    """
    threshold = 0.3*energy_avg # 设置阈值，低于threshold的属于静音段,因此滤除该帧
    new_frames = []
    for i in np.arange(frames.shape[0]):
        if energy_list[i] > threshold: # 筛选出浊音段
            new_frames.append(list(frames[i]))
    new_frames = np.array(new_frames)
    return new_frames

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

# 提取音高、音长特征
def get_features(filepath):
    # 1、读取音频
    # load读取音频文件,返回 data为数据 与 fs为采样频率
    data, fs = librosa.load(filepath, sr=None)  # 一次就好16k.wav
    # 显示各种信息
    # show_wav("D:/Python/data/sings_data/一次就好16k.wav")
    # plt_wave("D:/Python/data/sings_data/一次就好16k.wav")

    # 2、预处理————音频去噪
    # 带通滤波处理(bandpass:带通滤波;highpass:高通滤波;lowpass:低通滤波)
    butter_data = butter_filter(4, 60, 1000, fs, 'bandpass', data)  # ???选取60~1000???

    # 3、预加重(一阶数字滤波器——差分方程实现)
    # 目的：为了对语音的高频部分进行加重,去除口唇辐射的影响,增加语音的高频分辨率。
    # 使用preemphasis(data, coeff=0.95) 默认coeff=0.95
    signals = preemphasis(butter_data, coeff=0.97)
    '''
    # 类型转换(signals的类型float64;data的类型float32)
    signals = np.asfortranarray(signals)  # 返回在内存中以Fortran顺序布局的数组
    butter_data = np.asfortranarray(butter_data)
    # 原始图 和 去噪后的图 对比
    plt.figure()  # 创建图形
    plt.subplot(3, 2, 1)  # 3*2的矩阵图,也就是总共有4个图,1就代表了第一幅图
    librosa.display.waveplot(data, fs)
    plt.xlabel('Time')  # 时间
    plt.ylabel('Amplitude')  # 振幅
    plt.title("原始图", fontproperties='STKAITI', fontsize=10)
    plt.grid()  # 标尺

    plt.subplot(3, 2, 2)  # 3*2的矩阵图,也就是总共有4个图,1就代表了第一幅图
    librosa.display.waveplot(butter_data, fs)
    plt.xlabel('Time')  # 时间
    plt.ylabel('Amplitude')  # 振幅
    plt.title("去噪的图", fontproperties='STKAITI', fontsize=10)
    plt.grid()  # 标尺

    plt.subplot(3, 2, 5)  # 3*2的矩阵图,也就是总共有4个图,1就代表了第一幅图
    librosa.display.waveplot(signals, fs)
    plt.xlabel('Time')  # 时间
    plt.ylabel('Amplitude')  # 振幅
    plt.title("去噪与预加重后的图", fontproperties='STKAITI', fontsize=10)
    plt.grid()  # 标尺

    plt.show()
    '''
    # 4、加窗分帧
    wlen = int(0.025 * fs)  # 帧长25ms,也就是fs*0.025=400采样点(采样率fs为16000)
    inc = int(0.01 * fs)  # 帧移10ms,也就是fs*0.01=160的重叠
    # window = signal.windows.hann(wlen)  # 汉宁窗
    window = signal.windows.hamming(wlen)  # 汉明窗
    Frame = enframe(signals, wlen, inc, window)
    N = 20  # 帧数
    # 画出分帧加窗后 第20帧 图像
    # plt_frame(Frame, N, wlen, fs)
    # 5、过滤静音段(区分清音和浊音)————短时能量、短时平均幅度的有作用主要是：作为区分清浊音，区分声母韵母，区分有话段和无话段的指标。
    energy_list,energy_avg = calEnergy(Frame)
    new_Frame = mute_filter(Frame,energy_list,energy_avg) # 过滤静音段
    print("过滤了{}帧清音段，剩余{}帧浊音段".format((Frame.shape[0]-new_Frame.shape[0]),new_Frame.shape[0]))

    # 6、提取基音周期————自相关函数(？？？易受到共振峰的影响？？？)
    # (???提取不准确???)参考：http://www.doc88.com/p-3962314591949.html
    # 音高、音长的提取：http://www.doc88.com/p-9455402201799.html
    ac = librosa.autocorrelate(new_Frame)
    # 图形显示
    # plt.subplot(3, 1, 1)
    # plt.plot(new_Frame[N])
    # plt.title("第{}帧原图".format(N), fontproperties='STKAITI', fontsize=10)
    # plt.xlabel('Lag (frames)')
    #
    # plt.subplot(3, 1, 3)
    # plt.plot(ac[N])
    # plt.title('自相关函数', fontproperties='STKAITI', fontsize=10)
    # plt.xlabel('Lag (frames)')
    #
    # plt.show()

    # 求第20帧数据的 峰值位置(即基音周期)
    # peaks = pick_peaks(ac[N])
    # print(peaks)
    # pos = peaks['pos'][0]
    # print("该帧中的峰值位置：", pos)  # ？？？求平均值 ？？？
    # print("该帧的频率：{:.2f} Hz".format(fs / pos))
    # print("该帧的音高：", get_pitch(fs / pos))

    # 获取各帧的 基音周期列表
    Peak_values = get_Peak_values(ac)  # 获得基音周期列表

    # 7、基音检测后处理————由于峰值检测提取频率时会存在一些偏差，需要滤除“野点”
    # 方法：（中值平滑处理、线性平滑处理）
    # 7.1、中值平滑处理(3点平滑) ————？？？？效果令人质疑？？？？
    Peak_values_new = signal.medfilt(Peak_values, 3) # 设置窗口为3，3点平滑
    # 7.2、显示对比图像      (存在的问题：？？？出现半频、半频错误，提取的基音周期不准确？？？)
    # plt.subplot(3, 1, 1)
    # plt.plot(Peak_values[500:600],'ro',markersize='1') # 设置图像显示为红点，大小为 5   #,'ro',markersize='1'
    # plt.title("未平滑处理的基音周期(区间[300:400])", fontproperties='STKAITI', fontsize=10)
    # plt.xlabel('帧数', fontproperties='STKAITI', fontsize=10)
    # plt.ylabel('基音周期', fontproperties='STKAITI', fontsize=10)
    #
    # plt.subplot(3, 1, 3)
    # plt.plot(Peak_values_new[500:600],'ro',markersize='1') # ,'ro',markersize='1'
    # plt.title('中值平滑处理后(区间[300:400])', fontproperties='STKAITI', fontsize=10)
    # plt.xlabel('帧数', fontproperties='STKAITI', fontsize=10)
    # plt.ylabel('基音周期', fontproperties='STKAITI', fontsize=10)
    #
    # plt.show()

    # 8、提取特征
    # 8.1、获得音高特征序列
    pitch_list = get_pitch_list(Peak_values_new,fs) # 未做中值平滑处理时，得到的音高特征
    # 8.2、获得音长特征序列

    return pitch_list

if __name__ == "__main__":
    # 哼唱旋律特征提取
    filepath = "D:\Python\PyCharm\workspace\智能音乐搜索\音乐识别\旋律识别\data\\recording.wav" # 哼唱录制的文件路径(一次就好16k.wav)
    pitch_list = get_features(filepath) # 获取音高特征 (待修改完善？？？)
    print("音高序列：", pitch_list)

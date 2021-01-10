import pyaudio # 这个需要自己下载轮子
import wave

def get_audio(filepath,time=8):
    """
    声音录制
    :param filepath: 录制后存储路径
    :param time: 录制时长，默认为 8
    :return: None
    """
    # in_path = "D:/Python/PyCharm/workspace/Learning/语音识别/讯飞API/data/"  # 存放录音的路径
    aa = str(input("是否开始录音？   （y/n）"))
    if aa == str("y") :
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 采样率
        RECORD_SECONDS = time       # 录音时间
        # WAVE_OUTPUT_FILENAME = in_path + filename+".wav"
        WAVE_OUTPUT_FILENAME = filepath
        in_path = WAVE_OUTPUT_FILENAME
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*5, "开始录音：请在{}秒内输入语音".format(time), "*"*5)
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*5, "录音结束\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str("否"):
        exit()
    else:
        print("语音录入失败，请重新开始")
        get_audio(filepath)
    return None


import vosk
import wave
import sys
import pyaudio  # 实时识别需装，pip install pyaudio

# 初始化Vosk中文小模型（自动下载，无需手动放路径）
model = vosk.Model(lang="cn")
sample_rate = 16000

# 方式1：识别本地音频文件（任务二的voice_clone.mp3，需转WAV，下方附转码方法，超简单）
def recognize_audio(file_path):
    wf = wave.open(file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomprehension() != 0:
        print("请将音频转为16bit单声道WAV格式")
        return
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print("本地音频识别结果：", rec.Result())
    print("本地音频最终识别结果：", rec.FinalResult())

# 方式2：麦克风实时识别
def recognize_mic():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=8000)
    stream.start_stream()
    rec = vosk.KaldiRecognizer(model, sample_rate)
    rec.SetWords(True)
    print("已开启麦克风实时识别，说话即可，按Ctrl+C退出")
    try:
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print("实时识别结果：", rec.Result())
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("实时识别已退出")

# 主函数：先运行本地音频识别，再运行实时识别
if __name__ == "__main__":
    # 替换为你的音频文件路径（WAV格式）
    audio_file = "voice_clone.wav"
    print("===== 开始识别本地音频 =====")
    recognize_audio(audio_file)
    print("===== 本地音频识别完成，开始实时识别 =====")
    recognize_mic()

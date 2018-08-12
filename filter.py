from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin,freqz
from pylab import figure, plot, grid, show
import  librosa
import matplotlib.pyplot as plt
import librosa.display
import librosa.output
import numpy as np
import os
import wave


#you should install ffmpeg packet

is_real_wav=False
# 如果是官方的真确wav则是true
# 如果是自己的wav不能用库去读取，需要自己写的去读取，所以是false
filt_dir='wav/'
filt_store_dir='wav1/'
Cutoff_hz = [10.0,1000.0]
# Cutoff_hz = 1000
Numtaps = 499
Sample_rate=16000

def filt_wav_store(dir,filename,filt_store_dirs):
    print(filename)
    X, sample_rate = librosa.load(dir+filename)
    nyq_rate = sample_rate / 2.
    fir_coeff = firwin(Numtaps, Cutoff_hz / nyq_rate)
    filtered_X = lfilter(fir_coeff, 1.0, X)
    librosa.output.write_wav(filt_store_dir+filename, filtered_X, sample_rate, norm=True)

def filt_dir_all_wav(dir,filt_store_dir):
    if not os.path.exists(filt_store_dir):
        os.mkdir(filt_store_dir)
    for file in os.listdir(dir):
        filt_wav_store(dir,file,filt_store_dir)


def wav_open(filename):
    # -*- coding: utf-8 -*-
    import wave
    import numpy
    import pylab as pl

    # 打开wav文件
    # open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据

    f = wave.open(filename, "rb")

    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
    # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    # 读取波形数据
    # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
    str_data = f.readframes(nframes)
    f.close()

    # 将波形数据转换成数组
    # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    wave_data = numpy.fromstring(str_data, dtype=numpy.uint8)/255

    wave_data.shape = -1
    # # wave_data = wave_data.T
    # time = numpy.arange(0, nframes) * (1.0 / framerate)
    # # len_time = int(len(time) / 2)
    # # time = time[0:len_time]
    #
    # ##print "time length = ",len(time)
    # ##print "wave_data[0] length = ",len(wave_data[0])
    #
    # # 绘制波形
    #
    # pl.subplot(211)
    # pl.plot(time, wave_data)
    # # pl.subplot(212)
    # # pl.plot(time, wave_data[1], c="r")
    # pl.xlabel("time")
    # pl.show()

    return wave_data

def wav_save(file_name,wave_data):

    f = wave.open(file_name, "wb")
    # set wav params
    f.setnchannels(1)
    f.setsampwidth(1)
    f.setframerate(Sample_rate)
    # turn the data to string
    f.writeframes(wave_data.tostring())
    f.close()


def filter_wav_test(filename):
    if is_real_wav:
        X, sample_rate = librosa.load(filename,sr=Sample_rate)
    else:
        X=wav_open(filename)
        sample_rate=Sample_rate
    librosa.output.write_wav(filename.replace('.wav', 'save.wav'), X,Sample_rate,norm=False)
    nyq_rate = sample_rate / 2.
    cutoff_hz = Cutoff_hz
    # Length of the filter (number of coefficients, i.e. the filter order + 1)
    numtaps = Numtaps
    # Use firwin to create a lowpass FIR filter
    band=[i/ nyq_rate for i  in cutoff_hz ]
    fir_coeff = firwin(numtaps, band,pass_zero=False)

    w, h = freqz(fir_coeff)
    plt.title('Digital filter frequency response')
    plt.plot(w*nyq_rate/pi, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude [dB]', color='b')
    # plt.xlabel('Frequency [rad/sample]')
    plt.xlabel('Frequency [HZ]')
    plt.grid()
    plt.axis('tight')
    plt.xlim(0, 2000)
    plt.show()


    filtered_X = lfilter(fir_coeff, 1.0, X)

    librosa.output.write_wav(filename.replace('.wav','filt.wav'),filtered_X,sr=sample_rate,norm=True)

    D = librosa.stft(X.astype(np.float))
    D1 = librosa.stft(filtered_X)
    # Use left-aligned frames, instead of centered frames
    D_left = librosa.stft(X.astype(np.float), center=False)
    # Use a shorter hop length
    D_short = librosa.stft(filtered_X, hop_length=64)
    # Display a spectrogram
    librosa.display.specshow(librosa.amplitude_to_db(librosa.magphase(D)[0],np.max),y_axis='log', x_axis='time')
    plt.title('Power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()
    librosa.display.specshow(librosa.amplitude_to_db(librosa.magphase(D1)[0],np.max),y_axis='log', x_axis='time')
    plt.title('Power spectrogram after filted')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()


def filter_test():
    # ------------------------------------------------
    # Create a signal for demonstration.
    # ------------------------------------------------
    # 320 samples of (1000Hz + 15000 Hz) at 48 kHz
    sample_rate = 48000.
    nsamples = 320

    F_1KHz = 1000.
    A_1KHz = 1.0

    F_15KHz = 15000.
    A_15KHz = 0.5

    t = arange(nsamples) / sample_rate
    signal = A_1KHz * sin(2 * pi * F_1KHz * t) + A_15KHz * sin(2 * pi * F_15KHz * t)

    # ------------------------------------------------
    # Create a FIR filter and apply it to signal.
    # ------------------------------------------------
    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.

    # The cutoff frequency of the filter: 6KHz
    cutoff_hz = 6000.0

    # Length of the filter (number of coefficients, i.e. the filter order + 1)
    numtaps = 29

    # Use firwin to create a lowpass FIR filter
    fir_coeff = firwin(numtaps, cutoff_hz / nyq_rate)

    # Use lfilter to filter the signal with the FIR filter
    filtered_signal = lfilter(fir_coeff, 1.0, signal)


    # ------------------------------------------------
    # Plot the original and filtered signals.
    # ------------------------------------------------

    # The first N-1 samples are "corrupted" by the initial conditions
    warmup = numtaps - 1

    # The phase delay of the filtered signal
    delay = (warmup / 2) / sample_rate

    figure(1)
    # Plot the original signal
    plot(t, signal,'b')

    # Plot the filtered signal, shifted to compensate for the phase delay
    plot(t - delay, filtered_signal, 'r-')

    # Plot just the "good" part of the filtered signal.  The first N-1
    # samples are "corrupted" by the initial conditions.
    plot(t[warmup:] - delay, filtered_signal[warmup:], 'g', linewidth=4)

    grid(True)
    figure(2)
    plot(t[warmup:] - delay, filtered_signal[warmup:], 'g', linewidth=4)
    # figure(3)
    plot(t , filtered_signal, 'r-')
    show()

    print_values('signal', signal)
    print_values('fir_coeff', fir_coeff)
    print_values('filtered_signal', filtered_signal)

# ------------------------------------------------
# Print values
# ------------------------------------------------
def print_values(label, values):
    var = "float32_t %s[%d]" % (label, len(values))
    print("%-30s = {%s}" % (var, ', '.join(["%+.10f" % x for x in values])))



#
# def waveletSmooth(x, wavelet="db4", level=1, title=None):
#     # calculate the wavelet coefficients
#     coeff = pywt.wavedec(x, wavelet, mode="per")
#     # calculate a threshold
#     sigma = mad(coeff[-level])
#     # changing this threshold also changes the behavior,
#     # but I have not played with this very much
#     uthresh = sigma * np.sqrt(2 * np.log(len(x)))
#     coeff[1:] = (pywt.threshold(i, value=uthresh, mode="soft") for i in coeff[1:])
#     # reconstruct the signal using the thresholded coefficients
#     y = pywt.waverec(coeff, wavelet, mode="per")
#     f, ax = plt.subplots()
#     plot(x, color="b", alpha=0.5)
#     plot(y, color="b")
#     if title:
#         ax.set_title(title)
#     ax.set_xlim((0, len(y)))

if __name__=='__main__':
    # filter_wav_test('wav/normal__201105011626.wav')
    # filt_dir_all_wav(filt_dir,filt_store_dir)
    # X = wav_open('2018-08-11 11_16_19.wav')
    # print(librosa.util.normalize([-4.0,0.0 , 1.0]))
    filter_wav_test('2018-08-11 21_35_29.wav')
    filter_wav_test('normal_0112filt.wav')
    # wav_open('2018-08-11 11_16_19.wav')s
    filter_wav_test('/home/lechatelia/Desktop/Codes/dataset2/filt/extrastole/extrastole_0001filt.wav')

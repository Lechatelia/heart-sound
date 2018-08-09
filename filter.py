from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin,freqz
from pylab import figure, plot, grid, show
import  librosa
import matplotlib.pyplot as plt
import librosa.display
import librosa.output
import numpy as np
import os

# import pywt
# import numpy as np
# import seaborn
# from statsmodels.robust import mad

#you should install ffmpeg packet

filt_dir='wav/'
filt_store_dir='wav1/'
Cutoff_hz = 1000.0
Numtaps = 1000

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







def filter_wav_test(filename):
    X, sample_rate = librosa.load(filename)
    nsamples=29
    nyq_rate = sample_rate / 2.
    cutoff_hz = 1000.0
    # Length of the filter (number of coefficients, i.e. the filter order + 1)
    numtaps = 100
    # Use firwin to create a lowpass FIR filter
    fir_coeff = firwin(numtaps, cutoff_hz / nyq_rate)

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

    # Use lfilter to filter the signal with the FIR filter
    filtered_X = lfilter(fir_coeff, 1.0, X)
    librosa.output.write_wav(filename.replace('.wav','filt.wav'),filtered_X,sample_rate,norm=True)

    D = librosa.stft(X)
    D1 = librosa.stft(filtered_X)
    # Use left-aligned frames, instead of centered frames
    D_left = librosa.stft(X, center=False)
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
    plot(t, signal)

    # Plot the filtered signal, shifted to compensate for the phase delay
    plot(t - delay, filtered_signal, 'r-')

    # Plot just the "good" part of the filtered signal.  The first N-1
    # samples are "corrupted" by the initial conditions.
    plot(t[warmup:] - delay, filtered_signal[warmup:], 'g', linewidth=4)

    grid(True)

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
    filter_wav_test('2018-08-09 13_39_27.wav')
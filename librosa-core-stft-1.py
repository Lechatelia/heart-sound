import numpy as np
import librosa
import librosa.display

y, sr = librosa.load('dataset/artifact__201012172012.wav')
D = librosa.stft(y)
# array([[  2.576e-03 -0.000e+00j,   4.327e-02 -0.000e+00j, ...,
# 3.189e-04 -0.000e+00j,  -5.961e-06 -0.000e+00j],
# [  2.441e-03 +2.884e-19j,   5.145e-02 -5.076e-03j, ...,
# -3.885e-04 -7.253e-05j,   7.334e-05 +3.868e-04j],
# ...,
# [ -7.120e-06 -1.029e-19j,  -1.951e-09 -3.568e-06j, ...,
# -4.912e-07 -1.487e-07j,   4.438e-06 -1.448e-05j],
# [  7.136e-06 -0.000e+00j,   3.561e-06 -0.000e+00j, ...,
# -5.144e-07 -0.000e+00j,  -1.514e-05 -0.000e+00j]], dtype=complex64)

# Use left-aligned frames, instead of centered frames

D_left = librosa.stft(y, center=False)

# Use a shorter hop length

D_short = librosa.stft(y, hop_length=64)

# Display a spectrogram

import matplotlib.pyplot as plt
librosa.display.specshow(librosa.amplitude_to_db(librosa.magphase(D)[0],
                                                 ref=np.max),
                         y_axis='log', x_axis='time')
plt.title('Power spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

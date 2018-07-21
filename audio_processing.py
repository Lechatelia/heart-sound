# Beat tracking example
from __future__ import print_function
import os
import glob
import ntpath
import numpy as np
import librosa
import matplotlib.pyplot as plt
import librosa.display
import os
import xlwt
import csv

txt_name_for_chongfu='./chongfu1.txt'



def extract_feature(file_name,outfile=None):
    min_data =44000
    X, sample_rate = librosa.load(file_name)
    # X, sample_rate1 = librosa.load(file_name, offset=8.1)
    if len(X) >= min_data:
        offset = np.random.randint(0, high=len(X) - min_data)
        X = X[offset:offset + min_data]
        if(outfile!=None):
            # print("!!!{file_name}".format(file_name=file_name))
            outfile.write(file_name+'\n')
    # else:
    #     pad = (int((min_data - len(X)) / 2), min_data - len(X) - int((min_data - len(X)) / 2))
    #     X = np.pad(X, pad_width=pad, mode='constant', constant_values=0)
    stft = np.abs(librosa.stft(X))
    mfccs = librosa.util.normalize(np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0))
    chroma = librosa.util.normalize(np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0))
    mel = librosa.util.normalize(np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0))
    contrast = librosa.util.normalize(np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0))
    tonnetz = librosa.util.normalize(np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0))

    # Compute local onset autocorrelation

    # # hop_length = 512
    oenv = librosa.onset.onset_strength(y=X, sr=sample_rate)
    tempogram = librosa.util.normalize(np.mean(librosa.feature.tempogram(onset_envelope=oenv, sr=sample_rate).T, axis=0))
    # # Compute global onset autocorrelation
    # ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
    # ac_global = librosa.util.normalize(ac_global)
    #
    # rmse = np.mean(librosa.feature.rmse(y=X).T, axis=0)
    # cent = np.mean(librosa.feature.spectral_centroid(y=X, sr=sample_rate).T, axis=0)
    # spec_bw = np.mean(librosa.feature.spectral_bandwidth(y=X, sr=sample_rate).T, axis=0)

    # print("tempogram:%d, ac_global:%d, rmse:%d, stft:%d, mel:%d" % (len(tempogram), len(ac_global), len(rmse), len(stft), len(mel)))
    # print(rmse)
    # print(cent)
    # print(spec_bw)
    #
    # onset_env = librosa.onset.onset_strength(y=X, sr=sample_rate,
    #                                          hop_length=512,
    #                                          aggregate=np.median)
    # peaks = librosa.util.peak_pick(onset_env, 3, 3, 3, 5, 0.5, 10)
    # print(stft)
    # print(tonnetz)
    # print(peaks)
    return mfccs, chroma, mel, contrast, tonnetz, tempogram

def extract_feature_2D(file_name):
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    # mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    # chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    # mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
    # contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    # tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
    # oenv = librosa.onset.onset_strength(y=X, sr=sample_rate)
    # tempogram = np.mean(librosa.feature.tempogram(onset_envelope=oenv, sr=sample_rate).T, axis=0)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T

    chroma = librosa.feature.chroma_stft(S=stft, sr=sample_rate).T
    mel = librosa.feature.melspectrogram(X, sr=sample_rate).T
    contrast = librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T
    oenv = librosa.onset.onset_strength(y=X, sr=sample_rate)
    tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sample_rate).T
    print(str(mfccs.shape))
    print(str(chroma.shape))
    print(str(mel.shape))
    print(str(contrast.shape))
    print(str(tonnetz.shape))
    print(str(tempogram.shape))
    return mfccs, chroma, mel, contrast, tonnetz, tempogram

def parse_audio_files(parent_dir, sub_dirs, file_ext='*.wav'):
    labels_map = ['artifact', 'extrahls', 'normal', 'murmur', 'extrastole', 'Aunlabelledtest', 'Bunlabelledtest']
    # print(enumerate(sub_dirs))

    # filenames, folders = []
    saveft = []
    header = []
    features, labels = np.empty((0, 580)), np.empty(0)
    for sub_dir in sub_dirs:  # enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            file_name = ntpath.basename(fn)
            file_attrs = file_name.split("_")
            xi_class = file_attrs[0].strip()

            # if xi_class != "Bunlabelledtest":
            print('Processing file: %s'.ljust(30) % file_name, end='\r')
            mfccs, chroma, mel, contrast, tonnetz, tempogram = extract_feature(fn)
            print(mfccs.shape)
            print(mel.shape)
            print(chroma.shape)
            print(tonnetz.shape)
            print(contrast.shape)
            print(tempogram.shape)
            # print(ac_global.shape)

            ext_features = np.hstack([file_name, sub_dir, xi_class, mfccs, chroma, mel, contrast, tonnetz, tempogram])

            header = ['filename', 'folder', 'label']
            header.extend(['mfcc'] * len(mfccs))
            header.extend(['chroma'] * len(chroma))
            header.extend(['mel'] * len(mel))
            header.extend(['contrast'] * len(contrast))
            header.extend(['tonnetz'] * len(tonnetz))
            header.extend(['tempogram'] * len(tempogram))
            # header.extend(['ac_global']*len(ac_global))

            tmp = [file_name, sub_dir, xi_class]
            tmp.extend(mfccs)
            tmp.extend(chroma)
            tmp.extend(mel)
            tmp.extend(contrast)
            tmp.extend(tonnetz)
            tmp.extend(tempogram)
            # tmp.extend(ac_global)
            # print(len(ext_features))
            features = np.vstack([features, ext_features])
            # print(labels_map[file_attrs[0].strip()])
            labels = np.append(labels, labels_map.index(xi_class))
            # filenames.append(file_name)
            # folders.append(sub_dir)
            saveft.append(tmp)
        # exit(-1)

    # print(mfccs.tolist())

    # with open('some.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(mfccs.tolist())
    #     writer.writerow(chroma.tolist())
    #     writer.writerow(mel.tolist())
    saveft.insert(0, header)
    return np.array(features), np.array(labels, dtype=np.int), saveft


def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels, n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode

def pre_precessing():
    # 1. Get the file path to the included audio example
    # filename = librosa.util.example_audio_file()
    # labels_map = ['artifact', 'normal', 'murmur', 'extrahls'] #setb labels
    # labels_map = ['normal', 'murmur', 'extrastole'] #setb labels
    labels_map = ['artifact', 'extrahls', 'normal', 'murmur', 'extrastole', 'Aunlabelledtest', 'Bunlabelledtest']  # all
    # labels_map = ['artifact', 'normal', 'murmur', 'extrastole']#{'artifact':0, 'murmur':1}
    filename = "fea4.wav"  # ""data/set_a/murmur__201108222221.wav"

    data = {}
    # 2. Load the audio as a waveform `y`
    #    Store the sampling rate as `sr`
    y, sr = librosa.load(filename)
    # # 3. Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # #data['chroma_stft'] = librosa.feature.chroma_stft(y=y, sr=sr)
    data['beat_track'] = librosa.frames_to_time(beat_frames, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print("beat_times" + str(beat_times))


    parent_dir = 'data'
    sub_dirs = ['set_a', 'set_b']
    features, labels, saveft = parse_audio_files(parent_dir, sub_dirs)
    print(labels)
    print(features)
    print(saveft)
    labels = one_hot_encode(labels)
    print(labels)

    print('Processing file: %s', filename, end='\r')
    mfccs, chroma, mel, contrast, tonnetz, tempogram = extract_feature(filename)
    print(mfccs.shape)
    print(mel.shape)
    print(chroma.shape)
    print(tonnetz.shape)
    print(contrast.shape)
    print(tempogram.shape)

    # np.savetxt("features.csv", features, delimiter=",")
    # np.savetxt("labels.csv", labels, delimiter=",")

    print(len(saveft))
    import csv

    with open('fea3.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(saveft)



def write_features_into_excel(dir,write_txt=True):
    write_data=[]
    out_file = open(txt_name_for_chongfu, 'a+')
    # out_file.close()
    with open('write.csv', 'w', newline='') as csv_file:

    # with open('write.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for file in os.listdir(dir):
            # if os.path.isfile(file):
            if file.split('.')[-1] == 'wav':


                features= extract_feature(dir + file,out_file)
                features = np.concatenate(features, 0)
                # print(file.split('_')[0])
                write_data[0:3]=[file, '', file.split('_')[0]]
                write_data[3:]=features
                csv_writer.writerow(write_data)  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容

def write_features_intxt_into_excel(dir):
    write_data=[]
    i=0
    with open('write.csv', 'a+', newline='') as csv_file:

    # with open('write.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        with open(dir, 'r') as file_to_read:  #路径加txt的文件名
            while True:
                lines = file_to_read.readline().strip('\n')  # 整行读取数据
                if not lines:
                    break
                features = extract_feature(lines)
                features = np.concatenate(features, 0)
                # print(lines.split('/')[1].split('_')[0])
                write_data[0:3] = [lines.split('/')[1], '', lines.split('/')[1].split('_')[0]]
                write_data[3:] = features
                csv_writer.writerow(write_data)
                i+=1
        print("txt2csv number:\t{num}".format(num=i))




if __name__ == '__main__':
    # extract_feature('dataset/artifact__201012172012.wav')
    # write_features_into_excel('dataset/')
    write_features_intxt_into_excel(txt_name_for_chongfu)



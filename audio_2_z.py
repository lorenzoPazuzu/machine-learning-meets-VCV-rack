import os
import csv
import umap
import json
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

np.random.seed(8)

def wavenet_encode(file_path):
    checkpoint_path = './wavenet-ckpt/model.ckpt-200000'

    #load and downsample the audio
    neural_sample_rate = 16000
    audio = utils.load_audio(file_path,
                             sample_length=400000,
                             sr=neural_sample_rate)

    # pass the audio through the first half of the autoencoder,
    # to get a list of latent variables that describe the sound.
    # Note that it would be quicker to pass a batch of audio
    # to fastgen.

    encoding = fastgen.encode(audio, checkpoint_path, len(audio))

    # reshape to a  single sound.
    return encoding.reshape((-1,16))

directory = './VCVpatches'
dataset = []
errors = 0

sample_rate = 44100
mfcc_size = 13

for file in os.listdir(directory):
    if(file.endswith('.wav')):
        file_path = os.path.join(directory,file)

        try:
            wavenet_data = wavenet_encode(file_path)
            stddev_wavenet = np.std(wavenet_data, axis=0)
            mean_wavenet = np.mean(wavenet_data, axis=0)
            average_difference_wavenet = np.zeros((16,))
            for i in range(0, len(wavenet_data) - 2, 2):
                average_difference_wavenet += wavenet_data[i] - wavenet_data[i+1]
            average_difference_wavenet /= (len(wavenet_data) // 2)
            average_difference_wavenet = np.array(average_difference_wavenet)

            concat_features_wavenet = np.hstack((stddev_wavenet, mean_wavenet))
            concat_features_wavenet = np.hstack((concat_features_wavenet, average_difference_wavenet))

            data, _ = librosa.load(file_path)

            trimmed_data, _ = librosa.effects.trim(y=data)
            mfccs = librosa.feature.mfcc(trimmed_data,
                                         sample_rate,
                                         n_mfcc=mfcc_size)
            stddev_mfccs = np.std(mfccs, axis=1)

            mean_mfccs = np.mean(mfccs, axis=1)

            average_difference = np.zeros((mfcc_size,))
            for i in range(0, len(mfccs.T) - 2, 2):
                average_difference += mfccs.T[i] - mfccs.T[i+1]
            average_difference /= (len(mfccs) // 2)
            average_difference = np.array(average_difference)

            concat_features = np.hstack((stddev_mfccs, mean_mfccs))
            concat_features = np.hstack((concat_features, average_difference))

            dataset += [(file, concat_features_wavenet, concat_features)]

        except:
            print("error!")
            errors += 1

print('errors:', errors)


#### preparing the data to be plotted and saved in a json file for visualization

all_file_paths, wavenet_features, mfcc_features = zip(*dataset)

wavenet_features = np.nan_to_num(np.array(wavenet_features))
mfcc_features = np.array(mfcc_features)

mfcc_tuples = []
wavenet_tuples = []

all_json = dict()
all_json["filenames"] = all_file_paths

print(all_file_paths.index('bird.wav'))

#return index of the external file
ext_index = all_file_paths.index('bird.wav')


print(len(all_file_paths),
      wavenet_features.shape,
      mfcc_features.shape)

def get_scaled_tsne_embeddings(features,perplexity, iteration):
    embedding = TSNE(n_components=2,
                     perplexity=perplexity,
                     n_iter=iteration).fit_transform(features)
    scaler = MinMaxScaler()
    scaler.fit(embedding)
    return scaler.transform(embedding)

def transform_numpy_to_json(array):
    data = []
    for index, position in enumerate(array):
        data.append({
            'coordinates{0}'.format(str(index)) : position.tolist()
        })
    return data

tnse_embeddings_mfccs = []
tnse_embeddings_wavenet = []

perplexities = [5,30,50,100]
iterations = [500, 1000, 2000, 5000]
for i, perplexity in enumerate(perplexities):
    for j, iteration in enumerate(iterations):
        tsne_mfccs = get_scaled_tsne_embeddings(mfcc_features,
                                                perplexity,
                                                iteration)
        tnse_wavenet = get_scaled_tsne_embeddings(wavenet_features,
                                                  perplexity,
                                                  iteration)
        tnse_embeddings_mfccs.append(tsne_mfccs)
        tnse_embeddings_wavenet.append(tnse_wavenet)

        mfcc_key = 'tsnemfcc{}{}'.format(i,j)
        wavenet_key = 'tsnewavenet{}{}'.format(i,j)

        all_json[mfcc_key] = transform_numpy_to_json(tsne_mfccs)
        all_json[wavenet_key] = transform_numpy_to_json(tnse_wavenet)


'''# plotting

fix, ax = plt.subplots(nrows=len(perplexities),
                       ncols=len(iterations),
                       figsize=(30, 30))

for i, row in enumerate(ax):
    for j, col in enumerate(row):
        current_plot = i * len(iterations) + j
        col.scatter(tnse_embeddings_mfccs[current_plot].T[0],
                    tnse_embeddings_mfccs[current_plot].T[1],
                    s=100) # size of the plotted dots
plt.show()

def get_pca(features):
    pca = PCA(n_components=2)
    transformed = pca.fit(features).transform(features)
    scaler = MinMaxScaler()
    scaler.fit(transformed)
    return scaler.transform(transformed)

pca_mfcc = get_pca(mfcc_features)
pca_wavenet = get_pca(wavenet_features)

mfcc_key = 'pcamfcc'
wavenet_key = 'pcawavenet'

all_json[mfcc_key] = transform_numpy_to_json(pca_mfcc)
all_json[wavenet_key] = transform_numpy_to_json(pca_wavenet)

plt.figure(figsize=(30,30))
_ = plt.scatter(pca_mfcc.T[0],
                pca_mfcc.T[1],
                s = 100) # size of the plotted dots
plt.show()

json_name = "data.json"
json_string = "d = '" + json.dumps(all_json) + "'"
with open(json_name, 'w') as json_file:
    json_file.write(json_string)'''
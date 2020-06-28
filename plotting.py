from audio_2_z import *

# color list
color = []

for c in range(len(all_file_paths)):
    if c != ext_index:
        color.append('b')
    else:
        color.append('r')
color = np.array(color)

# plotting

fix, ax = plt.subplots(nrows=len(perplexities),
                       ncols=len(iterations),
                       figsize=(30, 30))


for i, row in enumerate(ax):
    for j, col in enumerate(row):
        current_plot = i * len(iterations) + j
        col.scatter(tnse_embeddings_mfccs[current_plot].T[0],
                    tnse_embeddings_mfccs[current_plot].T[1],
                    s=100,
                    c = color) # size of the plotted dots
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
                s = 300,
                c=color) # size of the plotted dots
plt.show()

json_name = "data.json"
json_string = json.dumps(all_json)
with open(json_name, 'w') as json_file:
    json_file.write(json_string)
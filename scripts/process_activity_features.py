import numpy as np
import pandas as pd
from scipy import spatial

def demo(labels, dist_matrix):
    for i in range(len(dist_matrix)):
        indices = list(np.argsort(dist_matrix[i]))
        out_labels = list()
        for j in indices:
            if dist_matrix[i][j] <= 0.01:
                indices.remove(j)
        for k in indices:
            if labels[i] is not labels[k] and labels[k] not in out_labels: 
                out_labels.append(labels[k])
        print(f'{labels[i]} ++++ {", ".join([x for x in out_labels[:3]])}')

def calculate_distance_matrix(features):
    dist_matrix = []
    for i in range(len(features)):
        dist_vec = []
        for j in range(len(features)):
            dist_vec.append(spatial.distance.cosine(features[i], features[j]))
        dist_matrix.append(dist_vec)
    return dist_matrix

def main():
    data = pd.read_csv("./output.csv", header=None)
    labels = data.ix[:,0]
    features = np.matrix(data.ix[:,1:])
    dist_mat = calculate_distance_matrix(features)
    demo(labels, dist_mat)

if __name__ == "__main__":
    main()
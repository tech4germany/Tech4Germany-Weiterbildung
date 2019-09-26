import csv
import numpy as np
from scipy import spatial

def embeddings_to_distance_matrix(embeddings):
    dist_matrix = []
    for i in range(len(embeddings)):
        distances = []
        for j in range(len(embeddings)):
            distances.append(spatial.distance.cosine(np.array(embeddings[i]), np.array(embeddings[j])))
        dist_matrix.append(distances)
    return dist_matrix

def export_dist_matrix(dist_matrix, out_path):
    with open(out_path, 'w+') as out_file:
        for i in range(len(dist_matrix)):
            out_file.write(f'{",".join([str(x) for x in dist_matrix[i]])}\n')

def load_embeddings(path):
    embeddings = []
    with open(path, 'r') as infile:
        data = csv.reader(infile, delimiter=',', quotechar='|')
        for line in data:
            embedding = [float(x) for x in line[1:]]
            embeddings.append(embedding)
    return embeddings

def main():
    embeddings_path = './embeddings.csv'
    embeddings = load_embeddings(embeddings_path)
    dist_matrix = embeddings_to_distance_matrix(embeddings)
    export_dist_matrix(dist_matrix, "./embeddings_dists_cosine.csv")

if __name__ == "__main__":
    main()
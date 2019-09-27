import csv
import numpy as np

def load_entities():
    entities = []
    with open('../data/embeddings.csv', 'r') as embeddings_in:
        data = csv.reader(embeddings_in, delimiter=',')
        for line in data:
            entities.append(line[0])
    return entities

def load_cosine_distances():
    cosine_distances = []
    with open('../data/embeddings_dists_cosine.csv', 'r') as dists_in:
        data = csv.reader(dists_in, delimiter=',')
        for line in data:
            cosine_distances.append([float(x) for x in line])
    return cosine_distances

def get_unique_distances(distances):
    unique_distances = []
    for i in range(len(distances)):
        for j in range(i+1,len(distances)):
            unique_distances.append(distances[i][j])
    return unique_distances

def get_average_cosine_distance(unique_distances):
    return sum(unique_distances) / len(unique_distances)

def find_seed_points(cosine_distance_matrix, average_distance, num_pts = 2):
    seed_pts = np.random.choice(np.arange(len(cosine_distance_matrix[0])), num_pts)
    for index in range(len(seed_pts)-1):
        if cosine_distance_matrix[seed_pts[index]][seed_pts[index+1]] < average_distance:
            return find_seed_points(cosine_distance_matrix, average_distance, num_pts)
    return seed_pts

def main():
    entities = load_entities()
    cosine_distances = load_cosine_distances()
    unique_distances = get_unique_distances(cosine_distances)
    average_distance = get_average_cosine_distance(unique_distances)
    seed_pts = find_seed_points(cosine_distances, average_distance)
    seed_vals = [entities[x] for x in seed_pts]
    print(f'Seed with values {seed_vals}')

if __name__ == "__main__":
    main()
import csv
from scipy.spatial import distance

def export_cosine_distances(input_file, output_file):
    embeddings = []
    with open(input_file, 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        for line in data:
            embedding = [float(x) for x in line[1:]]
            embeddings.append(embedding)
    
    with open(output_file, 'a+') as outfile:
        for i in range(len(embeddings)):
            dists = [distance.cosine(embeddings[i], embeddings[j]) for j in range(len(embeddings))]
            outfile.write(f'{",".join([str(round(x, 4)) for x in dists])}\n')
                

if __name__ == "__main__":
    export_cosine_distances("./job_embeddings.csv", "../backend/data/jobs_cosine_distances.csv")
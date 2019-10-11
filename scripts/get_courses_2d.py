from sklearn.manifold import TSNE
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def tsne_features(jobs):
    print('========== Fitting T-SNE ==========')
    features = []
    for key in jobs:
        features.append(jobs[key])
    tsne_ak_2d = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
    jobs_ak_2d = tsne_ak_2d.fit_transform(features)
    plt.figure(figsize=(16, 9))
    x = jobs_ak_2d[:,0]
    y = jobs_ak_2d[:,1]
    plt.scatter(x, y, alpha=0.1)
    for i, key in enumerate(jobs):
        if i % 1 == 0:
            plt.annotate(key, xy=(x[i], y[i]), xytext=(5, 2), 
                        textcoords='offset points', ha='right', va='bottom', size=5)
    plt.legend(loc=4)
    plt.title('Kurstitel')
    plt.show()
    print('========== Done Fitting T-SNE ==========')

def main():
    jobs = dict()
    line_nr = 0
    with open("./output.csv", 'r') as infile:
        for line in infile:
            if line_nr == 25000: break
            data = line.strip().split(',')
            jobs[data[0]] = data[1:]
            line_nr += 1
    tsne_features(jobs)

if __name__ == "__main__":
    main()
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
    plt.scatter(x, y, alpha = 0.05)
    for i, key in enumerate(jobs):
        interest_points = ['abfallbeauftragte/r''afrikanist/in', 'altenpfleger/in', 'anlageberater/in', 'apotheker/in', 'architekt/in', 'arzt/ärztin', 'betriebswirt/in (bbig)', 'bildeinrahmer/in', 'bodensteward/-stewardess', 'dachdecker/in', 'detektiv/in', 'fahrzeugpfleger/in', 'fitnesstrainer/in', 'fluglehrer/in' 'forstmaschinenführer/in', 'fußballtrainer/in', 'gamedesigner/in', 'geofraf/in', 'gestalter/in - produktdesign', 'gewandmeister/in', 'imam', 'inkassobeauftragte/r (außendienst)', 'jurist/in', 'klauenpfleger/in' 'modist/in', 'politiker/in', 'regisseur/in', 'rettungshelfer/in', 'schweißer/in', 'schiffssteward/-stewardess', 'softwareentwickler/in', 'sportgerätebauer/in', 'verkaufstrainer/in', 'wahrsager/in', 'wett- und lotterieannehmer/in']
        if key.lower() in interest_points:
            plt.annotate(key, xy=(x[i], y[i]), xytext=(5, 2), 
                        textcoords='offset points', ha='right', va='bottom', size=15)
        # plt.annotate(key, xy=(x[i], y[i]), xytext=(5, 2), color='blue',
        #             textcoords='offset points', ha='right', va='bottom', size=8)
    plt.legend(loc=4)
    plt.xlabel = "T-distributed Stochastic Neighbor Embedding Dimension 1"
    plt.ylabel = "T-distributed Stochastic Neighbor Embedding Dimension 2"
    plt.title('Repräsentationen von Berufstiteln anhand von Embeddings der Tätigkeitsbeschreibungen')
    plt.show()
    print('========== Done Fitting T-SNE ==========')
    
def main():
    jobs = dict()
    line_nr = 0
    with open("./job_features.csv", 'r') as infile:
        for line in infile:
            data = line.strip().split(',')
            jobs[data[0]] = data[1:]
            line_nr += 1
    tsne_features(jobs)

if __name__ == "__main__":
    main()
import json

a = []
for l in open('tuits.json','r'):
    a.append(json.loads(l))

tuits = map(lambda i: a[i]['text'], xrange(len(a)))


################################################################################################################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import izip
import matplotlib.pyplot as plt
import numpy as np
import operator
import json
import pickle

from scipy.spatial.distance import cosine
from itertools import combinations

# my_stop_words = text.ENGLISH_STOP_WORDS
my_stop_words = text.ENGLISH_STOP_WORDS.union(['https','trump','realdonaldtrump','trump2016','co','t'])
with open('/Users/davidr/Downloads/2016523tweets.json','r') as f:
    df1 = json.load(f)

with open('/Users/davidr/Downloads/tuits2/tuits.txt','r') as f:
    df2 = pickle.load(f)


#vectorizer = TfidfVectorizer(token_pattern=u'^[^@#][\w]+',min_df=0.1,ngram_range=(3,4),max_features=100,stop_words=set(my_stop_words),max_df=0.2)
vectorizer = TfidfVectorizer(token_pattern=u'[\w]+',ngram_range=(2,4),analyzer='word',max_features=100,stop_words=my_stop_words)
tfidf_matrix = vectorizer.fit_transform(df1['tweet'].values()[:1000] + df2)
feature_names = vectorizer.get_feature_names()
npm = np.array(tfidf_matrix.toarray())


Uf, sf, Vf = np.linalg.svd(npm, full_matrices=False)
c = 2
rd_words = np.dot(np.diag(sf[:c]) , Vf[:c,])

plt.scatter(rd_words[0],rd_words[1])
for i, l in enumerate(feature_names):
    plt.annotate(l, (rd_words[0][i],rd_words[1][i]))

plt.show()

data = rd_words.T
k = 20
kmedias = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=-1)
kmedias.fit(rd_words.T,feature_names)

labels = kmedias.labels_
centroids = kmedias.cluster_centers_

for i in range(k):
    # select only data observations with cluster label == i
    ds = data[np.where(labels==i)]
    # plot the data observations
    plt.plot(ds[:,0],ds[:,1],'o')
    # plot the centroids
    lines = plt.plot(centroids[i,0],centroids[i,1],'kx')
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)

for i in np.random.randint(0,len(feature_names),size=10):
    plt.annotate(feature_names[i], (rd_words[0][i],rd_words[1][i]))

plt.show()

for i in xrange(k):
    topics = []
    for t in (np.where(labels == i)[0]):
        topics.append(feature_names[t])
    print 'Cluster {} : {}'.format(i,topics)


###############################################################################################################
###############################################################################################################
###############################################################################################################

from sklearn.cluster import KMeans
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import izip
import matplotlib.pyplot as plt
import numpy as np
import operator
import json
import pickle

from scipy.spatial.distance import cosine
from itertools import combinations

with open('/Users/davidr/Downloads/2016523tweets.json','r') as f:
    df1 = json.load(f)
with open('/Users/davidr/Downloads/tuits2/tuits.txt','r') as f:
    df2 = pickle.load(f)

my_stop_words = text.ENGLISH_STOP_WORDS.union(['https','#trump','@realdonaldtrump','co','t'])
vectorizer = TfidfVectorizer(token_pattern=u'[#@\w]+',ngram_range=(2,4),analyzer='word',max_features=100,stop_words=my_stop_words)
tfidf_matrix = vectorizer.fit_transform(df1['tweet'].values()[:1000] + df2)
feature_names = vectorizer.get_feature_names()
npm = np.array(tfidf_matrix.toarray())


Uf, sf, Vf = np.linalg.svd(npm, full_matrices=False)
c = 2

rd_words = np.dot(np.diag(sf[:c]) , Vf[:c,])

data = rd_words.T
k = 20
kmedias = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=-1)
kmedias.fit(rd_words.T,feature_names)

labels = kmedias.labels_
centroids = kmedias.cluster_centers_


for i in xrange(k):
    topics = []
    for t in (np.where(labels == i)[0]):
        topics.append(feature_names[t])
    print 'Cluster {} : {}'.format(i,topics)

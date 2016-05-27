from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import izip
import numpy as np
import operator
import json

from scipy.spatial.distance import cosine
from itertools import combinations

my_stop_words = text.ENGLISH_STOP_WORDS
with open('../Downloads/2016523tweets.json') as f:
    data = json.load(f)

# data contiene un diccionario con una sola llava 'tweet' que contiene otro diccionario.


# vectorizer = TfidfVectorizer(min_df=1)
# Definimos la forma en que parte los strings para procesarlos en tfidf
my_stop_words = text.ENGLISH_STOP_WORDS
vectorizer = TfidfVectorizer(token_pattern=u'[\S]+',min_df=1,stop_words=set(my_stop_words))  #quitamos stopwords porque si aparecen como palabras relevantes
# Aplica tfidf a los datos cargados del archivo (texto de los tweets)
tfidf_matrix = vectorizer.fit_transform(data['tweet'].values())
# Extraemos los feature_names (en nuestro caso, los features son las palabras del vocabulario de los tweets)
feature_names = vectorizer.get_feature_names()
# tfidf_matrix contiene la matriz de resultado tfidf, pero es numerica, por lo que es conveniente convertirla a numpy.array para procesar mas rapido.
npm = np.array(tfidf_matrix.toarray())
## Eliminamos @realdonaldtrump y #trump #Trump
def drop_word(w, fn, m):
    aux2= range(len(fn))
    index = fn.index(w)
    del fn[index]
    del aux2[index]
    aux = m.T[aux2]
    return fn,aux.T

feature_names, npm =drop_word('@realdonaldtrump',feature_names,npm)
feature_names, npm =drop_word('#trump',feature_names,npm)
feature_names, npm =drop_word('#Trump',feature_names,npm)


# Hacemos la compisicion por suma (suma de los documentos por palabra), cuyo resultado es un vector con el peso de cada palabra (ordenado de acuerdo con el arreglo de feature_names)
wp = map(lambda i: sum(npm[:,i]), range(len(npm)))
tfidf_dict = dict(izip(iter(feature_names),iter(wp)))
sorted_tfidf = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)
## Definimos con cuantas palabras, con cuantos hashtags y con cuantas personas nos quedaremos (de las más importantes extridas de la composicion) para hacer el análisis propuesto
nw = 200
nh = 10
pn = 20

## Limpiamos la matriz tfidf para quedarnos sólo con los vectores correspondientes a las palabras, hastags y personas que nos interesan.
interesting_words  = []
cnw = 0
cnh = 0
cpn = 0
for i in sorted_tfidf:
    if (i[0].startswith('@')):
        if (cpn < pn):
            interesting_words.append(i[0])
            cpn += 1
    elif (i[0].startswith('#')):
        if (cnh < nh):
            interesting_words.append(i[0])
            cnh += 1
    elif (cnw < nw):
        cnw += 1
        interesting_words.append(i[0])
    if cnw == nw and cnh == nh and cpn == pn:
        break


indices = []
for w in interesting_words:
    indices.append(feature_names.index(w))


miw = npm.T[indices].T
## Ahora interesting_words contiene nuestra lista de feature_names y miw(matrix of interesting words) contiene la matriz tfidf de solo las palabras que nos interesan

U, s, V = np.linalg.svd(miw)
print miw.shape, len(interesting_words)

# Numero de caracteristicas (coordenadas) que queremos

c = 100

rd_words = np.dot(np.diag(s[:100]) , V[:100,])


def m_distance(m):
    m = m.T
    distancias = np.zeros((len(m), len(m)))
    for x, y in combinations(range(len(distancias)), 2):
        d = cosine(m[x],m[y])
        distancias[x][y] = d
        distancias[y][x] = d
    return distancias


distancias = m_distance(rd_words)

spectral = SpectralClustering(n_clusters=2,eigen_solver='arpack',affinity="nearest_neighbors")

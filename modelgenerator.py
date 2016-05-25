from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import izip
import numpy as np
import operator
import json

my_stop_words = text.ENGLISH_STOP_WORDS.union(my_words)
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
# tfidf_matrix contiene la matriz de resultado tfidf, pero es numérica, por lo que es conveniente convertirla a numpy.array para procesar más rápido.
npm = np.array(tfidf_matrix.toarray())
# Hacemos la compisición por suma (suma de los documentos por palabra), cuyo resultado es un vector con el peso de cada palabra (ordenado de acuerdo con el arreglo de feature_names)
wp = map(lambda i: sum(npm[:,i]), range(len(npm)))
tfidf_dict = dict(izip(iter(feature_names),iter(wp)))
sorted_tfidf = sorted(tfidf_dict.items(), key=operator.itemgetter(1))

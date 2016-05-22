from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import izip
import numpy as np
import operator

arch = open('Downloads/tweets.csv','rb')
d = list()
header = arch.readline()
for l in arch:
    if l != header:
        d.append(l)

# vectorizer = TfidfVectorizer(min_df=1)
vectorizer = TfidfVectorizer(token_pattern=u'[\S]+',min_df=1)
tfidf_matrix = vectorizer.fit_transform(d)
feature_names = vectorizer.get_feature_names()
npm = np.array(tfidf_matrix.toarray())
wp = map(lambda i: sum(npm[:,i]), range(len(npm)))
tfidf_dict = dict(izip(iter(feature_names),iter(wp)))
sorted_tfidf = sorted(tfidf_dict.items(), key=operator.itemgetter(1))

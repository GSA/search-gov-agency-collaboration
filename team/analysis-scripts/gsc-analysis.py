import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# Read the performance data into Pandas data frame.

client = ""

df = pd.read_csv("input-files/" + client + "-Queries.csv")

documents = df["Top queries"].to_list()
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,3))
X = vectorizer.fit_transform(documents)

true_k = 20
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=42, random_state=42)
model.fit(X)
topic_map = {}
topic_terms = {} 

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
for i in range(true_k):

    cluster_terms = []
    for ind in order_centroids[i, :10]:
        cluster_terms.append(' %s' % terms[ind])
    print("Cluster {}, Terms : {}".format(i, cluster_terms)),
    topic_map[i] = str(i) + "-" + cluster_terms[0].strip()
    topic_terms[i] = str(cluster_terms)

# assign cluster to each query
df['cluster'] = model.predict(vectorizer.transform(df["Top queries"]))

# add label to the clusters
df['cluster_label'] = df.cluster.map(topic_map)
df['cluster_top_terms'] = df.cluster.map(topic_terms)

# Next create the ctr from Click and impression data
df['CTR'] = df.Clicks/df.Impressions

df.to_csv("output-files/" + client + "-all.csv", index=False, header=True)

# Find the topic cluster on your site which are converting the best and also the topic which get impression but doesn't convert well.
df.groupby(['cluster_label', 'cluster_top_terms']).agg({'CTR': 'mean', 'Impressions': 'sum'}).reset_index().sort_values('CTR', ascending=False).to_csv('output-files/' + client + '-cluster.csv',index=False, header=True)




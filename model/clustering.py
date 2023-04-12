from sklearn.metrics import r2_score
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
def k_means():
    df_train = pd.read_csv('../data/encoded_data_train.csv')
    df_test = pd.read_csv('../data/encoded_data_test.csv')




    kmeans = KMeans(2).fit_predict(df_train)
    df_train['cluster'] = pd.Series(kmeans, index=df_train.index)

    #plt.show()
    #q = df_train["connectedDuration"].quantile(0.90)
    #df2 = df_train[df_train["connectedDuration"] > q]
    df_train[['cluster']].hist(figsize=(20, 15))
    plt.show()


k_means()
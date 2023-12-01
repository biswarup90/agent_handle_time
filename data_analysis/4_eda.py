import matplotlib.pyplot as plt
import seaborn as sns
import ydata_profiling.profile_report as pp
from util.utils import get_encoded_data, get_engineered_data_train, get_unique_values_of_col
import seaborn as sns
import dtale
import sweetviz as sv
import seaborn as sns
from scipy.special import boxcox
from constants.constants import *


def eda():
    df = get_encoded_data(False)[0]
    #df = df[df['createdTime_hour'] == 5]
    #print(df.info())
    #print(get_unique_values_of_col(df, 'createdTime_week'))
    df.plot.scatter(x='queue_encoded', y='connectedDuration', s=1)
    plt.title('Relationship between Agent and Handle time')
    plt.xlabel('Queue')
    plt.ylabel('Connected Duration')
    plt.show()


def histograms():
    df = get_encoded_data(False)[0]
    df['connectedDuration'].hist(figsize=(20, 15), bins=100)
    plt.title('Distribution of Connected Duration')
    plt.xlabel('Connected Duration')
    plt.ylabel('Frequency')
    plt.show()


def basic():
    df = get_encoded_data(False)[0]
    print(df['connectedDuration'].describe())
    print(df['connectedDuration'].std())
    #x = df.reset_index().plot.scatter(x='index', y='connectedDuration')
    #print(type(x))
    #plt.show()


def find_outlier(col):
    df = get_encoded_data()[0]
    print(df[col].value_counts(bins=50))

    df[col].hist(figsize=(20, 15))
    plt.show()


def correlation():
    df = get_encoded_data(True)[0]
    #corr = df.corr()
    #print(corr[Y].abs().sort_values(ascending=False))
    corr = df.corr()
    sns.heatmap(corr, cmap="Blues", annot=True)
    plt.show()


def histograms_for_y():
    df = get_encoded_data()[0]
    df['normalised'] = (df[Y] - df[Y].mean()) / df[Y].std()
    plt.hist(boxcox(df[Y], BOX_COX_LAMBDA), bins=50)
    plt.show()


def pandasprofiling():
    df = get_encoded_data(False)[0]
    profile = pp.ProfileReport(df)
    profile.to_file("../plots/{0}/output.html".format(DATA_SOURCE))
    sweet_report = sv.analyze(df)
    sweet_report.show_html('../plots/{0}/sweet_report_output.html'.format(DATA_SOURCE))


def sns_plots():
    df = get_encoded_data()[0]
    sns.pairplot(data=df,
                 hue="connectedDuration")
    plt.show()


def getDataGroupedByAgent():
    df = get_encoded_data(False)[0]
    print(df.agent_encoded.value_counts())
    print(df.shape)


eda()

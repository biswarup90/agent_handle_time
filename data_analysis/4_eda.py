import matplotlib.pyplot as plt
import seaborn as sns
import ydata_profiling.profile_report as pp
from util.utils import get_encoded_data, get_engineered_data_train
import seaborn as sns
import dtale
import sweetviz as sv
import seaborn as sns
from scipy.special import boxcox
from constants.constants import *


def eda():
    ''''''
    # 1. discard selfserviceDuration, ringingDuration, queueDuration

    # df_test.drop(['selfserviceDuration', 'ringingDuration', 'queueDuration']) - adds no value
    # drop channel type - channel sub type captures all the info provided by channel type
    # origin, destination, queue, agent, contactReason, channelType are highly correlated columns


def histograms():
    df = get_encoded_data()[0]
    df['destination_encoded'].hist(figsize=(20, 15))
    plt.show()


def basic():
    df = get_encoded_data(False)[0]
    print(df.describe())


def find_outlier(col):
    df = get_encoded_data()[0]
    print(df[col].value_counts(bins=50))

    df[col].hist(figsize=(20, 15))
    plt.show()


def correlation():
    df = get_encoded_data(False)[0]
    corr = df.corr()
    print(corr[Y].abs().sort_values(ascending=False))
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
    profile.to_file("../plots/{0}/output.html".format(SOURCE))
    sweet_report = sv.analyze(df)
    sweet_report.show_html('../plots/{0}/sweet_report_output.html'.format(SOURCE))


def sns_plots():
    df = get_encoded_data()[0]
    sns.pairplot(data=df,
                 hue="connectedDuration")
    plt.show()


pandasprofiling()

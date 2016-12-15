from sklearn.ensemble import RandomForestRegressor
from numpy import genfromtxt, savetxt
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    # feature_data = genfromtxt(open('/Users/songjiang/Desktop/data_before_pca_7.csv','r'), delimiter=',', dtype='str')[0]
    # features = feature_data[0:-1]
    # dataset = genfromtxt(open('/Users/songjiang/Desktop/data_before_pca_7.csv','r'), delimiter=',', dtype='f8')[1:]

    dataset = genfromtxt(open('/Users/songjiang/Desktop/film_data/data_reducted_3.csv','r'), delimiter=',', dtype='f8')

    size = len(dataset)
    train_data_size = int(0.9*size)
    train_data = dataset[0: train_data_size]
    test_data = dataset[train_data_size:]

    target = [x[-1] for x in train_data]
    train = [x[0:-1] for x in train_data]

    true_test_label = [y[-1] for y in test_data]
    test = [y[0:-1] for y in test_data]

    rf = RandomForestRegressor(n_estimators=1000, max_features='sqrt')
    rf.fit(train, target)

    predicted_class = [round(x,1) for x in rf.predict(test)]
    # savetxt('/Users/songjiang/Desktop/predict_score.csv', predicted_class, delimiter=',', fmt='%f')

    # plot_feature_importance(rf, features)

    dif=[]
    for i in range(len(predicted_class)):
        dif.append(abs(true_test_label[i]-predicted_class[i]))

    mean = np.mean(dif)
    print mean


def plot_feature_importance(randomforest, features):
    importances = randomforest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in randomforest.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

    # Plot the feature importances of the random forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(len(features)), importances[indices], color="r", yerr=std[indices], align="center")
    plt.xticks(range(len(features)), features[indices],rotation=17)
    plt.xlim([-1, len(features)])
    plt.show()


if __name__=="__main__":
    main()

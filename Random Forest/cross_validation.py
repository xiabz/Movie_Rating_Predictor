from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from numpy import genfromtxt, savetxt
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def main():
    # feature_data = genfromtxt(open('/Users/songjiang/Desktop/data_before_pca.csv','r'), delimiter=',', dtype='str')[0]
    # features = feature_data[0:-1]
    # dataset = genfromtxt(open('/Users/songjiang/Desktop/data_before_pca.csv','r'), delimiter=',', dtype='f8')[1:]

    dataset = genfromtxt(open('/Users/songjiang/Desktop/film_data/data_reducted_3.csv','r'), delimiter=',', dtype='f8')

    train = np.array([x[0:-1] for x in dataset])
    target = np.array([int(x[-1]) for x in dataset])
    kf = KFold(n_splits=10, shuffle=True)

    ensemble_clf = [
       ("RandomForestClassifier, max_features='sqrt'",
        RandomForestClassifier(max_features="sqrt")),
       ("RandomForestClassifier, max_features='log2'",
        RandomForestClassifier(max_features='log2')),
       ("RandomForestClassifier, max_features=None",
        RandomForestClassifier(max_features= None ))
    ]
    precision_rate = OrderedDict((label, []) for label, _ in ensemble_clf)

    min_estimators = 5
    max_estimators = 300

    for label, clf in ensemble_clf:
        for i in range(min_estimators, max_estimators + 1):
            clf.set_params(n_estimators=i)
            temp_precision = []
            for train_index, test_index in kf.split(train):
                X_train, X_test = train[train_index], train[test_index]
                y_train, y_test = target[train_index], target[test_index]

                clf.fit(X_train, y_train)
                predicted_class = clf.predict(X_test)

                correct_predict_num = 0
                for j in range(len(y_test)):
                    if y_test[j] == predicted_class[j]:
                        correct_predict_num += 1
                temp_precision.append(1.0 * correct_predict_num / len(predicted_class))
            precision = round(sum(x for x in temp_precision) / 10, 3)
            precision_rate[label].append((i, precision))

    for label, clf_pre in precision_rate.items():
        xs, ys = zip(*clf_pre)
        plt.plot(xs, ys, label=label)

    plt.xlim(min_estimators, max_estimators)
    plt.xlabel("n_estimators")
    plt.ylabel("precision rate")
    plt.legend(loc="upper right")
    plt.show()

    # savetxt('/Users/songjiang/Desktop/predict_score.csv', predicted_class, delimiter=',', fmt='%f')




if __name__=="__main__":
    main()



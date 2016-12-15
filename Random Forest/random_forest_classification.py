from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from numpy import genfromtxt, savetxt
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()
def main():

    # feature_data = genfromtxt(open('/Users/songjiang/Desktop/film_data/data_before_pca_3.csv','r'), delimiter=',', dtype='str')[0]
    # features = feature_data[0:-1]
    # dataset = genfromtxt(open('/Users/songjiang/Desktop/film_data/data_before_pca_3.csv','r'), delimiter=',', dtype='f8')[1:]

    dataset = genfromtxt(open('/Users/songjiang/Desktop/film_data/data_before_pca_3.csv','r'), delimiter=',', dtype='f8')

    train = np.array([x[0:-1] for x in dataset])
    target = np.array([int(x[-1]) for x in dataset])
    kf = KFold(n_splits=10, shuffle=True)

    precision_rate = []
    for train_index, test_index in kf.split(train):
        X_train, X_test = train[train_index], train[test_index]
        y_train, y_test = target[train_index], target[test_index]

        rf = RandomForestClassifier(n_estimators=200, max_features='sqrt')
        rf.fit(X_train, y_train)

        predicted_class = rf.predict(X_test)

        correct_predict_num = 0
        for i in range(len(y_test)):
            if y_test[i] == predicted_class[i]:
                correct_predict_num += 1

        precision_rate.append(1.0 * correct_predict_num / len(predicted_class))

        plot_feature_importance(rf, features)
    precision = round(sum(x for x in precision_rate) / 10,3)
    print precision
    print precision_rate
    # target = transform_label(target)
    # true_test_label = transform_label(true_test_label)


    # savetxt('/Users/songjiang/Desktop/predict_score.csv', predicted_class, delimiter=',', fmt='%f')


# def transform_label(target):
#     for i in range(len(target)):
#         if target[i] >= 8:
#             target[i] = 3
#         elif target[i] < 8 and target[i] >= 5:
#             target[i] = 2
#         elif target[i] < 5:
#             target[i] = 1
#     return target


# def transform_label(target):
#     for i in range(len(target)):
#         if target[i] > 9.75:
#             target[i] = 100
#         elif target[i] < 9.75 and target[i] > 9.25:
#             target[i] = 95
#         elif target[i] < 9.25 and target[i] > 8.75:
#             target[i] = 90
#         elif target[i] < 8.75 and target[i] > 8.25:
#             target[i] = 85
#         elif target[i] < 8.25 and target[i] > 7.75:
#             target[i] = 80
#         elif target[i] < 7.75 and target[i] > 7.25:
#             target[i] = 75
#         elif target[i] < 7.25 and target[i] > 6.75:
#             target[i] = 70
#         elif target[i] < 6.75 and target[i] > 6.25:
#             target[i] = 65
#         elif target[i] < 6.25 and target[i] > 5.75:
#             target[i] = 60
#         elif target[i] < 5.75 and target[i] > 5.25:
#             target[i] = 55
#         elif target[i] < 5.25 and target[i] > 4.75:
#             target[i] = 50
#         elif target[i] < 4.75 and target[i] > 4.25:
#             target[i] = 45
#         elif target[i] < 4.25:
#             target[i] = 40
#     return target

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
    print("--- %s seconds ---" % (time.time() - start_time))


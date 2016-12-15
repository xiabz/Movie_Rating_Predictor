load Fisher.csv;

featuresTraining                        = [meas(1:30,:); meas(51:80,:); meas(101:130,:)];
featureSelectedTraining                 = featuresTraining(:,1:3);

groundTruthGroupTraining                = [species(1:30,:); species(51:80,:); species(101:130,:)];
[~, ~, groundTruthGroupNumTraining]     = unique(groundTruthGroupTraining);

featuresTesting                         = [meas(31:50,:); meas(81:100,:); meas(131:150,:)];
featureSelectedTesting                  = featuresTesting(:,1:3);

groundTruthGroupTesting                 = [species(31:50,:); species(81:100,:); species(131:150,:)];
[~, ~, groundTruthGroupNumTesting]      = unique(groundTruthGroupTesting);

% Train the classifier
optsStruct                              = ['-c ', num2str(2), ' -g ', num2str(4), '-b ', 1];
SVMClassifierObject                     = svmtrain(groundTruthGroupNumTraining, featureSelectedTraining, optsStruct);

optsStruct                              = ['-b ', 1];
[predLabelTesting, predictAccuracyTesting, ...
    predictScoresTesting]               = svmpredict(groundTruthGroupNumTesting, featureSelectedTesting, SVMClassifierObject, optsStruct);
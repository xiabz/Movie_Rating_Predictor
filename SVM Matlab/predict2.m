% read the dataset
tic
[movieTrainLabel, movieTrainData] = libsvmread('movie3');
NTrain = size(movieTrainData,1);
[movieTrainLabel, permIndex] = sortrows(movieTrainLabel);
movieTrainData = movieTrainData(permIndex,:);
[movieTestLabel, movieTestData] = libsvmread('movie3t');
NTest = size(movieTestData,1);
[movieTestLabel, permIndex] = sortrows(movieTestLabel);
movieTestData = movieTestData(permIndex,:);

% combine the data together just to fit my format
totalData = [movieTrainData; movieTestData];
totalLabel = [movieTrainLabel; movieTestLabel];

[N D] = size(totalData);
labelList = unique(totalLabel(:));
NClass = length(labelList);

% determine the train and test index
trainIndex = zeros(N,1);
trainIndex(1:NTrain) = 1;
testIndex = zeros(N,1);
testIndex((NTrain+1):N) = 1;
trainData = totalData(trainIndex==1,:);
trainLabel = totalLabel(trainIndex==1,:);
testData = totalData(testIndex==1,:);
testLabel = totalLabel(testIndex==1,:);

% Parameter selection using 10-fold cross validation
bestcv = 0;
for log2c = -1:1:3,
  for log2g = -4:1:2,
    cmd = ['-q -c ', num2str(2^log2c), ' -g ', num2str(2^log2g)];
    cv = get_cv_ac(trainLabel, trainData, cmd,10);
    if (cv >= bestcv),
      bestcv = cv; bestc = 2^log2c; bestg = 2^log2g;
    end
    fprintf('%g %g %g (best c=%g, g=%g, rate=%g)\n', log2c, log2g, cv, bestc, bestg, bestcv);
  end
end

% Train the SVM in one-vs-rest (OVR) mode
% #######################
bestParam = ['-t 2 -q -c ', num2str(bestc), ' -g ', num2str(bestg)];
model = ovrtrain(trainLabel, trainData, bestParam);
% #######################
% Classify samples using OVR model
% #######################
[predict_label, accuracy, prob_values] = ovrpredict(testLabel, testData, model);
fprintf('Accuracy = %g%%\n', accuracy * 100);
toc
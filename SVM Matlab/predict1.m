% read the dataset
tic
[movie_scale_label, movie_scale_inst] = libsvmread('movie2');
[N D] = size(movie_scale_inst);

% determine the train and test size
trainIndex = zeros(N,1);
trainIndex(1:2165) = 1;
testIndex = zeros(N,1);
testIndex(2166:N) = 1;
trainData = movie_scale_inst(trainIndex==1,:);
trainLabel = movie_scale_label(trainIndex==1,:);
testData = movie_scale_inst(testIndex==1,:);
testLabel = movie_scale_label(testIndex==1,:);



% Train the SVM
model = svmtrain(trainLabel, trainData, '-h 0 -c 1 -g 0.125 -b 1 -t 0');

% Use the SVM to classify the dataset
[predict_label, accuracy, prob_values] = svmpredict(testLabel, testData, model, '-b 1');
toc
% model = svmtrain(trainLabel, [(1:1900)' trainData*trainData'], '-c 1 -g 0.125 -b 1 -t 0');
% [predict_label, accuracy, prob_values] = svmpredict(testLabel, [(1:1901)' testData*trainData'], model, '-b 1');



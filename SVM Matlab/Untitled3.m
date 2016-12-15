% read the dataset
[movie_scale_label, movie_scale_inst] = libsvmread('movie_scale');
[N D] = size(movie_scale_inst);

% determine the train and test size
trainIndex = zeros(N,1);
trainIndex(1:1900) = 1;
testIndex = zeros(N,1);
testIndex(1901:N) = 1;
trainData = movie_scale_inst(trainIndex==1,:);
trainLabel = movie_scale_label(trainIndex==1,:);
testData = movie_scale_inst(testIndex==1,:);
testLabel = movie_scale_label(testIndex==1,:);

stepSize = 1;
log2c_list = -20:stepSize:20;
log2g_list = -20:stepSize:20;

numLog2c = length(log2c_list);
numLog2g = length(log2g_list);
cvMatrix = zeros(numLog2c,numLog2g);
bestcv = 0;
for i = 1:numLog2c
    log2c = log2c_list(i);
    for j = 1:numLog2g
        log2g = log2g_list(j);
        % -v 3 --> 3-fold cross validation
        param = ['-q -v 3 -c ', num2str(2^log2c), ' -g ', num2str(2^log2g)];
        cv = svmtrain(trainLabel, trainData, param);
        cvMatrix(i,j) = cv;
        if (cv >= bestcv),
            bestcv = cv; bestLog2c = log2c; bestLog2g = log2g;
        end
        % fprintf('%g %g %g (best c=%g, g=%g, rate=%g)\n', log2c, log2g, cv, bestc, bestg, bestcv);
    end
end
disp(['CV scale1: best log2c:',num2str(bestLog2c),' best log2g:',num2str(bestLog2g),' accuracy:',num2str(bestcv),'%']);

param = ['-q -c ', num2str(2^bestLog2c), ' -g ', num2str(2^bestLog2g), ' -b 1'];
bestModel = svmtrain(testLabel, testData, param);
[predict_label, accuracy, prob_values] = svmpredict(testLabel, testData, bestModel, '-b 1'); % test the training data


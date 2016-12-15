load('result.mat');
fileName = ('new_movie.xlsx');
% fileName = ('new_movie5.xlsx');
[data,titles,~] = xlsread(fileName);

data_norm = bsxfun(@minus, data, mu);
data_norm = bsxfun(@rdivide, data_norm, sigma);
data_reducted = data_norm * trsfm_mtx;

csv_file = 'data_test.csv';
% csv_file = 'data_test_5.csv';
dlmwrite(csv_file, data_reducted);

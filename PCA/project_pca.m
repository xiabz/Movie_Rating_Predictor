thshd_2 = 6;
thshd_31 = 5;
thshd_32 = 8;
content_saved = 90;
% get data from excel 
% fileName = 'movie_data_without_aspect.xlsx';
fileName = 'fianl_movie_selected_features.xlsx';
[data,titles,~] = xlsread(fileName);
data_ori = data;

% delete all rows have missing data
indexN = isnan(data);
indexN = sum(indexN,2);
data(indexN~=0,:) = [];

% delete cols with too many zero;
indexZ = isnan(data./0);
indexZ = sum(indexZ);
data(:,indexZ>1000) = [];
titles(:,indexZ>1000) = [];

% get imdb score out of data
col = strcmp(titles,'imdb_score');
score = data(:,col);
data = data(:,~col);
titles = titles(:,~col);
data_copy = data;
numOfSample = size(data,1);

% set different class
score_2 = score>=thshd_2;
idx_2 = find(score>=thshd_32);
idx_1 = find(score>=thshd_31 & score<thshd_32);
score_3 = zeros(numOfSample,1);
score_3(idx_1) = 1;
score_3(idx_2) = 2;

% before pca, do feature normalization
mu = mean(data);
sigma = std(data);
data_norm = bsxfun(@minus, data, mu);
data_norm = bsxfun(@rdivide, data_norm, sigma);

% writre data before pca out
csv_filename = 'data_before_pca.csv';
fid = fopen(csv_filename, 'w') ;
fprintf(fid, '%s,', titles{1,1:end-1}) ;
fprintf(fid, '%s\n', titles{1,end}) ;
fclose(fid) ;
dlmwrite(csv_filename, data_norm, '-append') ;

% do pca 0.9
[data_reducted_trn, trsfm_mtx, explained] = dms_rdct(data_norm, content_saved);
explained_plot = zeros(size(explained));
for i = 1: size(explained)
    explained_plot(i) = sum(explained(1:i)) ;
    
end
figure(1);
plot(1:size(explained), explained_plot);
xlabel('dimension', 'FontSize', 12);
ylabel('percentages of original data(%)', 'FontSize', 12);
title('Result of PCA', 'FontSize', 15);
grid on;

csv_file_1 = 'data_reducted.csv';
csv_file_2 = 'data_reducted_2.csv';
csv_file_3 = 'data_reducted_3.csv';
% csvwrite(csv_file, data_reducted_trn, 0, 0);

data_write = [ data_reducted_trn score];
dlmwrite(csv_file_1, data_write);

data_write_2 = [ data_reducted_trn score_2];
dlmwrite(csv_file_2, data_write_2);

data_write_3 = [ data_reducted_trn score_3];
dlmwrite(csv_file_3, data_write_3);

save('result.mat', 'mu', 'sigma', 'trsfm_mtx');
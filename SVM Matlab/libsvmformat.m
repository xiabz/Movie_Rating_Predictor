SPECTF = csvread('data_before_pca_3.csv'); % read a csv file
 labels = SPECTF(:, 1); % labels from the 1st column
 features = SPECTF(:, 2:end); 
 features_sparse = sparse(features); % features must be in a sparse matrix
 libsvmwrite('movieb3', labels, features_sparse);
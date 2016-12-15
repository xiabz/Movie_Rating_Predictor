function [ data_reducted, W, explained] = dms_rdct( data_norm, percent )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
%   data_reducted: the data set we use for classifiers after doing
%   dimension reduction.
%   W: transform matrix

% do pca
[coeff,score,latent,~,explained] = pca(data_norm,'Algorithm','svd','Centered',true);
total_latent = sum(latent);
% find the least number of principle compoents that can explain most of variability in data 
for d = 1:size(explained)
    if ( (sum(explained(1:d)) ) >= percent ) 
        break;
    end
end

% construct the transform matrix with dimension 
cov = 1 / size(data_norm,1) * data_norm' * data_norm;
[U,S,V] = svd(cov);

% reduction
W = U(:,1:d);
data_reducted = data_norm * W;


end


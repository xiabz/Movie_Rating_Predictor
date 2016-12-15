clear;
clc;
close all;

data = csvread('data_reducted.csv');
trainingData = data(:,1:8);
trainingLabel = data(:,9);
testData = csvread('data_test.csv');
k = 35;

target = knnclassify(testData,trainingData,trainingLabel,k,'cosine','nearest');        

 



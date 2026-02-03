% Load datasets
data_updated = readtable('california_housing_updated.csv');
data_1990 = readtable('california_housing_1990.csv');

clc; % Clear Command Window

% Display number of entires before cleaning
fprintf('Number of entries in 1990 dataset: %d\n', height(data_1990));
fprintf('Number of entries in updated dataset: %d\n', height(data_updated));

% Show summary of data
summary(data_1990)
summary(data_updated)

% Remove entries with missing data
data_updated = rmmissing(data_updated);
data_1990 = rmmissing(data_1990);

% Check for rows that have a -666666666 entry
rowsToDelete = any(data_updated{:, 2:10} == -666666666, 2);

% Remove rows only if there are any to delete
if any(rowsToDelete)
    data_updated(rowsToDelete, :) = [];
end

% In ocean_proximity column, rename "ISLAND" entires, to "NEAR OCEAN" in
% the 1990 data set
data_1990.ocean_proximity(strcmp(data_1990.ocean_proximity, 'ISLAND')) = {'NEAR OCEAN'};

% Display number of entries after cleaning
fprintf('Number of entries in cleaned 1990 dataset: %d\n', height(data_1990));
fprintf('Number of entries in cleaned updated dataset: %d\n', height(data_updated));

% Show new summary
summary(data_1990);
summary(data_updated);

% Write cleaned data sets
writetable(data_updated, 'cleaned_california_housing_updated.csv');
writetable(data_1990, 'cleaned_california_housing_1990.csv');
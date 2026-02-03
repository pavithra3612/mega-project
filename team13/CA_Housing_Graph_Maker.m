% Load cleaned data sets
cl_data_1990 = readtable('cleaned_california_housing_1990.csv');
cl_data_updated = readtable('cleaned_california_housing_updated.csv');

summary(cl_data_1990);
summary(cl_data_updated);

%% --- Pie Charts for "ocean_proximity" ---
figure;
subplot(1, 2, 1);
pie(categorical(cl_data_1990.ocean_proximity));
title('Ocean Proximity - 1990 Data');

subplot(1, 2, 2);
pie(categorical(cl_data_updated.ocean_proximity));
title('Ocean Proximity - Updated Data');

%% --- Grouped Bar Chart: Median House Value by Age Range ---
edges = [0 10 20 30 40 50 60 70 80 100];

[~,~,bins_1990] = histcounts(cl_data_1990.housing_median_age, edges);
[~,~,bins_updated] = histcounts(cl_data_updated.average_house_age, edges);

mean_value_1990 = accumarray(bins_1990(~isnan(bins_1990)), ...
    cl_data_1990.median_house_value(~isnan(bins_1990)), [], @mean);
mean_value_updated = accumarray(bins_updated(~isnan(bins_updated)), ...
    cl_data_updated.median_house_value(~isnan(bins_updated)), [], @mean);

xlabels = {'0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80+'};

len = min(length(mean_value_1990), length(mean_value_updated));
mean_value_1990 = mean_value_1990(1:len);
mean_value_updated = mean_value_updated(1:len);
xlabels = xlabels(1:len);

figure;
bar(categorical(xlabels), [mean_value_1990 mean_value_updated], 'grouped');
xlabel('Housing Age Range');
ylabel('Average Median House Value ($)');
title('Comparison of Housing Median Age and Value');
legend('1990 Data', 'Updated Data', 'Location', 'northoutside', 'Orientation', 'horizontal');
colormap([0.2 0.4 0.8; 0.9 0.4 0.2]);
set(gca, 'YGrid', 'on', 'Box', 'off');


%% --- Grouped Bar Chart: Median House Value by Ocean Proximity ---

% Get unique categories of ocean proximity
categories_1990 = categories(categorical(cl_data_1990.ocean_proximity));
categories_updated = categories(categorical(cl_data_updated.ocean_proximity));

% Merge categories to make sure both sets have the same labels
all_categories = unique([categories_1990; categories_updated]);

% Preallocate
mean_value_1990 = nan(length(all_categories), 1);
mean_value_updated = nan(length(all_categories), 1);

% Compute mean median house value per ocean proximity group
for i = 1:length(all_categories)
    group = all_categories{i};
    
    % 1990
    idx_1990 = strcmp(cl_data_1990.ocean_proximity, group);
    if any(idx_1990)
        mean_value_1990(i) = mean(cl_data_1990.median_house_value(idx_1990), 'omitnan');
    end
    
    % Updated
    idx_updated = strcmp(cl_data_updated.ocean_proximity, group);
    if any(idx_updated)
        mean_value_updated(i) = mean(cl_data_updated.median_house_value(idx_updated), 'omitnan');
    end
end

% Plot grouped bar chart
figure;
bar(categorical(all_categories), [mean_value_1990 mean_value_updated], 'grouped');
xlabel('Ocean Proximity');
ylabel('Average Median House Value ($)');
title('Comparison of Median House Value by Ocean Proximity');
legend('1990 Data', 'Updated Data', 'Location', 'northoutside', 'Orientation', 'horizontal');
colormap([0.2 0.4 0.8; 0.9 0.4 0.2]);
set(gca, 'YGrid', 'on', 'Box', 'off');


%% --- Box Plot: Distribution Comparison ---
figure;

boxplot([cl_data_1990.median_house_value; cl_data_updated.median_house_value], ...
        [repmat({'1990'}, height(cl_data_1990), 1);
         repmat({'Updated'}, height(cl_data_updated), 1)]);
title('Comparison of Median House Value Distributions');
ylabel('Median House Value ($)');

% Print the max and min "median_house_value" value in each dataset
max_value_1990 = max(cl_data_1990.median_house_value, [], 'omitnan');
min_value_1990 = min(cl_data_1990.median_house_value, [], 'omitnan');
max_value_updated = max(cl_data_updated.median_house_value, [], 'omitnan');
min_value_updated = min(cl_data_updated.median_house_value, [], 'omitnan');

fprintf('1990 Data: Max = $%.2f, Min = $%.2f\n', max_value_1990, min_value_1990);
fprintf('Updated Data: Max = $%.2f, Min = $%.2f\n', max_value_updated, min_value_updated);

% Double bar graph displaying the number of blocks that number of houses
% that fall into a certain price range
% Extract the median house values
vals_1990 = cl_data_1990.median_house_value;
vals_updated = cl_data_updated.median_house_value;

% Define the bin edges (last bin covers >500k)
edges = [0 100000 200000 300000 400000 500000 Inf];

% Compute counts for each dataset
counts_1990 = histcounts(vals_1990, edges);
counts_updated = histcounts(vals_updated, edges);

% Create labels for each bin
labels = { ...
    '0–100k', ...
    '100–200k', ...
    '200–300k', ...
    '300–400k', ...
    '400–500k', ...
    '>500k'};

% Create a double bar graph
figure;
bar([counts_1990; counts_updated].')
xlabel('Median House Value Range ($)');
ylabel('Number of Blocks');
title('Comparison of Median House Value Distribution (1990 vs Updated)');
legend('1990 Data','Updated Data');
set(gca, 'XTickLabel', labels, 'FontSize', 12);
xtickangle(45);
grid on;

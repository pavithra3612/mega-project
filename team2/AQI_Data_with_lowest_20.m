%% =========================
%   Load Data
% ==========================
clear; clc;

filename = "data_date.csv";   % your dataset
T = readtable(filename);

% Make sure types are correct
T.Date = datetime(T.Date,'InputFormat','yyyy-MM-dd');
T.AQIValue = double(T.AQIValue);

%% =========================
%   Compute Average AQI per Country
% ==========================
countryAvg = groupsummary(T, "Country", "mean", "AQIValue");

% Sort by ascending (lowest = best air)
countryAvg = sortrows(countryAvg, "mean_AQIValue", "ascend");

% Select lowest 20
lowest20 = countryAvg(1:20, :);

fprintf("\n=== LOWEST 20 COUNTRIES (BEST AIR QUALITY) ===\n");
disp(lowest20);

%% =========================
%   PIE CHART OF 20 BEST
% ==========================
figure;
pie(lowest20.mean_AQIValue);
title("20 Countries With Best (Lowest) Average AQI");
legend(lowest20.Country, "Location", "eastoutside");

%%graphs for cleaned over crowding data
clc; clear;


T = readtable('cleaned_overcrowding_data_.csv');

%convert cell names to strings
if iscell(T.geotype);      T.geotype      = string(T.geotype);      end
if iscell(T.race_name);    T.race_name    = string(T.race_name);    end
if iscell(T.reportyear);   T.reportyear   = string(T.reportyear);   end
if iscell(T.county_name);  T.county_name  = string(T.county_name);  end
if iscell(T.location);     T.location     = string(T.location);     end

%years to focus on
yr = "2006-2010";


%Graph 1: Overcrowding by Race/Ethnicity


%filter for rows for that year
state = T(T.geotype == "CA" & T.reportyear == yr, :);

%sort races by overcrowding percent (highest first)
[~, idx] = sort(state.pct_overcrowded_calc, 'descend');
state = state(idx, :);

figure;
bar(categorical(state.race_name), state.pct_overcrowded_calc);

xlabel('Race / Ethnicity');
ylabel('Percent Overcrowded (%)');
title("Household Overcrowding by Race/Ethnicity in California (" + yr + ")");
grid on;



%graph 2: Overcrowding by County for Total Population

race = "Total";

%filter for county level data
county = T(T.geotype == "CO" & T.race_name == race & T.reportyear == yr, :);

%sort counties by overcrowding percent
[~, idx2] = sort(county.pct_overcrowded_calc, 'ascend');
county = county(idx2, :);

figure;
barh(categorical(county.county_name), county.pct_overcrowded_calc);

ylabel('County');
xlabel('Percent Overcrowded (%)');
title("Household Overcrowding by County (" + race + ", " + yr + ")");
grid on;

%change font size of county to read
set(gca, 'FontSize', 8);

%Clean overcrowding dataset

clc; clear;

filename = 'hci_housing_crowding_137_ca_re_co_cd_pl_ct_overcrowding_total2017-11-06.csv';

% Detect import options with correct settings
opts = detectImportOptions(filename, ...
    'Delimiter', ',', ...                 % CSV: comma-separated
    'TextType', 'string', ...             % keep text as string
    'PreserveVariableNames', true);       % keep original column names

%clean header, data lines, and colunms
opts.VariableNamesLine = 1;               
opts.DataLines        = [2 Inf];         

opts.ExtraColumnsRule = 'ignore';
opts.EmptyLineRule    = 'read';

% Read the table
T = readtable(filename, opts);

% Quick sanity check
disp('Original table size [rows, cols]:');
disp(size(T));
disp('First few columns/rows of raw data:');
disp(T(1:5, 1:8));

%%delete useless colunms
colsToRemove = { ...
    'ind_definition', ...
    'version', ...
    'CA_decile', ...
    'CA_RR', ...
    'se', ...
    'rse'};
keepCols = setdiff(T.Properties.VariableNames, colsToRemove);
T = T(:, keepCols);

%change numbered columns to double
numericCols = {'numerator', 'denominator', 'estimate', 'll_95ci', 'ul_95ci'};
for k = 1:numel(numericCols)
    col = numericCols{k};
    if ismember(col, T.Properties.VariableNames)
        % If stored as string or cellstr, convert to double
        if isstring(T.(col)) || iscellstr(T.(col))
            T.(col) = str2double(T.(col));
        end
    end
end
%fill missing county_name with Statewide
if ismember("county_name", T.Properties.VariableNames)
    T.county_name = fillmissing(T.county_name, 'constant', "Statewide");
end

% delete rows where numerator or denominator is missing
varsNeeded = intersect({'numerator','denominator'}, T.Properties.VariableNames);
T = rmmissing(T, 'DataVariables', varsNeeded);


%calculated columns

% Percent overcrowded = numerator / denominator * 100
if all(ismember({'numerator','denominator'}, T.Properties.VariableNames))
    T.pct_overcrowded_calc = T.numerator ./ T.denominator * 100;
end

% Difference between calculated percent and given estimate
if all(ismember({'pct_overcrowded_calc','estimate'}, T.Properties.VariableNames))
    T.estimate_diff = T.pct_overcrowded_calc - T.estimate;
end




%save cleaned table to a CSV file

outFile = 'cleaned_overcrowding_data_fixed.csv';
writetable(T, outFile);


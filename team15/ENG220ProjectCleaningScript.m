T = readtable("insurance.csv");

%2.Cleans missing or invalid values
T = standardizeMissing(T, {'', 'NA', 'N/A', 'null'});
T = rmmissing(T, 'DataVariables', {'sex', 'region'});

%3.Clean numeric columns
T.age = str2double(string(T.age));
T.bmi = str2double(string(T.bmi));
T.children = str2double(string(T.children));
T.charges = str2double(string(T.charges));


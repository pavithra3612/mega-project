clc;
clear;
close all;

T = readtable("Food_Production.csv");

for i = 2:width(T)   % loop through each column of the table
    if iscell(T.(i)) || isstring(T.(i)) || ischar(T.(i))
        % Try converting text/cell/string columns to numeric
        T.(i) = str2double(string(T.(i)));
    end
    
    if isnumeric(T.(i))
        % Replace NaN with 0
        T.(i)(isnan(T.(i))) = 0;
    end
end


disp(T);
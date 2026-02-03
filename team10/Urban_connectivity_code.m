


data = readtable('urban_connectivity.csv');


cities = data.City;
states = data.State;
walk = data.("WalkScore");
transit = data.("TransitScore");
bike = data.("BikeScore");


isABQ = strcmpi(cities, 'Albuquerque') & strcmpi(states, 'NM');
if ~any(isABQ)
    error('Albuquerque, NM not found in dataset.');
end


abq_walk = walk(isABQ);
abq_transit = transit(isABQ);
abq_bike = bike(isABQ);


avg_walk = mean(walk(~isABQ), 'omitnan');
avg_transit = mean(transit(~isABQ), 'omitnan');
avg_bike = mean(bike(~isABQ), 'omitnan');



sorted_walk = sort(walk, 'descend', 'MissingPlacement', 'last');
sorted_transit = sort(transit, 'descend', 'MissingPlacement', 'last');
sorted_bike = sort(bike, 'descend', 'MissingPlacement', 'last');


top10_walk = mean(sorted_walk(1:10), 'omitnan');
top10_transit = mean(sorted_transit(1:10), 'omitnan');
top10_bike = mean(sorted_bike(1:10), 'omitnan');


categories = {'Walk Score', 'Transit Score', 'Bike Score'};
abq_scores = [abq_walk, abq_transit, abq_bike];
avg_scores = [avg_walk, avg_transit, avg_bike];
top10_scores = [top10_walk, top10_transit, top10_bike];


figure;
bar([abq_scores; avg_scores; top10_scores]')
set(gca, 'XTickLabel', categories)
legend({'Albuquerque, NM', 'Average of All Other Cities', 'Average of Top 10 Cities'}, ...
       'Location', 'northoutside', 'Orientation', 'horizontal')
title('Walkability Comparison: Albuquerque vs. U.S. Averages and Top 10 Cities')
ylabel('Score')
ylim([0 100])
grid on


fprintf('\nWalkability Comparison Summary:\n');
fprintf('------------------------------------------------------\n');
fprintf('Category        Albuquerque   All Others   Top 10 Avg\n');
fprintf('------------------------------------------------------\n');
fprintf('Walk Score      %6.1f         %6.1f        %6.1f\n', abq_walk, avg_walk, top10_walk);
fprintf('Transit Score   %6.1f         %6.1f        %6.1f\n', abq_transit, avg_transit, top10_transit);
fprintf('Bike Score      %6.1f         %6.1f        %6.1f\n', abq_bike, avg_bike, top10_bike);
fprintf('------------------------------------------------------\n');


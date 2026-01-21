% Sample data (replace with your own)
categories = {'Housing', 'Food', 'Transportation', 'Healthcare', 'Entertainment'};
costs = [1200, 450, 300, 200, 150]; % Monthly costs in USD
x = 1:length(costs);

% Line Plot
figure;
plot(x, costs, '-o', 'LineWidth', 2);
title('Monthly Cost of Living - Line Plot');
xlabel('Category Index');
ylabel('Cost (USD)');
xticks(x);
xticklabels(categories);
grid on;

% Bar Chart
figure;
bar(costs);
title('Monthly Cost of Living - Bar Chart');
xlabel('Category');
ylabel('Cost (USD)');
set(gca, 'XTickLabel', categories);
grid on;

% Pie Chart
figure;
pie(costs, categories);
title('Monthly Cost Distribution - Pie Chart');

% Scatter Plot
figure;
scatter(x, costs, 100, 'filled');
title('Monthly Cost of Living - Scatter Plot');
xlabel('Category Index');
ylabel('Cost (USD)');
xticks(x);
xticklabels(categories);
grid on;

% Histogram (simulated expenses)
expenses = randi([100, 1500], 1, 100); % Random expense data
figure;
histogram(expenses, 10);
title('Distribution of Monthly Expenses - Histogram');
xlabel('Expense Amount (USD)');
ylabel('Frequency');
grid on;

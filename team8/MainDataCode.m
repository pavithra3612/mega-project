%Download both of the data set's csv's into matlab directly 
%for the code to work

data = readtable("FinalProjectDataPt2.csv", 'VariableNamingRule', 'modify');

data.HPSAScore = str2double(data.HPSAScore);

MainScoreCol=data.HPSAScore;

CleanScoreCol = rmmissing(MainScoreCol);

fprintf("Average HPSA Score for New Mexico:")
mean(CleanScoreCol, "all")

%Creating a bar graph with the data

tiledlayout(3, 1);

nexttile;
bar(CleanScoreCol, 1,'grouped', "red");
title("HSPA Score Within NM");
xlabel("Different Disciplines in NM");
ylabel("Different HSPA Scores");

%Cali Data
CaliData = readtable("CaliDataFinal.csv", 'VariableNamingRule', 'modify');

%CaliData.HPSAScore = str2double(CaliData.HPSAScore);

CaliScoreCol=CaliData.HPSAScore;

CaliClean = rmmissing(CaliScoreCol);

fprintf("Average HPSA Score for California:")
mean(CaliClean, "all")

%Creating a bar graph with the data

nexttile;
bar(CaliClean, 1,'grouped', "blue");
title("HSPA Score Within California");
xlabel("Different Disciplines in Calirfornia");
ylabel("Different HSPA Scores");

%MassachusettsData

MassData = readtable("MassachusettsData.csv", 'VariableNamingRule', 'modify');

MassData.Var8 = str2double(MassData.Var8);

MassCol=MassData.Var8;

CleanMassCol = rmmissing(MassCol);

fprintf("Average HPSA Score for Massachussettes:")
mean(CleanMassCol, "all")



%Creating a bar graph with the data

nexttile;
bar(CleanMassCol, 1,'grouped', "green");
title("HSPA Score Within Massachussettes");
xlabel("Different Disciplines in Massachussettes");
ylabel("Different HSPA Scores");

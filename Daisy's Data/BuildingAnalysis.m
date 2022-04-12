clear all
clc

set(0, 'DefaultLineLineWidth', 2);
set(0,'defaultAxesFontSize',24);

% Building 9 %
%M9STMFLOW	
%M9CHWTONS	
%M9TFRARealPower	
%M9TFRBRealPower

% Building 76 %
% M76STMFLOW	
% M76CHWTONS	
% M76TFRARealPower	
% M76TFRBRealPower	
% M76TFRCRealPower	
% M76TFRDRealPower

% Building E60 %
% E60STMFLOW	
% E60CHWTONS	
% E62_BREAKER_E60_SB1_RealPower

% Temperature Data %
% Month 
% Day
% Hour
% Temp - Normal (F)
% Temp - DewP (F)
% Temp - Normal (C)
% Temp - DewP (C)

% Conversions
% 1kwh = 3412.14 BTU
% 1 THR = 12000 BTU
% 1 lbs steam = 1100 BTU

% Square feet
% Building 9: 77,414  
% Building 76: 367,689
% Building E60: 30,130


% Convert to BTU %
PowertoBTU = 3412.14;
CWtoBTU = 12000;
SteamtoBTU = 1100;

% Building Area %
Bldg9SF = 77414;
Bldg76SF = 367689;

% Process Loads %
Bldg9SteamProcess = 6;
Bldg9CWProcess = 5;
Bldg76SteamProcess = 9;
Bldg76CWProcess = 4;

% Import Data %
data9 = importdata('Building9.csv').data;
data76 = importdata('Building76.csv').data;
Energy9 = abs(data9(:,1:4));
Energy9(4441:end,2) = Energy9(4441:end,2)*2.4094;
Energy76 = abs(data76(:,1:6));

tempF = data9(:,6);

% time vector %
t1 = datetime(2019,1,1,0,0,0);
t2 = datetime(2019,12,30,23,0,0);
time_full = t1:hours(1):t2;

% time vector of interest %
t3 = datetime(2019,1,1,0,0,0);
t4 = datetime(2019,12,30,23,0,0);
time_short = t3:hours(1):t4;

[time,IA,IB] = intersect(time_full,time_short);

Energy9 = Energy9(IA,:);
Energy76 = Energy76(IA,:);
tempF = tempF(IA,:);

%  Building 9 %
Bldg9Steam = Energy9(:,1)*SteamtoBTU;
Bldg9CW = Energy9(:,2)*CWtoBTU;
Bldg9Power = (Energy9(:,3) + Energy9(:,4))*PowertoBTU;
% normalize by area
Bldg9SteamPerSF = Bldg9Steam/Bldg9SF;
Bldg9CWPerSF = Bldg9CW/Bldg9SF;
Bldg9PowerPerSF = Bldg9Power/Bldg9SF;
Bldg9TotalPerSF = Bldg9SteamPerSF + Bldg9CWPerSF + Bldg9PowerPerSF;

% Building 76 %
Bldg76Steam = Energy76(:,1)*SteamtoBTU;
Bldg76CW = Energy76(:,2)*CWtoBTU;
Bldg76Power = (Energy76(:,3) + Energy76(:,4) + Energy76(:,5) + Energy76(:,6))*PowertoBTU;
% normalize by area
Bldg76SteamPerSF = Bldg76Steam/Bldg76SF;
Bldg76CWPerSF = Bldg76CW/Bldg76SF;
Bldg76PowerPerSF = Bldg76Power/Bldg76SF;
Bldg76TotalPerSF = Bldg76SteamPerSF + Bldg76CWPerSF + Bldg76PowerPerSF;

% Remove Process Load
% Bldg9SteamPerSF = Bldg9SteamPerSF - Bldg9SteamProcess;
% Bldg9CWPerSF = Bldg9CWPerSF - Bldg9CWProcess;
% Bldg76SteamPerSF = Bldg76SteamPerSF - Bldg76SteamProcess;
% Bldg76CWPerSF = Bldg76CWPerSF - Bldg76CWProcess;

Bldg9VsTemp = [tempF Bldg9CWPerSF Bldg9SteamPerSF Bldg9PowerPerSF];
Bldg76VsTemp = [tempF Bldg76CWPerSF Bldg76SteamPerSF Bldg76PowerPerSF];

Bldg9TotalWithoutProcess = Bldg9SteamPerSF + Bldg9CWPerSF;
Bldg76TotalWithoutProcess = Bldg76SteamPerSF + Bldg76CWPerSF;
ChngPts9 = findchangepts(Bldg9TotalWithoutProcess,'Statistic','linear','MaxNumChanges',2);
ChngPts76 = findchangepts(Bldg76TotalWithoutProcess,'Statistic','linear','MaxNumChanges',2);

TempPts9 = tempF(ChngPts9)
TempPts76 = tempF(ChngPts76)

figure
scatter(tempF,Bldg9VsTemp(:,2),'filled'); hold all
scatter(tempF,Bldg9VsTemp(:,3),'filled');
xlabel('Ambient Dry Bulb Temperature, F');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building 9');
ylim([0 80]);
grid on
set(gcf,'color','w');

figure
scatter(tempF,Bldg76VsTemp(:,2),'filled'); hold all
scatter(tempF,Bldg76VsTemp(:,3),'filled');
xlabel('Ambient Dry Bulb Temperature, F');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building 76');
grid on
ylim([0 80]);
set(gcf,'color','w');

figure 
area(time,Bldg76CWPerSF,'EdgeColor','none'); hold all
area(time,-Bldg76SteamPerSF,'EdgeColor','none')
xlabel('Date');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building 76');
ylim([-100 80]);
grid on
set(gcf,'color','w');

figure 
area(time,Bldg9CWPerSF,'EdgeColor','none'); hold all
area(time,-Bldg9SteamPerSF,'EdgeColor','none');
xlabel('Date');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building 9');
ylim([-100 80]);
grid on
set(gcf,'color','w');

figure
pie([sum(Bldg76Steam) sum(Bldg76CW) sum(Bldg76Power)]);
legend('Steam','Chilled Water','Electricity');
title('Building 76');
set(gcf,'color','w');

figure
pie([sum(Bldg9Steam) sum(Bldg9CW) sum(Bldg9Power)]);
title('Building 9');
legend('Steam','Chilled Water','Electricity');
set(gcf,'color','w');



%% Building E60 2018

clear all
clc

% Convert to BTU %
PowertoBTU = 3412.14;
CWtoBTU = 12000;
SteamtoBTU = 1100;

% Building Area %
BldgE60SF = 30130;

% Process Loads %
BldgE60SteamProcess = 2;
BldgE60CWProcess = 0;

% Import Data %
dataE60 = importdata('BuildingE60_2018.csv').data;
EnergyE60 = abs(dataE60(:,1:3));
tempF = dataE60(:,5);

% time vector %
t1 = datetime(2018,1,1,0,0,0);
t2 = datetime(2018,12,31,23,0,0);
time_full = t1:hours(1):t2;

% time vector of interest %
t3 = datetime(2018,1,1,0,0,0);
t4 = datetime(2018,12,31,23,0,0);
time_short = t3:hours(1):t4;

[time,IA,IB] = intersect(time_full,time_short);

EnergyE60 = EnergyE60(IA,:);
tempF = tempF(IA,:);

% Building E60 %
BldgE60Steam = EnergyE60(:,1)*SteamtoBTU;
BldgE60CW = EnergyE60(:,2)*CWtoBTU;
BldgE60Power = EnergyE60(:,3)*PowertoBTU;
% normalize by area
BldgE60SteamPerSF = BldgE60Steam/BldgE60SF;
BldgE60CWPerSF = BldgE60CW/BldgE60SF;
BldgE60PowerPerSF = BldgE60Power/BldgE60SF;
BldgE60TotalPerSF = BldgE60SteamPerSF + BldgE60CWPerSF + BldgE60PowerPerSF;

BldgE60SteamPerSF = BldgE60SteamPerSF - BldgE60SteamProcess;
BldgE60CWPerSF = BldgE60CWPerSF - BldgE60CWProcess;

BldgE60VsTemp = [tempF BldgE60CWPerSF BldgE60SteamPerSF BldgE60PowerPerSF];

figure
scatter(tempF,BldgE60VsTemp(:,2),'filled'); hold all
scatter(tempF,BldgE60VsTemp(:,3),'filled');
xlabel('Ambient Dry Bulb Temperature, F');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building E60');
ylim([0 80]);
grid on
set(gcf,'color','w');

figure 
area(time,BldgE60CWPerSF,'EdgeColor','none'); hold all
area(time,-BldgE60SteamPerSF,'EdgeColor','none')
xlabel('Date');
ylabel('BTU/ft^2');
legend('Chilled Water','Steam');
title('Building E60');
ylim([-100 80]);
grid on
set(gcf,'color','w');


figure
pie([sum(BldgE60Steam) sum(BldgE60CW) sum(BldgE60Power)]);
legend('Steam','Chilled Water','Electricity');
title('Building E60');
set(gcf,'color','w');


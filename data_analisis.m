% === Leggi il file CSV ===
filename = 'smartmotor_data.csv';  % Sostituisci con il tuo nome file
data = readtable(filename);

% === Parametro di sottocampionamento ===
N = 10;  % Usa 1 dato ogni N (modifica a piacere)

% === Estrai e sottocampiona le colonne ===
time = data.timestamp_ms(1:N:end) / 1000;  % da ms a secondi
currentSpeed = data.currentSpeed(1:N:end);
targetSpeed = data.targetSpeed(1:N:end);
PIDOutput = data.PIDOutput(1:N:end);
POutput = data.POutput(1:N:end);
IOutput = data.IOutput(1:N:end);
DOutput = data.DOutput(1:N:end);

% === Plot velocità ===
figure;
subplot(2,1,1);
plot(time, currentSpeed, 'b', 'LineWidth', 1.5);
hold on;
plot(time, targetSpeed, 'r--', 'LineWidth', 1.5);
xlabel('Tempo [s]');
ylabel('Velocità [unità]');
legend('Velocità Attuale', 'Velocità Target');
title(['Andamento Velocità (1 ogni ' num2str(N) ' dati)']);
grid on;

% === Plot PID output ===
subplot(2,1,2);
plot(time, PIDOutput, 'g', 'LineWidth', 1.5); hold on;
plot(time, POutput, 'm', 'LineWidth', 1.5);
plot(time, IOutput, 'c', 'LineWidth', 1.5);
plot(time, DOutput, 'k', 'LineWidth', 1.5);
xlabel('Tempo [s]');
ylabel('Valore PID');
title(['Analisi PID (1 ogni ' num2str(N) ' dati)']);
legend('PIDOutput', 'POutput', 'IOutput', 'DOutput');
grid on;

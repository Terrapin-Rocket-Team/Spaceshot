%% Main
clear
clc

%% Changeable Parameters
% Diameters: .075 (75mm), .1016 (4in), .1524 (6in)
D_b = .1524; % m
D_s = .1016; % m
motor_casing_yield_strength = 276E6; % Pa 6061 Aluminum
motor_casing_density = 2700; % kg/m^3 6061 Aluminum
%altitude = 10000; % m Karman line
dV = 2200; %m/s (delta-V) https://space.stackexchange.com/questions/27898/what-is-the-delta-v-equivalent-to-cross-the-k%C3%A1rm%C3%A1n-line-in-vertical-suborbital

%% Constant Parameters
Isp = 180; % s based on 2025 pdr value
propellant_density = 1702; % kg/m^3 based on 2025 pdr value
pressure_chamber = 7E6; % Pa TODO update this -- based on pdr values
me_b = 10; % kg
me_s = 10; % kg

% Find casing thicknesses
%t_s = thickness(pressure_chamber, D_s, motor_casing_yield_strength, 4);
%t_b = thickness(pressure_chamber, D_b, motor_casing_yield_strength, 4);
t_s = 0.00635; % m (.25 in) SAC 2025
t_b = 0.00635; % m (.25 in) SAC 2025

% Initialize arrays for storing values
x_vals = 0.25:0.001:0.75;
L_s_vals = zeros(size(x_vals));
L_b_vals = zeros(size(x_vals));
L0_vals = zeros(size(x_vals));
M_s_vals = zeros(size(x_vals));
M_b_vals = zeros(size(x_vals));
M0_vals = zeros(size(x_vals));

% Calculate values for each x
for i = 1:length(x_vals)
    x = x_vals(i);
    
    % Calculate delta-V for each stage
    dVb = dV * x;
    dVs = dV * (1 - x);
    
    % Resolve sustainer dimensions and mass
    L_s = lengthStage(D_s, me_s, t_s, dVs, Isp, motor_casing_density, propellant_density);
    m_s = me_s + massProp(L_s, propellant_density, D_s, t_s) + massCasing(L_s, motor_casing_density, D_s, t_s);

    % Resolve booster dimensions and mass
    L_b = lengthStage(D_b, me_b + m_s, t_b, dVb, Isp, motor_casing_density, propellant_density);
    m_b = me_b + m_s + massProp(L_b, propellant_density, D_b, t_b) + massCasing(L_b, motor_casing_density, D_b, t_b);

    % Total length and mass
    L0 = L_s + L_b;
    m0 = m_s + m_b;

    % Store results
    L_s_vals(i) = L_s;
    L_b_vals(i) = L_b;
    L0_vals(i) = L0;
    M_s_vals(i) = m_s;
    M_b_vals(i) = m_b;
    M0_vals(i) = m0;
end

%% Plotting

% Plot 1: L_s, L_b, L0 vs x
figure;
plot(x_vals, L_s_vals, 'DisplayName', 'L_s (Sustainer Length)');
hold on;
plot(x_vals, L_b_vals, 'DisplayName', 'L_b (Booster Length)');
plot(x_vals, L0_vals, 'DisplayName', 'L0 (Total Length)');
hold off;
xlabel('Delta-V Fraction (x)');
ylabel('Length (m)');
title('L_s, L_b, L0 vs x');
xlim([min(x_vals), max(x_vals)])
legend;

% Plot 2: M_s, M_b, M0 vs x
figure;
plot(x_vals, M_s_vals, 'DisplayName', 'M_s (Sustainer Mass)');
hold on;
plot(x_vals, M_b_vals, 'DisplayName', 'M_b (Booster Mass)');
plot(x_vals, M0_vals, 'DisplayName', 'M0 (Total Mass)');
hold off;
xlabel('Delta-V Fraction (x)');
ylabel('Mass (kg)');
title('M_s, M_b, M0 vs x');
xlim([min(x_vals), max(x_vals)])
legend;

fprintf('Sustainer Thickness (t_s): %.4f m (%.4f inches)\n', t_s, t_s * 39.3701);
fprintf('Booster Thickness (t_b): %.4f m (%.4f inches)\n', t_b, t_b * 39.3701);










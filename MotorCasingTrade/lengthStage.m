function L = lengthStage(D, m_pl, t, dV, Isp, rhoc, rhop)
% lengthStage - Calculates the required length of a rocket stage for a given payload and design parameters.
% This function uses the rocket equation, taking into account the structural and propellant volumes.
%
% Inputs:
%   D        - Outer diameter of the rocket stage (m)
%   m_pl     - Payload mass (kg)
%   t        - Wall thickness of the casing (m)
%   dV       - Required change in velocity (delta-V) for the stage (m/s)
%   Isp      - Specific impulse of the rocket engine (s)
%   rhoc     - Density of the casing material (kg/m^3)
%   rhop     - Density of the propellant (kg/m^3)
%
% Output:
%   L        - Required length of the rocket stage (m)

g0 = 9.81; % m/s^2

r = D/2;
area_casing = pi*(r^2 - (r - t)^2); % Cross-sectional area of the casing
area_prop = pi*((r-t)^2); % Cross-sectional area of the propellant region

massRatio = exp(dV/(Isp*g0));

L = (m_pl - massRatio*m_pl)/(massRatio*area_casing*rhoc - area_casing*rhoc - area_prop*rhop); % rocket equation


end
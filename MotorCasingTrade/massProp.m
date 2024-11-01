function m = massProp(L, rho, D,t )
% massProp - Calculates the mass of the propellant inside a cylindrical casing.
% This function calculates the propellant mass based on the casing geometry and
% an adjustable volume loading parameter, which represents the proportion of the casing filled with propellant.
%
% Inputs:
%   L               - Length of the casing (m)
%   rho             - Density of the propellant (kg/m^3)
%   D               - Outer diameter of the casing (m)
%   t               - Wall thickness of the casing (m)
%
% Output:
%   m               - Mass of the propellant (kg)

volume_loading = .8; % this is an adjustable parameter (SAC 2025 was .84). It is how much of the casing is full of propellant
r = D/2;
m = L*rho*volume_loading*(pi*((r-t)^2));

end
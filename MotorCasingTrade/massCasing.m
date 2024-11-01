function m = massCasing(L, rho, D, t)
% massCasing - Calculates the mass of a cylindrical casing with a given wall thickness.
% This function assumes a thin-walled cylindrical structure.
%
% Inputs:
%   L        - Length of the casing (m)
%   rho      - Density of the casing material (kg/m^3)
%   D        - Outer diameter of the casing (m)
%   t        - Wall thickness of the casing (m)
%
% Output:
%   m        - Mass of the casing (kg)

r = D/2;
m = L*rho*(pi*(r^2 - (r - t)^2));

end
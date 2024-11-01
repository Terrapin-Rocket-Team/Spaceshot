function t = thickness(Pc, D, sigma_y, sf)
% thickness - Calculates the required wall thickness for a thin-walled pressure vessel.
% This function calculates based on hoop stress failure.
%
% Inputs:
%   Pc       - Chamber pressure in the pressure vessel (Pa)
%   D        - Diameter of the pressure vessel (m)
%   sigma_y  - Yield strength of the material (Pa)
%   sf       - Safety factor (dimensionless)
%
% Output:
%   t        - Required wall thickness (m)

t = Pc*D*sf/(2*sigma_y);
end
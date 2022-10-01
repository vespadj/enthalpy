# script for python2 (v.2.7)

# Given 6 arguments:
#   Temperature outdoor in Celsius
#   Humidity outdoor in %
#   Pressure outdoor in Pa (or 0 to default)
#   Temperature indoor in Celsius
#   Humidity indoor in %
#   Pressure indoor in Pa (or 0 to default)
# Returns Enthalpies in J/mc : outdoot, indoor, difference, unit_of_measure

# e.g.:
# $ python2 enthalpy_core.py 28 30 0 25 80 0
# 53593 76176 -22583 J/mc


import sys

# pip install CoolProp -> ok
# pip3 install CoolProp >>> import CoolProp -> error
# so code is splitted in two files: first file for python3 and second file for python2
from CoolProp.HumidAirProp import HAPropsSI
# http://www.coolprop.org/fluid_properties/HumidAir.html#haprops-sample
# Enthalpy (J per kg dry air) as a function of temperature, pressure,
#    and relative humidity at dry bulb temperature T of 25C, pressure
#    P of one atmosphere, relative humidity R of 50%
# h = HAPropsSI('H','T',298.15,'P',101325,'R',0.5)


def calc(t_out, u_out, p_out, t_in, u_in, p_in):
    # Input Temperature in Celsius, Humidity in % (50%), pressure in Pa

    # if the pressure is not known, use 0, 
    # it will be converted to the default atmospheric pressure (101325 Pa)

    if p_out == 0:
        p_out = 101325
    if p_in == 0:
        p_in = 101325

    # Conversions: Temperature Celsius to Kelvin (273.15+x), humidity % to float (y*0.01)

    # Calculate Enthalpy (Hha) in J/kg
    # Hha J/kg humid air 	Input/Output 	Mixture enthalpy per humid air
    hha_out = HAPropsSI('Hha', 'T', 273.15+t_out, 'P', p_out, 'R', u_out*0.01)
    hha_in  = HAPropsSI('Hha', 'T', 273.15+t_in,  'P', p_in,  'R', u_in *0.01)

    # Calculate the Volume in cubic meters of 1 kg [mc/kg]
    vha_out = HAPropsSI('Vha', 'T', 273.15+t_out, 'P', p_out, 'R', u_out*0.01)
    vha_in  = HAPropsSI('Vha', 'T', 273.15+t_in,  'P', p_in,  'R', u_in *0.01)

    if vha_out != 0 and vha_in != 0:
        # Calculate Density rho = 1/Vha  [kg/mc]
        rho_out = 1 / vha_out
        rho_in =  1 / vha_in

        # When you change air, suppose the same volumes of air supplied and extracted (approx.),
        # so Calculate Enthalpy per mc [J/mc]:
        #   Enthalpy Hha is in J/kg, so multiply for Density:
        delta_H = str(int(round((hha_out * rho_out) - (hha_in * rho_in))))
        print("%s %s %s J/mc" % (str(int(hha_out * rho_out)), str(int(hha_in * rho_in)), delta_H))
    else:
        # Avoid division by zero errors.
        # I'm not sure if vha_out or vha_in maybe zero, probably never.
        # Enthalpy in J/kg
        delta_H = str(int(round(hha_out - hha_in)))
        print("%s %s %s J/kg" % (str(int(hha_out)), str(int(hha_in)), delta_H))
        
        # The End


# Entry point
if __name__ == "__main__":
    calc(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

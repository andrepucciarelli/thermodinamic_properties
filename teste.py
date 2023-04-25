import CoolProp.CoolProp as cp
from CoolProp.CoolProp import PropsSI
from CoolProp.CoolProp import FluidsList


fluid = 'water'
T = round(PropsSI('Phase', 'P', 100000, 'Q', 1, fluid), 8)

print(FluidsList())
print(T)
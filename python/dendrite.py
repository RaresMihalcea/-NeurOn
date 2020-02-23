import math
import cmath

class Dendrite:
    __membrane_capacitance = 1 #C
    __passive_membrane_unit_resistance = 2000 #R
    __specific_cytoplasmic_resistivity = 100 #Ra
    __inductance = 5 #L
    __resistance = 1000 * 1e-3 #r
    __constant_D = None
    __constant_tau = 1
    __scaled_length = None #Cursive L
    __stimulus = None #Omega
    __gamma_scaling = None
    __ra = None # Dendrite Resistance
    __g_pas = 0

    def __init__(self, n1, n2, diameter, length, data):
        self.__n1 = n1
        self.__n2 = n2
        self.__diameter = diameter
        self.__physical_length = length
        self.__assign_vars(data)
        self.__g_pas = 1/self.__passive_membrane_unit_resistance
        # print("gpas: {}".format(self.__g_pas))
        # print('R after scaling: {}'.format(self.__passive_membrane_unit_resistance))
        self.__calculate_tau()
        self.__calculate_ra()
        self.__calculate_d()

        # R scaling 
        # print('r: {}'.format(self.__resistance))

    ############### Internal Logic ###############

    def __assign_vars(self, data):
        self.__diameter = data['a']
        self.__membrane_capacitance = data['C']
        self.__passive_membrane_unit_resistance = data['R']
        self.__specific_cytoplasmic_resistivity = data['Ra']
        self.__inductance = data['L']
        self.__resistance = data['r']

    def __calculate_d(self):
        # self.__constant_D = (self.__diameter / (4 * self.__specific_cytoplasmic_resistivity * self.__membrane_capacitance))
        # lambda_aux = math.sqrt((1e4/4 * (self.__diameter / (self.__specific_cytoplasmic_resistivity * self.__membrane_capacitance))))
        lambda_aux = math.sqrt((1e4 * (self.__diameter / (4 * self.__specific_cytoplasmic_resistivity * self.__g_pas))))
        # lambda_aux = 1e4 * (self.__diameter / (4 * self.__specific_cytoplasmic_resistivity * self.__membrane_capacitance))

        # lambda_aux = math.sqrt(((1e4 / 4) * (self.__diameter / ( self.__specific_cytoplasmic_resistivity * self.__g_pas))))
        self.__constant_D = (lambda_aux ** 2) / self.__constant_tau
        # print("D: {}".format(self.__constant_D))
        return self.__constant_D

    def __calculate_tau(self):
        # scaling 
        # self.__constant_tau = self.__passive_membrane_unit_resistance * self.__membrane_capacitance
        self.__constant_tau = 1e-3 * (self.__membrane_capacitance / self.__g_pas)
        # self.__constant_tau = 1e-3 * (self.__g_pas / self.__membrane_capacitance) 
        # self.__constant_tau = self.__constant_tau * 1e-3
        # print("tau: {}".format(self.__constant_tau))
        return self.__constant_tau

    def __calculate_ra(self):
        self.__ra =  1e-7 *((4 * self.__specific_cytoplasmic_resistivity) / (math.pi * (self.__diameter ** 2)))
        # print("ra: {}".format(self.__ra))
        # print('diameter: {}'.format(self.__diameter))
        return self.__ra

    def __gamma(self, omega):
        result = (self.__resistance + omega * self.__inductance) 
        # print("step 1: {}".format(result))
        result = result * self.__membrane_capacitance 
        # print("step 2: {}".format(result))
        result = result ** -1
        # print("step 3: {}".format(result))
        result += omega + (self.__constant_tau ** -1)
        # print(omega)
        # print(self.__constant_tau)
        # print("step 4: {}".format(result))
        # print("step 4 omega: {}".format(omega))
        # print("step 4 tau: {}".format(self.__constant_tau ** -1))
        # print(self.__constant_D)
        result = result / self.__constant_D
        # print("step 5: {}".format(result))
        result = cmath.sqrt(result)
        self.__gamma_scaling = result
        # print("gamma: {}".format(self.__gamma_scaling))
        # print("gamma: {}".format(result))
        return result

    def __rescale(self, omega): 
        self.__scaled_length = self.__gamma(omega) * (self.__physical_length)
        return self.__scaled_length

    def stimulate(self, omega):
        self.__stimulus = omega
        self.__rescale(omega)
        
    ############### Print Dendrite Info ###############

    def to_string(self):
        dendrite_string = "Node 1 = {} \nNode 2 = {}".format(self.__n1, self.__n2)
        dendrite_string += "\nDiameter = {}".format(self.__diameter)
        dendrite_string += "\nPhysical Length = {}".format(self.__physical_length)

        if self.__stimulus is not None:
            dendrite_string += "\nScaled Length = {} under Stimulus = {}".format(self.__scaled_length, self.__stimulus)

        dendrite_string += "\nPassive Membrane Area Unit Resistance = {}".format(self.__passive_membrane_unit_resistance)
        dendrite_string += "\nInductance = {}".format(self.__inductance)
        dendrite_string += "\nResistance = {}".format(self.__resistance)
        return dendrite_string

    def to_compact_str(self):
        if self.__stimulus is not None:
            return "({}, {}, {})".format(self.__n1, self.__n2, self.__scaled_length)
        return "({}, {}, {})".format(self.__n1, self.__n2, self.__physical_length)
        
    ############### Getters ###############

    def get_first_node(self):
        return self.__n1

    def get_second_node(self):
        return self.__n2

    def get_membrane_capacitance(self):
        return self.__membrane_capacitance

    def get_passive_membrane_area_unit_resistance(self):
        return self.__passive_membrane_unit_resistance

    def get_inductance(self):
        return self.__inductance

    def get_resistance(self):
        return self.__resistance

    def get_constant_d(self):
        return self.__constant_D

    def get_constant_tau(self):
        return self.__constant_tau

    def get_diameter(self):
        return self.__diameter

    def get_ra(self):
        return self.__ra

    def get_gamma(self):
        return self.__gamma_scaling

    def get_scaled_length(self):
        if self.__stimulus is not None:
            return self.__scaled_length
        else:
            raise ValueError("Scaled length has not been calculated due to lack of stimulus.")

    def get_current_stimulus(self):
        if self.__stimulus is not None:
            return self.__stimulus
        else:
            raise ValueError("The dendrite has not yet been stimulated.")
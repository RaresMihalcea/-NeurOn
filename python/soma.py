import math

class Soma:
    __soma_diameter = 25 #d_soma
    __soma_membrane_capacitance = 1 #C_soma
    __soma_passive_membrane_unit_resistance = 2000 #R_soma
    __soma_resistance = 100 * 1e-3 #r_soma 
    __soma_inductance = 5 #L_soma
    __taus = None
    __Cs = None
    __Rs = 2000
    __Ls = 5
    __rs = 100 * 1e-3
    __stimulus = None
    __gamma_soma = None

    def __init__(self):
        super().__init__()
        self.__calculate_tau()
        self.__calculate_Cs()
        # self.__calculate_Rs()
        # self.__calculate_rs()
        # self.__calculate_Ls()
        # self.__Ls = self.__soma_inductance
        # print('res_s: {}'.format(self.__soma_resistance))

    def __calculate_tau(self):
        self.__taus = 1e-3 * self.__soma_membrane_capacitance * self.__soma_passive_membrane_unit_resistance
        # print("soma_tau: {}".format(self.__taus))
        return self.__taus

    def __calculate_Cs(self):
        self.__Cs = self.__soma_membrane_capacitance * math.pi * (self.__soma_diameter ** 2)
        # print("soma_C: {}".format(self.__Cs))
        return self.__Cs

    # def __calculate_Rs(self):
    #     self.__Rs = (self.__soma_passive_membrane_unit_resistance / (math.pi * (self.__soma_diameter ** 2)))
    #     print("soma_R: {}".format(self.__Rs))
    #     return self.__Rs
    
    # def __calculate_rs(self):
    #     self.__rs = (self.__soma_resistance / (math.pi * (self.__soma_diameter ** 2)))
    #     print("soma_rs: {}".format(self.__rs))
    #     return self.__rs

    # def __calculate_Ls(self):
    #     self.__Ls = (self.__soma_inductance / (math.pi * (self.__soma_diameter ** 2)))
    #     print("soma_L: {}".format(self.__Ls))
    #     return self.__Ls

    def __gamma_s(self, omega):
        # print('GAMMA S CS: {}'.format(self.__Cs))
        # print('GAMMA S TAUS: {}'.format(self.__taus))
        # print('GAMMA S DIAMETER: {}'.format(self.__soma_diameter))
        # print('GAMMA S LS: {}'.format(self.__Ls))
        # print('GAMMA S R: {}'.format(self.__rs))
        # __soma_diameter = 25 #d_soma
        # __soma_membrane_capacitance = 1 #C_soma
        # __soma_passive_membrane_unit_resistance = 2000 #R_soma
        # __soma_resistance = 100 * 1e-3 #r_soma 
        # __soma_inductance = 5 #L_soma
        result = self.__Cs * (omega + (1/self.__taus) + ((self.__soma_diameter ** 2) * math.pi) / ((self.__Cs * (self.__rs + (self.__Ls * omega)))))
        # result = self.__Cs * (omega + (1/self.__taus) + (1 / ((self.__Cs * (self.__rs + (5 * omega))))))
        # result = self.__Cs * (omega + (1/self.__taus) + (1/(self.__Cs * (self.__rs + (self.__Ls * omega)))))
        # print("gamma_s {}".format(result))
        self.__gamma_soma = result
        return result

    def stimulate(self, omega):
        self.__stimulus = omega
        self.__gamma_s(omega)

    def z(self):
        # print("target: {}".format(1.720721162863643e+03))
        result = (self.__Cs * self.__stimulus + (self.__Rs ** -1) + ((self.__rs + (self.__Ls * self.__stimulus)) ** -1))
        # print("z: {}".format(result))
        # result = (self.__Cs * self.__stimulus + (self.__soma_passive_membrane_unit_resistance ** -1) + ((self.__soma_resistance + (self.__soma_inductance * self.__stimulus)))  ** -1)
        # print('zs: {}'.format(result))
        return result
    
    def get_gamma_s(self):
        return self.__gamma_soma
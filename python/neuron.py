from dendrite import *
from soma import *
import numpy as np
import cmath
# from mpmath import *

# TODO: try storing results that are not dependent on omega
# http://mpmath.org/doc/current/calculus/inverselaplace.html
# TODO: LAMBDA THE TRIPS

class Neuron:

    ############### Init Logic ###############

    # Linear algebraic system equations variables
    __coefficients = [] #A
    __variables = None #x
    __results = {} #b
    __geometry = None
    __stimulus = None #omega

    __x = -1 #scaled measurement location
    __y = -1 #scaled stimulus location
    __X = -1 #measurement location
    __Y = -1 #stimulus location
    __x_branch = None
    __y_branch = None
    jy = None
    y_branch = None
    __soma = None

    __trips_coef = {}
    __dendrites = list()
    __trips_to_dendrites = {}
    __dendrites_set = {}

    def __init__(self, soma_index, geometry, stimulus, data):
        self.__soma_i = soma_index
        self.__geometry = geometry
        self.__empty_coef_vars()
        # print(format('*' * 10 + 'SOMA-INIT' + '*' * 10))
        # print(self.__coefficients)
        # print('OMEGA: {}'.format(stimulus))
        self.__soma = Soma(data)
        self.__soma.stimulate(stimulus)
        # print(format('*' * 30))
        # print()
        self.__init_dendrites()

    def __init_dendrites(self):
        self.__dendrites = []
        for i in range(len(self.__geometry)):
            for j in range(len(self.__geometry[i])):
                if isinstance(self.__geometry[i][j], Dendrite):
                    # print('YES')
                    self.__dendrites.append(self.__geometry[i][j])
        # print(self.__dendrites)
        self.__dendrites_set = set(self.__dendrites)
        # print(self.__dendrites_set)

    ############### Internal Logic ###############

    def stimulate(self, omega):
        self.__stimulus = omega
        self.__scale_branches(omega)
        self.__empty_coef_vars()
        self.__construct_trips()

    def __empty_coef_vars(self):
        self.__coefficients = []
        self.__trips_coef = {}
        self.__dendrites = list()
        self.__trips_to_dendrites = {}
        # self.__dendrites_set = {}

    def __scale_branches(self, omega):
        for i in self.__dendrites_set:
            i.stimulate(omega)
        # for i in range(len(self.__geometry)):
        #     for j in range(len(self.__geometry[i])):
        #         if isinstance(self.__geometry[i][j], Dendrite):
        #             self.__geometry[i][j].stimulate(omega)

    def __f(self, x):
        # print("f: {}".format(math.e ** ( -1 * math.fabs(x))))
        return (math.e ** ( -1 * math.fabs(x.real)))

    def __construct_trips(self):
        self.__trips_to_dendrites = {}
        self.__trips_coef = {}
        for i in range(len(self.__geometry)):
            for j in range(len(self.__geometry[i])):
                if isinstance(self.__geometry[i][j], Dendrite) and ((i, j) not in self.__trips_to_dendrites.keys()):
                    self.__trips_to_dendrites[(i, j)] = self.__geometry[i][j]

        for key in self.__trips_to_dendrites:
            d = {}
            self.__trips_coef[key] = {}
            for key_trip in self.__trips_to_dendrites:
                d[key_trip] = 0
            self.__trips_coef[key] = d.copy()
            
        for i in range(len(self.__geometry)):
            for j in range(len(self.__geometry[i])):
                if isinstance(self.__geometry[i][j], Dendrite):
                    self.__trips_coef[(i, j)][(i, j)] = -1 
                    if self.__is_terminal_node(i) and not self.__is_soma_node(i):
                        self.__trips_coef[(i, j)][(j, i)] = self.__determine_terminal_coefficient() * self.__f(self.__geometry[i][j].get_scaled_length())
                        # print('Terminal node detected. Coef: {}'.format(self.__trips_coef[(i, j)][(j, i)]))

                    elif self.__is_branching_node(i) and not self.__is_soma_node(i):
                        for k in range(len(self.__geometry[i])):
                            if isinstance(self.__geometry[i][k], Dendrite):
                                if j == k:
                                    self.__trips_coef[(i, j)][(k, i)] = self.__branching_coeffiecient(self.__geometry[i][k], True) * self.__f(self.__geometry[i][j].get_scaled_length())
                                else:
                                    self.__trips_coef[(i, j)][(k, i)] = self.__branching_coeffiecient(self.__geometry[i][k], False) * self.__f(self.__geometry[i][j].get_scaled_length())

                    elif self.__is_soma_node(i) and self.__is_terminal_node(i):
                        self.__trips_coef[(i, j)][(j, i)] = self.__soma_coefficient(self.__geometry[i][j], True) * self.__f(self.__geometry[i][j].get_scaled_length())
                        # print("Soma node detected. Coef: {}".format(self.__trips_coef[(i, j)][(j, i)]))

                    elif self.__is_soma_node(i) and self.__is_branching_node(i):
                        for k in range(len(self.__geometry[i])):
                            if isinstance(self.__geometry[i][k], Dendrite):
                                if j == k:
                                    self.__trips_coef[(i, j)][(k, i)] = self.__soma_coefficient(self.__geometry[i][k], True) * self.__f(self.__geometry[i][j].get_scaled_length())
                                else:
                                    self.__trips_coef[(i, j)][(k, i)] = self.__soma_coefficient(self.__geometry[i][k], False) * self.__f(self.__geometry[i][j].get_scaled_length())
                        
                    else:
                        raise ValueError("Unsupported node type")

        self.__trips_to_coef()
        self.__init_results()

    def __find_coefficient(self, node_index, dendrite):
        if self.__is_terminal_node(node_index) and not self.__is_soma_node(node_index):
            return self.__determine_terminal_coefficient()
        elif self.__is_branching_node(node_index) and not self.__is_soma_node(node_index):
            return self.__branching_coeffiecient(dendrite, True)
        else:
            # print('HEEYYYYYYYYYYYYY')
            return self.__soma_coefficient(dendrite, True)
            # return 1

    def __trips_to_coef(self):
        for key in self.__trips_to_dendrites:
            self.__coefficients.append(list(self.__trips_coef[key].values()))
        # for key in self.__trips_coef:
        #     print("{} -> {}".format(key, self.__trips_coef[key]))

    def __init_results(self):
        for key in self.__trips_to_dendrites:
            self.__results[key] = 0
        # print(self.__results)
        
    def __is_terminal_node(self, node_index):
        count = 0
        for j in range(len(self.__geometry[node_index])):
            if isinstance(self.__geometry[node_index][j], Dendrite):
                count += 1
        if count == 1:
            return True
        return False

    def __is_soma_node(self, node_index):
        return node_index == self.__soma_i

    def __is_branching_node(self, node_index):
        count = 0
        for j in range(len(self.__geometry[node_index])):
            if isinstance(self.__geometry[node_index][j], Dendrite):
                count += 1
                if count > 1:
                    return True
        return False

    def __determine_terminal_coefficient(self):
        return 1

    def set_input_location(self, Y, dendrite):
        self.__Y = Y
        self.__y_branch = dendrite
        self.__scale_input_location(self.__Y, dendrite)
        self.__jy()

    def __scale_input_location(self, Y, dendrite):
        self.__y = dendrite.get_gamma() * Y

    def __add_measurement_equations(self, x, dendrite):
        #TODO: add check for soma ask Yulia
        n1 = dendrite.get_first_node()
        n2 = dendrite.get_second_node()
        l = dendrite.get_scaled_length().real
        if x.real >= l / 2:
            #TODO need validation
            self.__results[(n1, n2)] -= (self.__f(l - x) * self.__find_coefficient(n2, dendrite))
            self.__results[(n2, n1)] -= (self.__f(x) * self.__find_coefficient(n1, dendrite))
            for i in range(len(self.__results)):
                if (n1, i) in self.__results and i is not n2:
                    self.__results[(n1, i)] -= (self.__f(x) * self.__find_coefficient(n2, dendrite))
            for i in range(len(self.__results)):
                if (n2, i) in self.__results and i is not n1:
                    self.__results[(n2, i)] -= (self.__f(l - x) * self.__find_coefficient(n1, dendrite))
            
        else:
            # self.__results[(n1, n2)] -= (self.__f(x) * self.__find_coefficient(n2, dendrite))
            # self.__results[(n2, n1)] -= (self.__f(l - x) * self.__find_coefficient(n1, dendrite))
            self.__results[(n1, n2)] -= (self.__f(x) * self.__find_coefficient(n1, dendrite))
            self.__results[(n2, n1)] -= (self.__f(l - x) * self.__find_coefficient(n2, dendrite))
            # self.__results[(n1, n2)] -= (self.__f(l - x) * self.__find_coefficient(n2, dendrite))
            # self.__results[(n2, n1)] -= (self.__f(x) * self.__find_coefficient(n1, dendrite))
            for i in range(len(self.__results)):
                if (n1, i) in self.__results and i is not n2:
                    self.__results[(n1, i)] -= (self.__f(l - x) * self.__find_coefficient(n2, dendrite))
            for i in range(len(self.__results)):
                if (n2, i) in self.__results and i is not n1:
                    self.__results[(n2, i)] -= (self.__f(x) * self.__find_coefficient(n1, dendrite))
        self.__solve_system()

    def __scale_measurement_location(self, X, dendrite):
        # print('X: {}'.format(X))
        # print('scale X gamma: {}'.format(dendrite.get_gamma()))
        self.__x = dendrite.get_gamma() * X

    def set_measurement_location(self, X, dendrite):
        self.__X = X
        self.__x_branch = dendrite
        self.__scale_measurement_location(self.__X, dendrite)
        self.__add_measurement_equations(self.__x, dendrite)   

    def __branching_coeffiecient(self, dendrite, reflection):
        result = self.__z__branching(dendrite)
        sum = 0
        for i in range(len(self.__dendrites)):
            sum += self.__z__branching(self.__dendrites[i])
        result = 2 * (result / sum)
        if reflection is True:
            result -= 1
        return result

    def __soma_coefficient(self, dendrite, reflection):#
        result = self.__z__branching(dendrite)
        # print('z: {}'.format(result))
        sum = self.__z_soma(dendrite)
        # print('gamma s: {}'.format(sum))
        ###############TODO: EXTRACT THIS CODE##########
        # print(self.__dendrites_set)
        for dendrite in self.__dendrites_set:
            sum += self.__z__branching(dendrite)
        ################################################
        # print("sum: {}".format(sum))
        # print('ps before division: {}'.format(result))
        # print('ps before division: {}'.format(result/sum))
        result = 2 * (result / sum)
        # result = 2*(result/sum)
        # result = 2* 0.077033110155887
        if reflection is True:
            result -= 1
        # Jv = (2pS − 1)[ f (2L − x) + f (x)]
        # 1 − (2pS − 1) f (2L)
        # , (24)
        # Jw = (2pS − 1) f (L + x) + f (L − x)
        # 1 − (2pS − 1) f (2L)
        # ,
        # print('X: {}'.format(self.__x))
        # print('jv: {}'.format((result*(self.__f(2*dendrite.get_scaled_length() - self.__x) + self.__f(self.__x))) / (1 - result * self.__f(2*dendrite.get_scaled_length()))))
        # print('jw: {}'.format((result * self.__f(dendrite.get_scaled_length() + self.__x) + self.__f(dendrite.get_scaled_length() - self.__x)) / (1 - result * self.__f(2*dendrite.get_scaled_length()))))


        # print('ps: {}'.format(result))
        return result

    def __z__branching(self, dendrite):
        return (dendrite.get_gamma() / dendrite.get_ra())

    def __z_soma(self, dendrite):
        # print('gamma s test =: {}'.format(self.__soma.get_gamma_s()))
        # print('z s test=: {}'.format(self.__soma.z()))
        # return 2.061670178918302e+04
        # return self.__soma.z()
        return self.__soma.get_gamma_s()
        # omega = dendrite.get_current_stimulus()
        # diameter = 25#dendrite.get_diameter() ** 2
        # cs = 1#dendrite.get_membrane_capacitance() * math.pi * diameter
        # prs = 2000#dendrite.get_passive_membrane_area_unit_resistance() / (math.pi * diameter)
        # rs = 100#dendrite.get_resistance() / (math.pi * diameter) 
        # l = 5#dendrite.get_inductance() / (math.pi * diameter)
        # return (cs * omega + (prs ** -1) + ((rs + (l * omega)) ** -1))

    def __solve_system(self):
        #TODO: ASK YULIA
        # print('\n')
        # print(self.__coefficients)
        # print("result {}".format(self.__results))
        results = list(self.__results.values())
        results = np.linalg.solve(self.__coefficients, results)
        i = 0
        for key in self.__results:
            # print(key)
            self.__results[key] = results[i]
            i += 1
        # print(results)
        # print(self.__results)
        # print('\n')

        # print(self.__results)
        # self.__coefficients.append(list(self.__results))
        # print(self.__coefficients)
        # self.__coefficients = [[3, -2], [6, -4]]
        # print(np.linalg.solve(self.__coefficients, [0, 0]))
        # coef = Matrix(self.__coefficients)
        # print(coef.nullspace())

    def __jy(self):
        n1 = self.__y_branch.get_first_node()
        # print(n1)
        n2 = self.__y_branch.get_second_node()
        # print(n2)
        # print(self.__results)
        l = self.__y_branch.get_scaled_length()
        if self.__x_branch == self.__y_branch:
            self.jy = self.__f(self.__y) * self.__results[(n1, n2)]
            # print(self.__f(self.__y) * self.__results[(n1, n2)])
            # print('here')
            # print(self.__results[(n1, n2)])
            # print(self.__results[(n2, n1)])
            self.jy += self.__f(l - self.__y) * self.__results[(n2, n1)]
            # print(self.__f(l - self.__y) * self.__results[(n2, n1)])
            self.jy += self.__f(self.__x - self.__y)
            # self.jy /= math.pi ** 2
            # self.jy /= 2
            # print(self.__f(self.__x - self.__y))
            # self.jy = self.jy * 3e-1
            # print(self.__f(0))
            # print('target: {}'.format(0.1632833667711))
            # print('jy: {}'.format(self.jy))
        else:
            self.jy = self.__f(self.__y) * self.__results[(n1, n2)]
            self.jy += self.__f(l - self.__y) * self.__results[(n2, n1)]      

    def greens_function(self):
        self.y_branch = self.__y_branch
        # print(self.jy / ((2 * self.__y_branch.get_constant_d()) * self.__y_branch.get_gamma()))
        # print("final : {}".format((self.jy / ((2 * self.__y_branch.get_constant_d()) * self.__y_branch.get_gamma())))) 
        # print("final w zs: {}".format((self.jy / ((2 * self.__y_branch.get_constant_d()) * self.__soma.z()))))
        # print("final w omegas: {}".format((self.jy / ((2 * self.__y_branch.get_constant_d()) * 2.061670178918302e+4))))
        # print("final w omegas hardcoded: {}".format(((0.1632833667711 / ((2 * 5.000000000000001e+04) * 0.005477225575052)))))
        # return self.__soma.get_gamma_s()
        return (self.jy / ((2 * self.__y_branch.get_constant_d()) * self.__y_branch.get_gamma()))

    ############### Print Neuron Info ###############

    def to_string(self):
        result = "Neuron somma index: {}".format(self.__soma_i)
        result += "\nGeometry:\n"

        for i in range(len(self.__geometry)):
            for j in range(len(self.__geometry[i])):
                if isinstance(self.__geometry[i][j], Dendrite):
                    result += self.__geometry[i][j].to_compact_str() + " "
                else:
                    result += str(self.__geometry[i][j]) + " "
            result += "\n"

        return result    

    ############### Getters ###############

    def get_soma_index(self):
        return self.__soma_i

    def get_geometry(self):
        return self.__geometry

    def get_system_coeficients(self):
        return self.__coefficients

    def get_system_variables(self):
        return self.__variables
    
    def get_system_results(self):
        return self.__results
    
    def get_stimulus(self):
        return self.__stimulus

    def get_dendrites(self):
        return self.__dendrites
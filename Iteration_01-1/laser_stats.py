from cmath import log
import numpy as np
import warnings
import random
import math
import sys
import time
warnings.simplefilter("ignore", np.ComplexWarning)
class photon:
    def __init__(self, id, wavelength, probability, encoding_alpha, encoding_beta):
        self.id = id
        self.wavelength = wavelength
        self.probability = probability
        self.encoding_alpha = encoding_alpha
        self.encoding_beta = encoding_beta

class node:
    def __init__(self, id):
        self.id = id
    def receive(node, photon):
        #print("Photon received at Node " + str(node.id))
        #print("Photon probability: " + str(photon.probability))
        pass
    def emit(node1, node2, photon, fiber, platform):
        #print("Photon emitted from Node " + str(node1.id))
        #print("Photon probability: " + str(photon.probability))
        optical_fiber.transmit(fiber, photon, node2, platform)

#operation range: 775 nm to 1775 nm
lines = 10001
alpha_file = open("Iteration_01-1/data/SiO2_alpha_vs_lambda.csv")
alpha_data = np.empty(shape = (lines, 2))
for i in range(0, lines):
    str1, str2 = (alpha_file.readline()).strip().split("  ")
    alpha_data[i,0] = float(str1.strip())
    alpha_data[i,1] = float(str2.strip()) #* 0.20 / 0.18441225017619317
alpha_file.close()
platforms = 6
platform_file = open("Iteration_01-1/data/QR_platform_parameters_current.csv")
platform_names = []
platform_data = np.empty(shape = (platforms, 3))
for i in range(0, platforms):
    str0, str1, str2, str3 = (platform_file.readline()).strip().split("  ")
    platform_names.append(str0.strip())
    platform_data[i,0] = float(str1.strip()) / 100.0
    platform_data[i,1] = float(str2.strip())
    platform_data[i,2] = float(str3.strip())
platform_file.close()
def lc_eff(platform):
    for i in range(0, platforms):
        if (platform == platform_names[i]):
            return platform_data[i,0]
class optical_fiber:
    def __init__(self, id, length):
        self.id = id
        self.length = length
    def transmit(fiber, photon, node, platform):
        alpha = 10.0
        if (photon.wavelength <= alpha_data[0, 0]):
            alpha = alpha_data[0, 1] + (photon.wavelength - alpha_data[0, 0]) * (alpha_data[1, 1] - alpha_data[0, 1]) / (alpha_data[1, 0] - alpha_data[0, 0])
        elif (photon.wavelength >= alpha_data[lines -1, 0]):
            alpha = alpha_data[0, 1] + (photon.wavelength - alpha_data[0, 0]) * (alpha_data[lines -1, 1] - alpha_data[lines - 1, 1]) / (alpha_data[lines -1, 0] - alpha_data[lines - 1, 0])
        else:
            alpha = alpha_data[int(10 * (photon.wavelength - alpha_data[0, 0])), 1]
        l_att = 10.0 / (alpha * log(10))
        dampening = 10 ** (-0.1 * alpha * fiber.length)
        lc_efficiency = lc_eff(platform)
        photon.probability *= dampening * lc_efficiency
        node.receive(photon)

def factorial(n):
    factorial = 1
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        for i in range(1,n + 1):
            factorial = factorial*i
        return factorial
def probability_of_photons(n, meu):
    return ((pow(meu, n))*(math.exp(-1 * meu))/(factorial(n)))
def number_of_photons(meu):
    n = random.random()
    ll = 0
    i = 0
    while True:
        if (ll <= n and n <= ll + probability_of_photons(i, meu)):
            return i
            break
        else:
            ll = ll + probability_of_photons(i, meu)
        i = i + 1
def rand_key(p):
    key1 = ""
    for i in range(p):
        temp = str(random.randint(0, 1))
        key1 += temp
    return(key1)
def rand_basis(p):
    key1 = ""
    for i in range(p):
        temp = str(0 if (random.random() <= 0.9) else 1)
        key1 += temp
    return(key1)
def rand_signal(prob):
    return(str(0 if (random.random() <= prob) else 1))
def measure(encoding_alpha, encoding_beta, basis):
    if basis == '0':
        n = random.random()
        if n <= pow(encoding_alpha, 2):
            return '0'
        else:
            return '1'
    else:
        n = random.random()
        if n <= pow((encoding_alpha + encoding_beta)/(math.sqrt(2)), 2):
            return '0'
        else:
            return '1'
signal_mean_photon_number = 0.06
decoy_mean_photon_number = 0.03

number_of_photons_emitted = np.array([0, 0, 0, 0, 0, 0, 0, 0])
n  = 1000000
for i in range(n):
    number_of_photons_emitted[number_of_photons(signal_mean_photon_number if (rand_signal(0.6) == '0') else decoy_mean_photon_number)] += 1

for i in range(8):
    print(number_of_photons_emitted[i]/n)
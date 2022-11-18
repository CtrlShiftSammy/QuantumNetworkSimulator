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
alpha_file = open("Iteration_03/data/SiO2_alpha_vs_lambda.csv")
alpha_data = np.empty(shape = (lines, 2))
for i in range(0, lines):
    str1, str2 = (alpha_file.readline()).strip().split("  ")
    alpha_data[i,0] = float(str1.strip())
    alpha_data[i,1] = float(str2.strip()) #* 0.20 / 0.18441225017619317
alpha_file.close()
platforms = 6
platform_file = open("Iteration_03/data/QR_platform_parameters_current.csv")
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
        dampening = 10 ** (-0.1 * 0.17 * fiber.length)
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
        temp = str(0 if (random.random() <= 0.5) else 1)
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
pulse_rate = 2500000000
number_of_bits = 2500000
#length = 251.7
#length = 302.1
length = 354.5
#length = 404.9
#length = 421.1

signal_mean_photon_number = 0.35
decoy_mean_photon_number = 0.15
block_size = 6144000
alice_station_key = ""
alice_station_basis = ""
bob_station_raw_key = ""
bob_station_detected = ""
bob_station_basis = ""
alice_station_secret_key = ""
bob_station_secret_key = ""

start = time.time()
print("")
for i in range(number_of_bits):
    #each pulse
    alice_station_key += rand_key(1)
    alice_station_basis += rand_basis(1)    
    if (i%100 == 0):
        end = time.time()
        print ("\033[A                                                      \033[A")
        print(str(i*100/number_of_bits) + " % completed; ETA: " + str(int(((end - start) * (number_of_bits - i - 1) / (i + 1)) / 60)) + " minutes "  + str(int(((end - start) * (number_of_bits - i - 1) / (i + 1)) % 60)) + " seconds. ")
    
    if alice_station_basis[i] == '0':
        if alice_station_key[i] == '0':
            encoding_alpha = 1
            encoding_beta = 0
        else:
            encoding_alpha = 0
            encoding_beta = 1
    else:
        encoding_alpha = 1/math.sqrt(2)
        encoding_beta = 1/math.sqrt(2)
    number_of_photons_emitted = number_of_photons(signal_mean_photon_number if (rand_signal(0.6) == '0') else decoy_mean_photon_number)
    number_of_photons_detected = 0
    n_bsm = rand_basis(1)
    for j in range(number_of_photons_emitted):
        #each photon
        photon_j = photon(1, 1550, 1, encoding_alpha, encoding_beta) #id, wavelength in nm, probability, alpha, beta
        node_1 = node(1)
        node_2 = node(2)
        fiber_1 = optical_fiber(1, length) #id, length in km
        node.emit(node_1, node_2, photon_j, fiber_1, "Custom")
        if (random.random() <= photon_j.probability): #if detected
            if number_of_photons_detected == 0: #first photon
                bob_station_basis += str(n_bsm)
                bob_station_raw_key += measure(photon_j.encoding_alpha, photon_j.encoding_beta, n_bsm)
            number_of_photons_detected = number_of_photons_detected + 1
    bob_station_detected += str(number_of_photons_detected)
ii = 0
for i in range(number_of_bits):
    if bob_station_detected[i] != '0':
        if (bob_station_basis[ii] == '0' and alice_station_basis[i] == '0'):
            alice_station_secret_key += alice_station_key[i]
            bob_station_secret_key += bob_station_raw_key[ii]
        ii += 1
print(alice_station_secret_key)
print(bob_station_secret_key)
print("RKR: " + str(len(bob_station_basis) * pulse_rate / number_of_bits) + " bps")
print("SKR: " + str(len(bob_station_secret_key) * pulse_rate / number_of_bits) + " bps")
print(str(alice_station_secret_key == bob_station_secret_key))
print("Block time: " + str(block_size / (3600 * len(bob_station_basis) * pulse_rate / number_of_bits)) + " h")

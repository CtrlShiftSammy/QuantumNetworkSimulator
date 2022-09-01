from cmath import log
import numpy as np
import warnings
warnings.simplefilter("ignore", np.ComplexWarning)
class photon:
    def __init__(self, id, wavelength, probability):
        self.id = id
        self.wavelength = wavelength
        self.probability = probability

class node:
    def __init__(self, id):
        self.id = id
    def receive(node, photon):
        print("Photon received at Node " + str(node.id))
        print("Photon probability: " + str(photon.probability))
    def emit(node1, node2, photon, fiber, platform):
        print("Photon emitted from Node " + str(node1.id))
        print("Photon probability: " + str(photon.probability))
        optical_fiber.transmit(fiber, photon, node2, platform)

#operation range: 775 nm to 1775 nm
lines = 10001
alpha_file = open("data/SiO2_alpha_vs_lambda.csv")
alpha_data = np.empty(shape = (lines, 2))
for i in range(0, lines):
    str1, str2 = (alpha_file.readline()).strip().split("  ")
    alpha_data[i,0] = float(str1.strip())
    alpha_data[i,1] = float(str2.strip())
alpha_file.close()
platforms = 5
platform_file = open("data/QR_platform_parameters_current.csv")
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
        print("Photon transmitted through Fiber " + str(fiber.id) + " of length " + str(fiber.length) + " km")
        print("Alpha = " + str(alpha) + " dB/km")
        print("Attenuation = " + str(alpha * fiber.length) + " dB")
        print("Attenuation length = " + str(float(l_att)) + " km")
        print("Transmission probability = " + str(100 * dampening) + " %")        
        print("Link Coupling Efficiency = " + str(100 * lc_efficiency) + " %")        
        node.receive(photon)

photon_1 = photon(1, 1551, 1) #id, wavelength in nm, probability
node_1 = node(1)
node_2 = node(2)
fiber_1 = optical_fiber(1, 421.1) #id, length in kmm

node.emit(node_1, node_2, photon_1, fiber_1, "Q_dots")
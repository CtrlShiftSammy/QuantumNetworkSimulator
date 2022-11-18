import math
leff = 0.25
dist = 251.7
att = 10 ** (-0.17 * dist / 10)
meu1 = 0.49
meu2 = 0.18
eta = att * leff
print(att)
print(leff)
print(eta)
sum1 = 0
sum2 = 0
n = 0
#for n in range(100):
    #sum1 = sum1 + (meu1 ** n) * math.exp(-1 * meu1) * (1 - (1 - eta) ** n) / math.factorial(n)
    #sum2 = sum2 + (meu2 ** n) * math.exp(-1 * meu2) * (1 - (1 - eta) ** n) / math.factorial(n)
sum1 = 1 - math.exp(-1 * eta * meu1)
sum2 = 1 - math.exp(-1 * eta * meu2)

print((0.6*sum1 + 0.4*sum2) * 2.5 * 10**9)
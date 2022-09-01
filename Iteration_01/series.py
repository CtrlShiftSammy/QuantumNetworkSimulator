import math
leff = 0.032
dist = 101.6
att = 10 ** (-0.2 * dist / 10)
meu1 = 0.06
meu2 = 0.03
eta = att * leff
print(att)
print(leff)
print(eta)
sum1 = 0
sum2 = 0
n = 0
for n in range(100):
    sum1 = sum1 + (meu1 ** n) * math.exp(-1 * meu1) * (1 - (1 - eta) ** n) / math.factorial(n)
    sum2 = sum2 + (meu2 ** n) * math.exp(-1 * meu2) * (1 - (1 - eta) ** n) / math.factorial(n)
print((0.6*sum1 + 0.4*sum2) * 2.5 * 10**9)
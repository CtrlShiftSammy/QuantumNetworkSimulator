import numpy as np
import scipy as sp
import scipy.linalg
import math
import random

Zero = np.array([[1.0],
                 [0.0]])
One = np.array([[0.0],
                [1.0]])
NormalizeState = lambda state: state / sp.linalg.norm(state)

Plus = NormalizeState(Zero + One)

Hadamard = 1./np.sqrt(2) * np.array([[1, 1],
                                     [1, -1]])

NewState = np.dot(Hadamard, Zero)

ZeroZero = np.kron(Zero, Zero)
OneOne = np.kron(One, One)
PlusPlus = np.kron(Plus, Plus)

CatState = NormalizeState(ZeroZero + OneOne)

def NKron(*args):
  result = np.array([[1.0]])
  for op in args:
    result = np.kron(result, op)
  return result

FiveQubitState = NKron(One, Zero, One, Zero, One)   

Id = np.eye(2)
HadamardZeroOnFive = NKron(Hadamard, Id, Id, Id, Id)
NewState = np.dot(HadamardZeroOnFive, FiveQubitState)

P0 = np.dot(Zero, Zero.T)
P1 = np.dot(One, One.T)
X = np.array([[0,1],
              [1,0]])

CNOT03 = NKron(P0, Id, Id, Id, Id) + NKron(P1, Id, Id, X, Id)
NewState = np.dot(CNOT03, FiveQubitState)

import numpy.random

CatState = NormalizeState(ZeroZero + OneOne)
RhoCatState = np.dot(CatState, CatState.T)

#Find probability of measuring 0 on qubit 0
Prob0 = np.trace(np.dot(NKron(P0, Id), RhoCatState))

#Simulate measurement of qubit 0
if (np.random.rand() < Prob0):
    #Measured 0 on Qubit 0
    Result = 0
    ResultState = NormalizeState(np.dot(NKron(P0, Id), CatState))
else:
    #Measured 1 on Qubit 1
    Result = 1
    ResultState = NormalizeState(np.dot(NKron(P1, Id), CatState))

#print("Qubit 0 Measurement Result: {}".format(Result))
#print("Post-Measurement State:")
#print(ResultState)

def LeakAndMeasure(State):
    State[0][0] = 0
    State = NormalizeState(State)
    return(State)

def MeasureAtPosition(State, Position):
    #print(State)
    TwoPowerN = np.shape(State)[0]
    N = math.log(TwoPowerN) / math.log(2)
    alpha = 0
    for i in range(TwoPowerN):
      Bin = Binary(i, N)
      if (Bin[Position] == '0'):
        alpha = alpha + math.pow(State[i], 2)
    print(alpha)    
    if (random.random() <= alpha):
      toss = '0'
    else:
      toss = '1'
    for i in range(TwoPowerN):
      Bin = Binary(i, N)
      if (Bin[Position] != toss):
        State[i] = 0.0
    State = NormalizeState(State)
    return(State)

def Binary(i, N):
      Bin = format(i, 'b')
      for j in range(int(N)):
        if len(Bin) < N:
          Bin = '0' + Bin
      return(Bin)

def PrintQuantumState(State):
  PlusSign = False
  TwoPowerN = np.shape(State)[0]
  N = math.log(TwoPowerN) / math.log(2)
  for i in range(TwoPowerN):
    
    if State[i] != 0.0:
      Bin = Binary(i, N)
      if PlusSign:
        print(" + (", State[i], ")     |", Bin, ">")
      else:
        print("   (", State[i], ")     |", Bin, ">")
        PlusSign = True

State1 = NormalizeState(Zero + One)
State2 = NormalizeState(Zero + One)

State = np.kron(State1, State2)
State = LeakAndMeasure(State)

NOT12 = np.kron(X, X)
State = np.dot(NOT12, State)
State = LeakAndMeasure(State)
#print(State)
State = np.dot(np.kron(Id, X), State)
#print(State)

StateA = NormalizeState(Zero)
StateB = NormalizeState(Zero)
State = np.kron(np.kron(StateA, State), StateB)
print("Net State:")
print(State)

HIIH = np.kron(np.kron(Hadamard, Id), np.kron(Id, Hadamard))
State = np.dot(HIIH, State)
print(State)

CNOT12 = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]])
CNOT21 = np.array([[1, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0]])
CNOT1221 = np.kron(CNOT12, CNOT21)
State = np.dot(CNOT1221, State)

print("Final State:")
print(State)
State = MeasureAtPosition(State, 1)
State = MeasureAtPosition(State, 2)
print("Entangled state produced after measurement:")
print(State)
PrintQuantumState(State)
TwoPowerN = np.shape(State)[0]
N = math.log(TwoPowerN) / math.log(2)
OddParity = ((int(Binary(np.nonzero(State)[0][0], N)[1]) + int(Binary(np.nonzero(State)[0][0], N)[2])) % 2 == 1)

IIIX = np.kron(np.kron(Id, Id), np.kron(Id, X))
if OddParity:
  State = np.dot(IIIX, State)
PrintQuantumState(State)
print("EPR Pair 00 established using link level communication.")


import numpy as np
import scipy as sp
import scipy.linalg

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

print("Qubit 0 Measurement Result: {}".format(Result))
print("Post-Measurement State:")
print(ResultState)

def LeakAndMeasure(State):
    State[0][0] = 0
    State = NormalizeState(State)
    return(State)

State1 = NormalizeState(Zero + One)
State2 = NormalizeState(Zero + One)

State = np.kron(State1, State2)
State = LeakAndMeasure(State)
print(State)

NOT12 = np.kron(X, X)
State = np.dot(NOT12, State)
State = LeakAndMeasure(State)
print(State)

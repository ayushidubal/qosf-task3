#!/usr/bin/env python
# coding: utf-8

# # Task 3
# 
# The question given was:
# 
# Please write a simple compiler – program, which translates one quantum circuit into another, using a restricted set of gates.
# 
# You need to consider just the basic gates for the input circuit, such as (I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ).
# 
# The output circuit should consist only from the following gates: RX, RZ, CZ. In other words, each gate in the original circuit must be replaced by an equivalent combination of gates coming from the restricted set (RX, RZ, CZ) only.
# 
# For example, a Hadamard gate after compilation looks like this:
# 
# RZ(pi/2)
# RX(pi/2)
# RZ(pi/2)
# 
# Analyze what’s the overhead of the compiled program compared to the original one and propose how to improve it. What we mean by overhead is the following: by replacing all the initial gates with the restricted set of gates given in the problem, you will see that the resulting circuit is much more involved than the original one. This is what we called the overhead, and you may think about how to treat this problem, i.e. you could try to simplify as much as possible the resulting circuit.
# 
# ***
# 
# I interpreted this question as essentially implementing a transpiler, with a different set of basis gates. My final output was a lot more efficient than the transpiler in terms of overhead generated.
# I approached this question by expressing the given gates in terms of rx, rz and cz.
# After that, I parsed the input circuit and built a new circuit which replaced each gate in the input circuit with its transformation in our new basis and returned the new ciruit and the overhead generated.
# 
# The question taught me a lot about how optimization is performed in qiskit. 
# 
# This is how I think my code can be improved:
# - check for unitaries and reduce the number of gates
# - possible reordering and reduction by finding unitaries
# 
# In my opinion, the transpiler gives a more expensive circuit as it has been coded for a much more general case, unlike my code, which has been hardcoded for a few select input gates.

# In[96]:


#importing required libraries

from qiskit import QuantumCircuit, Aer
from qiskit.compiler import transpile
from qiskit.visualization import *

import math
from math import pi


# In[97]:


#each of these functions replaces the given gate with a combination of rx, rz and cz, and then returns the overhead increase

def convertid(qc,i):
    return 0

def converth(qc,i):
    qc.rz(0.5*pi,i)
    qc.rx(0.5*pi,i)
    qc.rz(0.5*pi,i)
    return 2

def convertx(qc,i):
    qc.rx(pi,i)
    return 0

def converty(qc,i):
    qc.rx(pi,i)
    qc.rz(pi,i)
    return 1

def convertz(qc,i):
    qc.rz(pi,i)
    return 0
    
def convertrx(qc,i,theta):
    qc.rx(theta,i)
    return 0

def convertry(qc,i,theta):
    qc.rz(0.5*pi,i)
    qc.rx(theta,i)
    qc.rz((-0.5)*pi,i)
    return 2

def convertrz(qc,i,theta):
    qc.rz(theta,i)
    return 0

def convertcz(qc,cq,tq):
    qc.cz(cq,tq)
    return 0


# In[98]:


#replaces each gate in the input circuit by the transformation and returns the new circuit and the overhead generated

def transform(qc_ip, n):
    
    overhead = 0
    
    qc_op = QuantumCircuit(n)
    
    for i in qc_ip.data:
        if i[0].name == 'id':
            overhead += convertid(qc_op, i[1][0].index)
        
        elif i[0].name == 'h':
            overhead += converth(qc_op, i[1][0].index)
        
        elif i[0].name == 'x':
            overhead += convertx(qc_op, i[1][0].index)
        
        elif i[0].name == 'y':
            overhead += converty(qc_op, i[1][0].index)
            
        elif i[0].name == 'z':
            overhead += convertz(qc_op, i[1][0].index)
        
        elif i[0].name == 'rx':
            overhead += convertrx(qc_op, i[1][0].index, i[0].params[0])
            
        elif i[0].name == 'ry':
            overhead += convertry(qc_op, i[1][0].index, i[0].params[0])
                
        elif i[0].name == 'rz':
            overhead += convertrz(qc_op, i[1][0].index, i[0].params[0])    
            
        elif i[0].name == 'cz':
            overhead += convertcz(qc_op, i[1][0].index, i[1][1].index)
        
        else:
            print("Gate cannot be processed")
            return
        
    return (qc_op, overhead)


# In[118]:


#testing for a specific case

qc = QuantumCircuit(3)
qc.h(0)
qc.ry(pi/3.0,2)
qc.x(1)
qc.cz(0,1)

print("This is the original circuit:")
print(qc)


# In[120]:


qc_new, overhead = transform(qc, 3)

print("This is the new circuit:")
print(qc_new)

print("Overhead :", overhead)


# In[121]:


qc_transpiled = transpile(qc, basis_gates = ['rx', 'rz', 'cz'])
print("This is the transpiled circuit:")
print(qc_transpiled)



# --------------------------------------------------------------------------------------------------
# This Script Provides An Application Example Of The Generalized Likelihood Uncertainty Estimation (GLUE) Method.
# This Script Prepared By Pooya Shirazi.
# Ferdowsi University of Mashhad, 2019.
# Email: p.shirazi.a@gmail.com
# --------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import scipy.stats as scs
import pyDOE

# Requaired Functions: -----------------------------------------------------------------------------

def sampleGenerator(SampStrategy, M, DistrFun, xmin, xmax, N):
    
    """
    
    Generates a Sample X Composed of N Random Samples of M Uncorrelated variables.
    
    Usage:
    X = sampleGenerator(SampStrategy, M, DistrFun, xmin, xmax, N)
    
    Input:
    SampStrategy = Sampling Strategy                                               - string
                   Options: 'rsu' : Random Uniform
                            'lhs' : Latin Hypercube
               M = Number of Variables                                             - scalar
        DistrFun = Probability Distribution Function of each Variable              - string
                   Options: 'uniform' (if all variables have the same PDF)
            xmin = Minimum Parameter Ranges Values of the PDF                      - list
            xmax = Maximum Parameter Ranges Values of the PDF                      - list
               N = Number of Samples                                               - scalar
    
    Output:
    X = Matrix of Samples                                                          - matrix (N,M)
        Each Row is a Point in the Input Space.
    
    Examples:
    # Example 1:
    SampStrategy = 'lhs'
    M = 3
    DistrFun = 'uniform'
    xmin = [0.1, 0.2, 0.3]
    xmax = [0.2, 0.4, 0.6]
    N = 3000
    X = sampleGenerator(SampStrategy, M, DistrFun, xmin, xmax, N)
    
    """
    
    # Check Inputs: --------------------------------------------------------------------------------
    
    # TODO: write code ...
    
    # Uniformly Sample The Unit Square: ------------------------------------------------------------
    
    if SampStrategy == 'rsu':
        X = np.random.rand(N,M)         # Uniform Sampling
    elif SampStrategy == 'lhs':
        X = pyDOE.lhs(n=M, samples=N)   # Latin Hypercube Sampling
    else:
        print("ERROR")
    
    # Map Back Into The Specified Distribution By Inverting The CDF: -------------------------------
    
    for i in range(M):
        if DistrFun == 'uniform':
            X[:,i] = scs.uniform.ppf(q=X[:,i], loc=xmin[i], scale=xmax[i] - xmin[i])
        else:
            print("ERROR")
    
    # Return Value: --------------------------------------------------------------------------------
    return X


# Experiment Setup: --------------------------------------------------------------------------------

M = 3                   # Number Of Uncertain Parameters [a, b, c].
DistrFun = 'uniform'    # Parameter Distribution.
xmin = [0.1, 0.2, 0.3]  # Minimum Parameter Ranges Values [a, b, c].
xmax = [0.2, 0.4, 0.6]  # Maximum Parameter Ranges Values [a, b, c].

# Sampling Input Space: ----------------------------------------------------------------------------

SampStrategy = 'lhs'     # Sampling Strategy (Other Options Is 'rsu')
N = 3000                 # Sample Size

# Perform Sampling:

X = sampleGenerator(SampStrategy, M, DistrFun, xmin, xmax, N)

# Model Evaluation: --------------------------------------------------------------------------------







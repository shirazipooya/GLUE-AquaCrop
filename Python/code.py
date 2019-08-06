
# --------------------------------------------------------------------------------------------------
# This Script Provides An Application Example Of The Generalized Likelihood Uncertainty Estimation (GLUE) Method.
# This Script Prepared By Pooya Shirazi.
# Ferdowsi University of Mashhad, 2019.
# Email: p.shirazi.a@gmail.com
# --------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import scipy.stats as scs
import os
import pyDOE
import time

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

def findLine(pathFile, lookup):
    
    '''
    Find Specific Line in File.
    
    Usage:
    X = findLine(pathFile, lookup)
    
    Input:
    pathFile = Location of Crop File                                   - string
      lookup = Lookup Your Parameter in Crop File                      - string
    
    Output:
    X = Line Number of Parameter                                       - scalar

    Examples:
    pathFile = 'C:/User/Pooya/Desktop/data.dat'
      lookup = 'Parameter Crop'
    X = findLine(pathFile, lookup)  
    '''
    
    with open(file=pathFile, mode='r') as myFile:
        for lineNumber, lineValue in enumerate(iterable=myFile, start=0):
            if lookup in lineValue:
                return lineNumber

def createNewLine(pathFile, lineNumber, newValue):
    
    '''
    Create New Line.
        
    Usage:
    X = createNewLine(pathFile, lineNumber, newValue)
    
    Input:
      pathFile = Location of Crop File                                   - string
    lineNumber = Line Number of Parameter                                - scalar
      newValue = Parameter New Value                                     - scalar
    
    Output:
    X = String of New Line                                               - string

    Examples:
      pathFile = 'C:/User/Pooya/Desktop/data.dat'
    lineNumber = 3
      newValue = 2.5
    X = createNewLine(pathFile, lineNumber, newValue)
    '''
    
    lines = open(file=pathFile, mode='r').readlines()
    oldLine = lines[lineNumber]
    newLine = str(newValue) + " " * (15-len(str(newValue))) + oldLine[oldLine.find(":"):]
    return newLine

def replaceLine(pathFile, lineNumber, newLine):
    
    '''
    Replace New Line into File.
    
    Usage:
    X = replaceLine(pathFile, lineNumber, newLine)
    
    Input:
      pathFile = Location of Crop File                                   - string
    lineNumber = Line Number of Parameter                                - scalar
      newLine  = String of New Line                                      - string
    
    Output:
    X = Write in File                                                    - string

    Examples:
      pathFile = 'C:/User/Pooya/Desktop/data.dat'
    lineNumber = 3
      newValue = 'Pooya'
    replaceLine(pathFile, lineNumber, newLine)
    '''
    
    lines = open(file=pathFile, mode='r').readlines()
    lines[lineNumber] = newLine
    out = open(file=pathFile, mode='w')
    out.writelines(lines)
    out.close()

def runACsaV60(pathFile):
    
    '''
    Run AquaCrop.
    
    Usage:
    X = runACsaV60(pathFile)
    
    Input:
    pathFile = Location of AquaCrop Program                              - string
    
    Output:
    X = Run AquaCrop

    Examples:
    pathFile = 'C:/User/Pooya/Desktop/AquaCrop.exe'
    runACsaV60(pathFile)
    '''
    
    os.startfile(filepath=pathFile)

# Experiment Setup: --------------------------------------------------------------------------------

M = 3                   # Number Of Uncertain Parameters [CCx, CDC, CGC].
paraName = ['Maximum canopy cover (CCx)', 'Canopy decline coefficient (CDC)', 'Canopy growth coefficient (CGC)']
DistrFun = 'uniform'    # Parameter Distribution.
xmin = [0.800, 0.003, 0.005]  # Minimum Parameter Ranges Values [CCx, CDC, CGC].
xmax = [0.990, 0.005, 0.007]  # Maximum Parameter Ranges Values [CCx, CDC, CGC].

# Sampling Input Space: ----------------------------------------------------------------------------

SampStrategy = 'lhs'     # Sampling Strategy (Other Options Is 'rsu')
N = 3000                 # Sample Size

# Perform Sampling:

X = sampleGenerator(SampStrategy, M, DistrFun, xmin, xmax, N).round(decimals=4)

# Model Evaluation: --------------------------------------------------------------------------------

# Location of Crop File:
pathFile = r"C:\Users\pooya\Documents\GitHub\GLUE-AquaCrop\FAO\AquaCrop\DATA\Wheat.CRO".strip("*u202a")

# Location of Result:
outputAquaCropPath = r"C:\Users\pooya\Documents\GitHub\GLUE-AquaCrop\FAO\ACsaV60\OUTP\projectPROseason.OUT"

# Location of Output:
outputProjectPath = r"C:\Users\pooya\Documents\GitHub\GLUE-AquaCrop\FAO\ACsaV60\OUTP\projectOutput.OUT"

# Location of ACsaV60.exe:
pathACsaV60 = r"C:\Users\pooya\Documents\GitHub\GLUE-AquaCrop\FAO\ACsaV60\ACsaV60.exe"

# lookup:
parameter = ['Maximum canopy cover (CCx)',
             'Canopy decline coefficient (CDC)',
             'Canopy growth coefficient (CGC)']

# Find Specific Line in File:
lineNumber = list(map(findLine, [pathFile] * len(parameter), parameter))

result = []

for i in range(len(X)):
  # New Value:
  newValue = X[i,:]
  
  # Create New Line:
  newLine = list(map(createNewLine, [pathFile] * len(parameter), lineNumber, newValue))
  
  # Replace New Line into File:
  for j in range(len(lineNumber)):
    replaceLine(pathFile=pathFile, lineNumber=lineNumber[j], newLine=newLine[j])
  
  # Run AquaCrop:
  runACsaV60(pathFile=pathACsaV60)
  
  time.sleep(2)
  
  # Open Output AquaCrop:
  outputAquaCrop = open(file=outputAquaCropPath, mode='r').readlines()
  result.append(outputAquaCrop[4])

# Save Output:
with open(file=outputProjectPath, mode='a+') as f:
    for item in result:
        f.write("%s\n" % item)
outputProject.close()

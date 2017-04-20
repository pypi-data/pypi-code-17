
# Packages
import numpy as np
import pandas as pd

# Begin Function
def psuedoinverse(filename):

    # Read CSV File
    print("Initiating...")
    print("Importing data from ", filename)
    print("------------------------------------------------------------")
    df = pd.read_csv(
            filepath_or_buffer=filename,
            header=0
            )
    df.fillna(0, inplace=True)
    print("Dataframe populated:")
    print(df)
    print("-----------------------------------------------------------")
    # Create Matrices: AX = B
    print("Splicing data...")
    nrows,ncols = df.shape
    A = df.iloc[0:,0:ncols-1].as_matrix()
    B = df.iloc[0:,[ncols-1]].as_matrix()
    header = list(df.iloc[0:,0:ncols-1])
    print("AX = B")
    for i in range(0,ncols-1):
        if (i == int(nrows/2)):
            print(A[i,:],"[",header[i],"]"," = ",B[i])
        else:
            print(A[i,:],"[",header[i],"]","   ",B[i])
    print("Data spliced.")
    print("-----------------------------------------------------------")
    # Evaluate Input for Potential Error
    #-enough equations for number of unknowns


    # Moore-Penrose Psuedo-Inverse: X = (A'A)^(-1)A'B
    print("Evaluating Moore-Penrose Psuedo-inverse...")
    print("X = (A'A)^(-1)A'B")
    At = A.transpose()
    X1 = np.matmul(At, A) #*At*B
    X2 = np.linalg.inv(X1)
    X3 = np.matmul(X2,At)
    X = np.matmul(X3,B)
    print("A solution was found!")
    print("-----------------------------------------------------------")
    for i in range(0,ncols-1):
        if (i == int(nrows/2)):
            print("[",header[i],"]"," = ",X[i])
        else:
            print("[",header[i],"]","   ",X[i])

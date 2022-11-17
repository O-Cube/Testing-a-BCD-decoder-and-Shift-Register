# Obed Oyandut
# Laborators exercise 1 Embedded Systems Verification and Testing

import pandas as pd
import numpy as np
import u3
import os
import time as tm

path = 'C:/Users/49152/Desktop/MeasureData/'


d = u3.U3()
d.configIO() # all  pins digital



def fetchData(row): 
    # Activates the required voltage on the pins. Row is a list of 5 elements
    [num, negLT, negRBI, ABCD, abcdefg] = row
    # By default all the voltage on all pins is turn off and only turn on if necessary.
    d.getFeedback(u3.BitDirWrite(8, 1), u3.BitDirWrite(9, 1), u3.BitDirWrite(10, 1), u3.BitDirWrite(11, 1), \
        u3.BitDirWrite(15, 1), u3.BitDirWrite(14, 1), u3.BitDirWrite(12, 1), u3.BitDirWrite(13, 1)) # 8-11 ABCD respectively, clock = 15, pload = 14, LT= 12, Blank= 13
    d.getFeedback(u3.BitStateWrite(8, 0), u3.BitStateWrite(9, 0), u3.BitStateWrite(10, 0), u3.BitStateWrite(11, 0), \
        u3.BitStateWrite(15, 0), u3.BitStateWrite(14, 0), u3.BitStateWrite(12, 0), u3.BitStateWrite(13, 0)) # 8-11 ABCD respectively, clock = 15, pload = 14, LT= 12, Blank= 13
    
    # turn on nPL
    d.getFeedback(u3.BitStateWrite(14, 1))
    if negLT == '1':
        # turn on negLT
        d.getFeedback(u3.BitStateWrite(12, 1))
    if negRBI == '1':
        # turn on negLT
        d.getFeedback(u3.BitStateWrite(13, 1))
    
    if ABCD[0] == '1':
        # turn on D
        d.getFeedback(u3.BitStateWrite(11, 1))
    if ABCD[1] == '1':
        # turn on C
        d.getFeedback(u3.BitStateWrite(10, 1))
    if ABCD[2] == '1':
        # turn on B
        d.getFeedback(u3.BitStateWrite(9, 1))
    if ABCD[3] == '1':
        # turn on A
        d.getFeedback(u3.BitStateWrite(8, 1))
    
    # turn on nPL
    # d.getFeedback(u3.BitStateWrite(14, 1))
    # tm.sleep(0.5)
    # turn off nPL
    d.getFeedback(u3.BitStateWrite(14, 0))
    tm.sleep(0.1)
    # turn on nPL
    d.getFeedback(u3.BitStateWrite(14, 1))
    outBits = ''
    results = 'NotTested'
    # configure serial output to fio16
    d.getFeedback(u3.BitDirWrite(16, 0))
    
    for i in range(8):
        # turn off clock
        d.getFeedback(u3.BitStateWrite(15, 0))
        tm.sleep(0.1)
        # turn on clock
        d.getFeedback(u3.BitStateWrite(15, 1))
        tm.sleep(0.1)
        # read and append serial out to outBits
        outBit = d.getFeedback(u3.BitStateRead(16))
        outBits = outBits+str(outBit[0])
    outBits = outBits[::-1]
    if (abcdefg == outBits):
        results = 'Passes'
    else:
        results = 'Failed'
    return {'num':num, 'negLT':negLT, 'negRBI':negRBI, 'ABCD':ABCD, 'abcdefg':abcdefg, 'outBits':outBits, 'results':results}

# Test vector.
# input values from 0-9 and their corresponding expected values
dic = {'Number':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 'nBI', 'nRBI', 'nLT'], \
    'negLT': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', 'X', '1', '0'], \
    'negRBI': ['1', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', 'X'], \
    'ABCD':['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111', 'XXXX', '0000', 'XXXX' ], \
         'abcdefg':['01111110', '00110000', '01101101', '01111001', '00110011', '01011011', '00011111', '01110000', '01111111', '01110011', '00001101', '00011001', '00100011', '01001011', '00001111', \
            '00000000', '00000000', '00000000', '01111111']} 

        
df = pd.DataFrame(dic)  # preparation
df2 = pd.DataFrame(columns=['num', 'negLT', 'negRBI', 'ABCD', 'abcdefg', 'outBits', 'results']) # Results
print(df)

# write preparation and result to file
try:
    df.to_csv(path+'prep.csv', sep=',', mode='w')
    df.to_csv(path+'results.csv', sep=',', mode='w')
except:
    os.rmdir(path+'prep.csv')
    os.rmdir(path+'results.csv')
    df.to_csv(path+'prep.csv', sep=',', mode='w')
    df2.to_csv(path+'results.csv', sep=',', mode='w')

# Reopens test vector from file for testing
df1 = pd.read_csv(path+'prep.csv')

# loops through each row of the test vector, test the row and write the results to file
for i in range(len(df)):
    rowTest = fetchData(list(df.iloc[i]))
    dataFrameRowTest = pd.DataFrame(rowTest)
    # add results to df1
    pd.concat([df1, dataFrameRowTest])
# write results to file
df2.to_csv(path+'results.csv', sep=',')
# Display results
print(df2)
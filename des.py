import copy
def passItThroughPC1():
    tempK = K.replace(" ","")
    #print('57',tempK[41])
    KPlus = PC1 #to get the same sized matrix
    i=0
    j = 0
    for row in PC1:
        j =0
        for value in row:
            #print("i:",i," j:",j)
            KPlus[i][j] = tempK[value-1] 
            j = j+1

        i = i+1

    #print(KPlus) 
    #print(KPlus)
    tempString = ""
    for i in KPlus:
        for j in i:
            tempString = tempString+j

    cNod, dNod = tempString[:len(tempString)//2],tempString[len(tempString)//2:]
    
    formSixteenKeys(cNod, dNod)

def formSixteenKeys(cNod, dNod):
    
    leftShifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    cN = []
    dN = []
    keys = []
    kN = []
    

    cN.append(cNod)
    dN.append(dNod)

    c=0
    d=0

    for i in leftShifts:
        test_str_c = cN[c]
        temp = (i) % len(test_str_c) 
        res = test_str_c[temp : ] + test_str_c[ : temp]
        cN.append(res)
        c = c+1

        test_str_d = dN[d]
        temp2 = (i) % len(test_str_d)
        res2 = test_str_d[temp2 : ]+test_str_d[ : temp2]
        dN.append(res2)
        d=d+1
        
    for count in range(1,17):
        cNdN = ""+cN[count] + dN[count]
        kN = copy.deepcopy(PC2) #to get the same lengths string

        i=0
        j = 0
        for row in kN:
            j = 0
            for value in row:
                kN[i][j] = cNdN[value-1] 
                j = j+1

            i = i+1
        
        #print("KN: ",kN)
        temp = ""
        for i in kN:
            for j in i:
                temp = temp + j
            temp = temp+" "

        #now we have all 16 keys
        keys.append(temp)
    applyInitialPerm(keys)

def applyInitialPerm(keys):
    #pass M through IP
    tempM = M.replace(" ","")
    i=0
    j = 0
    for row in IP:
        j = 0
        for value in row:
            IP[i][j] = tempM[value-1] 
            j = j+1

        i = i+1
    
    tempString = ""
    for i in IP:
        for j in i:
            tempString = tempString+j

    lNod, rNod = tempString[:len(tempString)//2],tempString[len(tempString)//2:]
    performIterations(lNod,rNod,keys)

def performIterations(lNod,rNod,keys):
    #16 keys of 48 bits each
    #keys have a space after every 6 bits
    #lNod and rNod is of 32 bits each with no spaces

    prevL = lNod
    prevR = rNod 
    
    for count in range (0,16):
        key = keys[count]
        lN = prevR

        #passing prevR through e bit selection table
        tempEtable = copy.deepcopy(E_Table)
        i=0
        j = 0
        for row in tempEtable:
            j = 0
            for value in row:
                tempEtable[i][j] = prevR[value-1] 
                j = j+1

            i = i+1
        
        temp_E_prevR = ""
        for i in tempEtable:
            for j in i:
                temp_E_prevR  = temp_E_prevR +j
        
        #now we have E(Rn-1) of 48 bits without spaces
        key = key.replace(" ","")
        
        xor = ""
        for i in range(len(key)):
            if (key[i] == temp_E_prevR[i]):  
                xor += "0"
            else:  
                xor += "1"
        
        #making groups of 6 bits B1B2B3B4B5B6B7B8
        xor = xor[0:6]+" "+xor[6:12]+" "+xor[12:18]+" "+xor[18:24]+" "+xor[24:30]+" " +xor[30:36]+" "+xor[36:42]+" "+xor[42:48]
        bList = xor.split(' ')
        outputBlist = ''
        
        #passing through substitution tables
        for num in range(0,len(bList)):
            b = bList[num]
            #print('B ',b)
            row = b[0]+b[5]
            col = b[1:5]
            

            row = binaryToDecimal(int(row))
            col = binaryToDecimal(int(col))
            #print('row: ',row,' col: ',col)
            temp = sList[num]
            #print(temp[row][col])
            outputBlist+=format(temp[row][col],'04b')
            
        #passing outputBList through P Block now
        #print(outputBlist)
        tempP = copy.deepcopy(P)
        i = 0
        for row in tempP:
            j = 0
            for value in row:
                #print('val: ',value)
                tempP[i][j] = outputBlist[value-1] 
                j = j+1

            i = i+1
        
        tempString = ""
        for i in tempP:
            for j in i:
                tempString = tempString+j

        #xoring tempString finally to form rN
        rN = ""
        for i in range(len(tempString)):
            if (tempString[i] == prevL[i]):  
                rN += "0"
            else:  
                rN += "1"
        #print('rN: ',rN)
        prevR = rN
        prevL = lN

    
    passThroughFinalIP1(lN,rN)

def passThroughFinalIP1(lN, rN):
    rNlN = rN+lN
    result = ''

    i = 0
    for row in IP1:
        j = 0
        for value in row:
            IP1[i][j] = rNlN[value-1] 
            j = j+1

        i = i+1
    temp = '' 
    temp2 = ''   
    for i in IP1:
        c = 0
        for j in i:
            if(c<4):
                temp+=j
            else:
                temp2+=j
            c+=1     

        #print('temp: ', temp,' ',temp2)           
        hex1 = hex(int(temp,2))
        hex2 = hex(int(temp2,2))
        result += hex1[2] +hex2[2]
        temp = ''
        temp2 = ''

    print('The final cipher text for M = 0123456789ABCDEF is: ',result)

def binaryToDecimal(binary): 
      
     
    decimal, i =  0, 0
    while(binary != 0): 
        dec = binary % 10
        decimal = decimal + dec * pow(2, i) 
        binary = binary//10
        i += 1
    return decimal


#Starter code
K = "00010011 00110100 01010111 01111001 10011011 10111100 11011111 11110001"
M = "0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111"
PC1 = [[57  , 49  ,  41 ,  33  ,  25 ,   17 ,   9],
        [ 1 ,  58,    50 ,  42  ,  34  ,  26 ,  18],
        [10    ,2   , 59,   51 ,   43,    35   ,27],
        [19  , 11    , 3,   60    ,52 ,   44   ,36],
        [63   ,55    ,47 ,  39    ,31  ,  23   ,15],
        [7  , 62   , 54  , 46   , 38   , 30   ,22],
        [14  ,  6  ,  61   ,53  ,  45    ,37  , 29],
        [21  , 13 ,    5  , 28 ,   20   , 12 ,   4]]

PC2 = [[14   , 17 ,  11    ,24 ,    1   , 5],
       [ 3   , 28  , 15   ,  6  ,  21   ,10],
         [23   , 19   ,12   ,  4  ,  26   , 8],
         [16   ,  7  , 27   , 20   , 13   , 2],
         [41   , 52  , 31   , 37   , 47  , 55],
         [30   , 40  , 51   , 45   , 33 ,  48],
         [44  ,  49  , 39  ,  56    ,34 ,  53],
         [46 ,   42  , 50 ,   36   , 29 ,  32]]
                                                

IP = [[58  ,  50 ,  42 ,   34 ,   26 ,  18 ,   10 ,   2],
      [60  ,  52 ,  44 ,   36 ,   28 ,  20 ,   12 ,   4],
      [62  ,  54 ,  46 ,   38 ,   30 ,  22 ,   14 ,   6],
      [64  ,  56 ,  48 ,   40 ,   32 ,  24 ,   16 ,   8],
      [57  ,  49 ,  41 ,   33 ,   25 ,  17 ,    9 ,   1],
      [59  ,  51 ,  43 ,   35 ,   27 ,  19 ,   11 ,   3],
      [61  ,  53 ,  45 ,   37 ,   29 ,  21 ,   13 ,   5],
      [63  ,  55 ,  47 ,   39 ,   31 ,  23 ,   15 ,   7]]

E_Table = [[32   ,  1 ,   2  ,   3 ,    4 ,   5],
        [4   ,  5 ,   6  ,   7 ,    8 ,   9],
        [8   ,  9 ,  10  ,  11 ,   12 ,  13],
        [12   , 13 ,  14  ,  15 ,   16 ,  17],
        [16   , 17 ,  18  ,  19 ,   20 ,  21],
        [20   , 21 ,  22  ,  23 ,   24 ,  25],
        [24   , 25 ,  26  ,  27 ,   28 ,  29],
        [28   , 29 ,  30  ,  31 ,   32 ,   1]]

S1 = [
    [14 ,  4,  13  ,1 ,  2 ,15,  11 , 8,   3 ,10,   6 ,12,   5 , 9,   0 , 7],
    [0  ,15  , 7  ,4  ,14  ,2  ,13 , 1  ,10 , 6 , 12 ,11  , 9 , 5  , 3  ,8],
    [4  , 1  ,14  ,8  ,13  ,6   ,2 ,11  ,15 ,12  , 9  ,7   ,3 ,10   ,5  ,0],
    [15 , 12 ,  8,  2  , 4 , 9  , 1,  7  , 5 ,11  , 3 ,14  ,10,  0   ,6 ,13]
]

S2 = [
    [15 , 1   ,8 ,14   ,6 ,11   ,3,  4   ,9 , 7   ,2 ,13  ,12 , 0   ,5 ,10],
      [3 ,13  , 4 , 7  ,15 , 2   ,8, 14  ,12 , 0  , 1 ,10  , 6 , 9  ,11 , 5],
      [0 ,14 ,  7 ,11 , 10  ,4  ,13 , 1 ,  5  ,8 , 12 , 6 ,  9  ,3  , 2 ,15],
     [13 , 8,  10 , 1,   3 ,15 ,  4  ,2,  11  ,6 ,  7 ,12 ,  0  ,5 , 14  ,9]

]

S3 = [[10 , 0  , 9, 14  , 6,  3  ,15,  5  , 1, 13  ,12,  7  ,11,  4  , 2 , 8],
     [13  ,7  , 0 , 9  , 3 , 4   ,6 ,10  , 2 , 8  , 5 ,14  ,12 ,11  ,15  ,1],
     [13  ,6 ,  4 , 9 ,  8 ,15  , 3  ,0 , 11 , 1 ,  2 ,12 ,  5 ,10  ,14  ,7],
      [1 ,10,  13 , 0,   6  ,9 ,  8  ,7,   4 ,15,  14 , 3,  11 , 5 ,  2 ,12]
]

S4 = [
    [7 ,13  ,14,  3   ,0,  6   ,9 ,10   ,1,  2,   8 , 5 , 11 ,12 ,  4 ,15],
     [13,  8  ,11,  5  , 6, 15   ,0,  3  , 4  ,7  , 2 ,12  , 1 ,10  ,14 , 9],
     [10 , 6 ,  9 , 0 , 12 ,11  , 7 ,13 , 15  ,1  , 3 ,14  , 5 , 2  , 8 , 4],
      [3 ,15,   0  ,6,  10  ,1 , 13 , 8,   9  ,4  , 5 ,11  ,12 , 7  , 2 ,14]

]

S5 = [
    [2 ,12   ,4,  1   ,7 ,10  ,11,  6  , 8 , 5  , 3 ,15  ,13,  0  ,14,  9],
    [14 ,11  , 2, 12 ,  4 , 7,  13,  1,   5 , 0,  15 ,10,   3,  9,   8,  6],
    [4  ,2  , 1 ,11 , 10 ,13  , 7,  8 , 15 , 9  ,12 , 5  , 6 , 3  , 0 ,14],
    [11 , 8,  12 , 7 ,  1, 14,   2, 13 ,  6 ,15,   0 , 9 , 10 , 4 ,  5,  3]
]

S6 = [
    [12,  1  ,10, 15  , 9,  2  , 6,  8   ,0 ,13  , 3,  4 , 14,  7  , 5 ,11],
    [10 ,15  , 4 , 2 ,  7, 12 ,  9 , 5  , 6  ,1  ,13 ,14  , 0 ,11 ,  3 , 8],
    [9 ,14  ,15  ,5 ,  2 , 8 , 12  ,3  , 7 , 0  , 4 ,10  , 1 ,13 , 11  ,6],
    [4 , 3 ,  2 ,12,   9 , 5,  15 ,10 , 11 ,14 ,  1 , 7 ,  6 , 0 ,  8 ,13]
]

S7 = [
    [4 ,11  , 2 ,14  ,15,  0   ,8, 13   ,3 ,12  , 9 , 7   ,5, 10   ,6 , 1],
    [13 , 0 , 11 , 7 ,  4,  9 ,  1, 10 , 14 , 3  , 5 ,12  , 2, 15  , 8 , 6],
    [1  ,4 , 11 ,13 , 12  ,3 ,  7 ,14 , 10 ,15  , 6 , 8  , 0  ,5  , 9 , 2],
    [6 ,11,  13 , 8,   1 , 4,  10 , 7,   9 , 5 ,  0 ,15 , 14  ,2 ,  3 ,12]
]

S8 = [
    [13,  2  , 8,  4  , 6, 15  ,11,  1  ,10,  9  , 3, 14  , 5,  0 , 12,  7],
    [1 ,15  ,13 , 8  ,10 , 3  , 7 , 4  ,12 , 5  , 6 ,11  , 0 ,14 ,  9 , 2],
    [7 ,11  , 4 , 1  , 9 ,12 , 14 , 2  , 0 , 6  ,10 ,13 , 15 , 3 ,  5 , 8],
    [2 , 1 , 14  ,7 ,  4 ,10,   8 ,13 , 15 ,12 ,  9 , 0 ,  3 , 5 ,  6 ,11]
]

P = [

    [16,   7,  20,  21],
    [29,  12,  28,  17],
    [1 , 15 , 23 , 26],
    [5 , 18 , 31 , 10],
    [2 ,  8 , 24 , 14],
    [32,  27,   3,   9],
    [19,  13,  30,  6],
    [22,  11,   4,  25]
]

IP1 = [ 

            [40,     8,   48,    16,    56,   24,    64,   32],
            [39,     7,   47,    15,    55,  23,    63,   31],
            [38,     6,   46,    14,    54,  22,    62,   30],
            [37,     5,   45,    13,    53,   21,    61,   29],
            [36,     4,   44,    12,    52,   20,    60,   28],
            [35,     3,   43,    11,    51,   19,    59,   27],
            [34,     2,   42,    10,    50,   18,    58,   26],
            [33,     1,   41,     9,    49,   17,    57,   25]
            ]


sList = []
sList.append(S1)
sList.append(S2)
sList.append(S3)
sList.append(S4)
sList.append(S5)
sList.append(S6)
sList.append(S7)
sList.append(S8)
passItThroughPC1()



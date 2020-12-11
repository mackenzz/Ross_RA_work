import os
import random



# generate random number
def U():
    return random.random()


def alpha(i):
    '''This is to compute alpha'''
    alpha = 0

    # ifdef SYNSET1B:
    alpha = (i - N/2) * 2.0 / N
    # elif i >= N / 2 and i < N / 2 + R:
    alpha = 1
    # else:
    if Alpha < 0:
        alpha = (i * 2.0 / N - 1)
    else:
        alpha = Alpha

    return alpha

# define some synergies:
# define SYNEQ0 ((1.0 - std::pow(i * 2.0 / N - 1.0, Beta)) * fitness1(form, i))
# define SYNEQ1 ((1.0 - alpha(i)) * fitness1(form, i))
# define SYNEQ2 (Sim * (1.0 - alpha(i)) * fitness1(form, i))
# define SYNEQ3 (fitness1(form, i))
# define SYNEQ4 (Sim * fitness1n(form, i))

# define SYNEQ SYNEQ2


K = 6  # temporarily use 0 to store it
Alpha, Beta, Sim, Delta = 0.0, 0.0, 0.0, 0.0  # temporarily use 0 to store it


class Environment:
    interStruct = []  # the interaction matrix
    # For each row in interStruct, use an unordered_map to store key-value pair
    # where key is a string of length (K+1), and value is its fitness value.
    # Note: K is different for each row

    comb2fit = []
    interStruct = []
    R = 5  # number of relateness, temporarily use 0 to store it

    def __init__(self, inputFile, N):
        '''If inputFile is an empty string, it means we will construct
        it later using randomized NK matrix.'''
        self.inputFile = inputFile
        self.N = N
        # Check whether file exsits
        if not os.path.exists(inputFile):
            return

        # check whether the file is empty
        if os.path.getsize(inputFile) == 0:
            pass
        else:
            # note down the position that the num is 1 (the num could be 0 or 1)
            f = open(inputFile)
            for i in range(N):
                toPush = []
                for j in range(N):
                    if inputFile[i][j] >> bit != 0:
                        if bit == 1:
                            toPush.append(j)
                        else:
                            raise TypeError("Error in reading inputFile.")
            self.interStruct.append(toPush)

        #   self.printNKMatrix()  # for debugging



    def printNKMatrix(self):
        '''This method is used to print NK matrix for debugging.'''
        print(self.interStruct)

    #   C++ code direct translation:
    #         for line in self.interStruct:
    #             output = [0 for _ in range(self.N)]
    #             for i in line:
    #                 output[i] = 1
    #             for i in line:
    #                 print(i, ' ')
    #             print('\n')
    #         print('\n')

    def createRandomNKMatrix(self, K):
        '''This method is to create a random symmetric NK matrix,
        call this when inputFile is empty.'''

        # Clear interStruct before populating.
        interStruct = []

        ids = set()

        # create the first N/2 attibutes K interaction terms.
        for i in range(self.N // 2):
            ids.add(i)
            count = 0
            while len(ids) != K:
                index = self.N // 2 * U()
                pickedIdx = min(int(index), self.N // 2 - 1)
                ids.add(pickedIdx)

            output = list(ids)
            interStruct.append(output)
            ids = set()

        # Due to symmetry, the remaining N/2 attributes will have K interaction terms
        # which could be derived from the first N/2 attributes.
        for i in range(self.N // 2):
            output = interStruct[i]
            for ele in output:
                ele += self.N // 2
            interStruct.append(output)
        return interStruct

    def construct(self):
        '''This method is to build the unordered_map "comb2fit" by mapping each combination
        attribute (with a size of K) to a random fitness value. Contribution of each attribute
        depends on K attribf c wutes (self included), i.e there are 2^K combinations of
        attributes which will be mapped to 2^K fitness values'''

        # Clear comb2fit before populating.
        comb2fit = []

        for i in range(self.N):
            K = len(self.interStruct[i])
            numOfComb = 1 << K
            obj = Environment(numOfComb, 0.0)  ######################## not quite sure
            comb2fit.append(obj)
            for j in range(numOfComb):
                comb2fit[-1][j] = U()
        return comb2fit

    def fitness1(self, form, i):
        fit = 0
        comb = 0
        for id in self.interStruct[i]:
            comb = (comb << 1) + form[id]  # Extract the interacting attributes.
        if i >= N // 2:
            a = alpha(i)
            fit += Sim * ((1 - a) * self.comb2fit[i][comb] + a * self.comb2fit[i - N / 2][comb]) + (1 - Sim) * \
                   self.comb2fit[i][comb]
        else:
            fit += self.comb2fit[i][comb]
        return fit

    def fitness1n(self, form, i):
        fit = 0
        comb = 0
        for id in self.interStruct[i]:
            comb = (comb << 1) + form[id]
        fit += self.comb2fit[i][comb]
        return fit

    def calcFitness(self, form, start, end):
        '''Return the fitness value of the substring, within [start,end), of a string,
        e.g. start = 0, end = N means the to calculate the fitness of entire string.'''

        fit = 0
        for i in range(start, end):
            fit += self.fitness1(form, i)
        return fit / (end - start)

#     def calcSynergy(self, form):
#         syn = 0
#         #ifdef SYNERGY
#             for int i in range(N / 2, N):
#                 if form[i] == form[i - N / 2]:
#                     syn += Delta * (SYNEQ)
#         return syn / N # average



# test cases
f = 'test.txt'
e = Environment(f, 20)
e.createRandomNKMatrix(6)
print(e.createRandomNKMatrix(6))


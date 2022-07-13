from operator import index, indexOf
import re
import math
import random
from turtle import pos, position
from time import time


from numpy import sort
def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

class Wordle:
    def __init__(self) -> None:
        self.__wordlist=[] # list of words sorted in alphabetical order
        unsortedwords=[]
        f=open('wordlewords.txt','r')
        for line in f:
            t=line.split()
            unsortedwords.append(t[0])
        f.close()
        self.__wordlist=sorted(unsortedwords)

    def checkWord(self,word):
        for i in self.__wordlist:
            if  i==word:
                return True
        return False

    
    def getWordList(self):
        return self.__wordlist
    
    def getClue(self,attemptword,goalword):
        ## given an attempt word and a goal word
        ## this function return the clue as a string
        ## i.e if letter is present in the correct position,
        ## clue in that position is green
        ## if letter is present in goalword but not correct position
        ## the clue in that position is yellow
        ## if attemptword contains 2 times same letter in incorrect position
        ## and goalword contains that letter only once, the first letter
        ## is yellow e.g goalword='SLATE', clueword='elect', clue=ygxxy''

        clue=['x','x','x','x','x'] # start with no matches
        letter_used=[0,0,0,0,0] # the letter in that position in the goal has been used to assign a 'y' or 'g'

        for i in range(0,5):
            if attemptword[i]==goalword[i]:
                clue[i]='g'
                letter_used[i]=1
        # if any letter in the attempword is present in the goalword 
        # but not at the correct position and that letter has not been
        # assigned a ''g'or a 'y, we assign it a 'y 
        # the thing to be careful here is when either the goal or the attempt word has repeated letters
        # the priority is a follows, 
        # e.g  attempt: brass, goal: rusty, output: xyxyx (first s assigned a yellow) 
        # e.g  attempt: glass, goal: slosh, output: xgxgy (the s in correct position gets green and the other s get y)*/
        
        for g in range(0,5):
            if letter_used[g]==0:
                for a in range(0,5):
                    if (attemptword[a]==goalword[g] and clue[a]=='x' and letter_used[g]==0):
                        clue[a]='y'
                        letter_used[g]=1
        
        return ''.join(clue)

    
    def isWordValid(self,word,clue,clueword)->bool:
        ## given a word, a clue and a clueword
        ## we check if the word is a valid word
        ## i.e we get the same clue
        ## eg word='stead' , clue='xxyxy', clueword='crane' 
        return clue==self.getClue(clueword,word)
    
    def getPossibleWords(self,reducedWordList,clueMat,clueWordMat):
        # takes an array even if it is size 1 eg ['xxgxx']
        sol_list=[]

        for l in reducedWordList:
            result=True
            for i in range(0,len(clueMat)):
                result=result and self.getClue(clueWordMat[i],l)==clueMat[i]
                if result==False:
                    break
            if result==True:
                sol_list.append(l)
        
        return sol_list   

    def getWordsForGivenClue(self,clueword,clue,listofwords):
        # given a word, a clue and a list
        # returns all the words in that list that correspond to that
        #clue
        possible_words=[]
        for w in listofwords:
            if  self.getClue(clueword,w)==clue:
                possible_words.append(w)
        
        return possible_words
    def getNumberFromClue(self,str_clue):
        str_dict={"x":0,"y":1, "g":2}
        num=0
        for i in range(0,5):
            num+=str_dict[str_clue[i]]*math.pow(3,i)
        return int(num)

    def getClueFromNumber(self,num):
        # there are 3*3*3*3*3=243 possible clues
        # given a number between 0 and 242, this function
        # returns the clue
        # 'x'=0, 'y'=1, g='2'
        # 0 corresponds to xxxxx
        # 242 corresponds to ggggg
        # least significant bit is on the left
        
        num_dict={0:"x", 1:"y", 2:"g"}
        cluecode=['x','x','x','x','x']
        i=0
        while(num!=0):
            cluecode[i]=num_dict[int(num%3)]
            num=(num-num%3)/3
            i=i+1
        return ''.join(cluecode)

    @timer_func
    def getWordsForEachClue(self,word,listofwords):
        # given a word and a list
        # return all the possible words for each possible clue
        # e.g  word=slate, for each possible clue ('xxxxx', 'yxxxy') that slate can generate
        # we will return the possible words
        possible_words_for_each_clue={}
        for w in listofwords:
            clue=self.getClue(word,w)
            if clue in possible_words_for_each_clue:
                possible_words_for_each_clue[clue].append(w)
            else:
                possible_words_for_each_clue[clue]=[]
                possible_words_for_each_clue[clue].append(w)
        return possible_words_for_each_clue

    def calculateEntropy(self,possible_words_for_each_clue):
        # calculate the entropy for the list given
        # the list is in the form of a dictionay
        # in the form  possible_words_for_each_clue[clue]=[array of words]
        # where clue can be 'hhhhh' and each h can take values 'x','y' or 'g'
        entropy=0
        p=0 # probability
        total_words=0
        for k in possible_words_for_each_clue:
            total_words+=len(possible_words_for_each_clue[k])
        for d in possible_words_for_each_clue:
            p=len(possible_words_for_each_clue[d])/total_words
            entropy+=p*math.log2(1/p)
        return entropy
            
    


    
    
    def PlayWordle(self):
        clueMat=[]
        clueWordMat=[]
        word_list=self.__wordlist
        suggest_word=['cater', 'react', 'least', 'stale', 'heart', 'crane', 'slate', 'parse', 'crate', 'trace'] #suggestWord(word_list,word_list)#self.suggestWord2D(word_list)
        print("Hello Are You Ready To Cheat")
        for i in range(0,5):
            print("We suggest you use with {} for your {}st/th try".format(suggest_word,i+1))
            word_input=input("Enter your word: ")
            clue_input=input("Enter the clue given to you: ")
            clueMat.append(clue_input)
            clueWordMat.append(word_input)
            word_list=self.getPossibleWords(word_list,clueMat,clueWordMat)
            printList(word_list)
            suggest_word=suggestWord(word_list,self.__wordlist)
            print("========Played till now======")
            for cl,clw in list(zip(clueMat,clueWordMat)):
                print(f'{clw }:{ cl}')
            
        


        






def quick_sort(arr):
    len_arr=len(arr)
    if len_arr<=1:
        return arr
    if len_arr==2:
        if arr[0][1]>=arr[1][1]:
            return ([arr[1],arr[0]])
        else:
            return (arr)

    # use last element as a pivot
    p=arr[len_arr-1]
    left_of_pivot=[]
    right_of_pivot=[]

    for i in range(len_arr-1):
        if arr[i][1]>p[1]:
            right_of_pivot.append(arr[i])
        else:
            left_of_pivot.append(arr[i])

    return (quick_sort(left_of_pivot)+[p]+quick_sort(right_of_pivot))



def printList(f):
    print('{:<20}'.format('******List********'))
    for w in f:
        print(w)
        
    print(f'Number in list: {len(f)}')
    print('{:<20}'.format('******EndList********'))



def encodeClue(clue):
    clue=list(clue)
    ## we are going to use 2 bit to encode each 
    ## character
    ## LSB is on the leftmost
    ## x-0
    ## y-1
    ## g-2
    number=0
    clue_dict={'x':0,'y':1,'g':2}
    for i in range(0,5):
        number=number+clue_dict[clue[i]]*math.pow(4,i)
    
    return number





if __name__=="__main__":
    w=Wordle()
   # w.PlayWordle()

   #list_words=['hedge','hence','hinge','horde','niche', 'tithe']
   #letter_dict=calcLetters(list_words)

   #for key,value in letter_dict.items():
   #    print(f'{key}:{value}')
    
    #w.PlayWordle()
    #l=w.getWordList()
    #r_list=[l[random.randint(0,2000)] for i in range(0,25)]
    #print(w.checkWord('alibi','xgyxx','slate'))
    #print(w.checkWord('alibi','yxxxx','bigot'))
  
    word_list=w.getWordList() # list of wordle words
    ## for each word we find how many bits of information they can give

    cluewords=["crane","salty"]
    clue=["xxyxx","xgxxx"]
    f=w.getPossibleWords(w.getWordList(),clue,cluewords)
    word_array=[]
    entropy_array=[]
    group_array=[]
    for word in f:
        possible_words=w.getWordsForEachClue(word,f)
        entropy=w.calculateEntropy(possible_words)
        word_array.append(word)
        entropy_array.append(entropy)
        group_array.append(len(possible_words.keys()))
        word_entropy=list(zip(word_array,entropy_array,group_array))
        word_entropy.sort(key=lambda i: i[1],reverse=True)
        print(word,word_entropy)
    
    def findClues():
        word_array=[]
        entropy_array=[]
        group_array=[]
        for word in word_list:
            possible_words=w.getWordsForEachClue(word,word_list)
            entropy=w.calculateEntropy(possible_words)
            word_array.append(word)
            entropy_array.append(entropy)
            group_array.append(len(possible_words.keys()))

        word_entropy=list(zip(word_array,entropy_array,group_array))
        word_entropy.sort(key=lambda i: i[1],reverse=True)
        fi=open('word_entropy.txt','w')
        for elem in word_entropy:
            print(f'{elem[0]} : {elem[1]}  : {elem[2]}')
            fi.write(f'{elem[0]}, {elem[1]}, {elem[2]}')
            fi.write('\n')
        fi.close()

        ## take the 
        sl=slice(15)
        words=[x[0] for x in word_entropy[:15:]]
        entropy_array=[]
        word_array=[]
        fi=open('best_possible_second_word.txt','w')
        for welem in words:
            ## for this particular word find the words for all given clue
            all_possible=w.getWordsForEachClue(welem,w.getWordList())
            ### for each word in a particular clue, get the one with the highest entropy
            for d in all_possible:
                entropy_array=[]
                word_array=[]
                for welem2 in w.getWordList(): # get the best word from the wordle list, not the reduced list
                    clue_possible=w.getWordsForEachClue(welem2,all_possible[d])
                    entropy=w.calculateEntropy(clue_possible)
                    entropy_array.append(entropy)
                    word_array.append(welem2)
                word_entropy=list(zip(word_array,entropy_array))
                word_entropy.sort(key=lambda i: i[1],reverse=True)
                fi.write(f'{welem}-->{d}-->{word_entropy[0][0]}')
                fi.write('\n')
        fi.close()




    ## sort the element in word_entropy
    



    
    
    
    
 
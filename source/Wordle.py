from operator import index, indexOf
import re
import math
import random

from numpy import sort
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
    
    def isLetterInWord(self,letter,word,typ,index)->bool:
        # given any letter and its typ
        # (letter,yellow,index)--> given a word check if that letter is present in any position except index
        # (letter,green,index)--> given a word check if letter is at index
        # (letter,gray, index)--> given a word check, return true if letter is not present
        assert(typ=='y' or typ=='g' or typ=='x') 

        ### repeated letters can be troublesome 
        ### for e.g in the word suppose the solution word is mover
        ### we play rover, the clue assigned to rover will be xgggg
        ### n if we play array it will be xyxxx

        ### check if word is double


        result=False
        if typ=='g':
            if letter==word[index]:
                return True
            else:
                return False

        
        if typ=='x':
            for l in word:
                if l==letter:
                    return False #if we find that letter in the word, it is invalid
            return True
        
        for i in range(0,len(word)):
            if word[i]==letter:
                if index==i:
                    return False
                else:
                    return True
        
        return False





    
    def isWordValid(self,word,clue,clueword)->bool:
        ## when a player plays a word,
        ## he gets clues toward the solution corresponding to that word
        ## yellow, that particular letter is in solution word but not correct pos
        ## green, that particular letter is in solution word n at correct position/
        ## gray, that letter is not in the solution word
        ## given a word, the clue and the word to get the clue (clueWord)
        ## this function determines if that word is a valid word 
        result=[False, False, False, False , False]
        p=True
        for  i in range(0,len(clue)):
            result[i]=self.isLetterInWord(clueword[i],word,clue[i],i)
            if result[i]==False:
                return False


        
        for i in result:
            p=i and True
        
        return p
    
    def getPossibleWords(self,reducedWordList,clueMat,clueWordMat):
        sol_list=[]
        # yellow - 'y'
        # gray   - 'gr''
        # green  - 'g' 

        #for word in reducedWordList:
        #    if self.isWordValid(word,clue[0],clueWord[0]):
        #        sol_list.append(word)
         
        #for word in reducedWordList:
        #    result=True
        #    for i in range(0,len(clueMat)):
        #        result=result and self.isWordValid(word,clueMat[i],clueWordMat[i])
        #        if result==False:
        #            break
        #    if result==True:
        #        sol_list.append(word)
        

        for l in reducedWordList:
            result=True
            for i in range(0,len(clueMat)):
                result=result and self.checkWord(l,clueMat[i],clueWordMat[i])
                if result==False:
                    break
            if result==True:
                sol_list.append(l)
        
        return sol_list   

    def checkWord(self,wordtocheck,clue,clueword):
        ## wordtocheck, clue and clueword are of type str i.e 'xxxxx'and not ['xxxxx']
        ## given wordtocheck, the clue and the clueword corresponding to clue
        ## return True if the word is valid else False
        ## there are four possibilities,
        ## wordtocheck and clueword both have repeated letters
        ## wordtochek and clueword have both distinct letters (no repetition)
        ## wordtocheck has repeated letters and clueword distinct letters
        ## wordtocheck has distinct letters and clueword repeated letters

        ## both have distinct letters
        ## brown-wordtocheck and beany-clueword clue-- gxxyx
        ## b is green hence b is in correct place
        ## e,a,y are  x hence a word containing e is invalid
        ## n is yellow, hence it is present but not at the correct place

        ## problems with double letters
        ## if wordtocheck is AMBLE and clueword is ABBEY and clue is yxgyx
        ## there are 2Bs and one of them is given an x, so that invalidates ABBEY but it is included

        ## the strategy would be to check for  all green and yellow and then invalidates a letter only if it is not present in green or yellow
        for c in clue:
            assert(c=='x' or c=='g' or c=='y') #check only these letters are in clue

        # the test gives 5 clues, each of the clues should pass
        # for each clue we store it in result

        result=[False,False,False,False,False]

        for i in range(0,5):
            if clue[i]=='g': # if clue[i] is 'g', wordtocheck[i] should be equal to clueword[i]
                if wordtocheck[i]==clueword[i]:
                    result[i]=True
            elif clue[i]=='y': # if clue[i] is 'y', if wordtocheck[j]==clueword[i] and i!=j pass
                for j in range(0,5):
                    if (wordtocheck[j]==clueword[i]):
                        if (i==j):
                            result[i]=False
                            break # no need to check other elements if a true is found since there be another same element not highlighted
                        else:
                            result[i]=True
                            break

            else:  # case for 'x'
                ## if clue[i]=='x'
                ## 1) results[i]==True, if for all k wordtocheck[j]!=clueword[i] 
                ## 2) result[i]==False, if there is at least one k such that wordtocheck[j]==clueword[i]
                #     and no k such that clueword[k]==clueword[i] b!=i and clue[b]=='g' or 'y' 
                is_letter_present=True # 
                for j in range(0,5):
                    if wordtocheck[j]==clueword[i]:
                        is_letter_present=True # the letter is present in the 
                        break
                    else:
                        is_letter_present=False
                
                # if letter is present check clueword at all places except j for same letter
                if is_letter_present:
                    for k in range(0,5): # find another clueword[i] in clueword
                        if (clueword[i]==clueword[k]) and (k!=i):
                            if (clue[k]=='g' or clue[k]=='y'):
                                result[i]=True  # if we find same letter but with a clue 'g' or 'y', that word becomes valid
                                break
                else:
                    result[i]=True


            if result[i]==False:
                return False
        return True








    def suggestWord1D(self,reducedWordList):
        # given a list of possible valid words
        # suggest a word to play
        prob_dic={}
        count=0
        value_word=[]
        ## calculate the number of occurences of letters in each word
        for word in reducedWordList:
            for letter in word:
                count=count+1
                if letter in prob_dic.keys():
                    prob_dic[letter]=prob_dic[letter]+1
                else:
                    prob_dic[letter]=1
        
        ## to each word assign a value
        ## that value is sum of each corresponding letter from the dict
        v=0
        max=0
        suggested_word=''
        for word in reducedWordList:
            for letter in list(set(word)):
                v=v+prob_dic[letter]
            value_word.append(v)
            if v>max:   ### find the maximum and return that word
                suggested_word=word
                max=v
            v=0
        sortedList=quick_sort(list(zip(reducedWordList,value_word)))
        if len(sortedList)>5:
            for i in (sortedList[1:5]):
                print(i)
        else:
            for i in reversed(sortedList):
                print(i)

        return suggested_word
    def suggestWord2D(self,reducedWordList):
        ## this one is similar to the one above except
        ## there is a dictionary for each index
        prob_dict=[{},{},{},{},{}] # list of dictionaries
        prob_dict[0]={}  # dictornay for first letter in word
        prob_dict[1]={}  # dictornay for second letter in word
        prob_dict[2]={}  # dictornay for third letter in word
        prob_dict[3]={}  # dictornay for fourth letter in word
        prob_dict[4]={}  # dictornay for fifth letter in word

        suggested_word=''
        value_word=[]
        for word in reducedWordList:
            for i in range(0,len(word)):
                if word[i] in prob_dict[i].keys():
                    prob_dict[i][word[i]]=prob_dict[i][word[i]]+1
                else:
                    prob_dict[i][word[i]]=1
        #print(prob_dict)

        # to each word assign a  value
        v=0
        max=0
        for word in reducedWordList:
            for i in range(0,len(word)):
                v=v+prob_dict[i][word[i]]
            value_word.append(v)
            if v>max:
                suggested_word=word
                max=v
            v=0

        sortedList=quick_sort(list(zip(reducedWordList,value_word)))
        if len(sortedList)>10:
            for i in reversed(sortedList[-10:]):
                print(i)
        else:
            for i in reversed(sortedList):
                print(i)
        #print("Everything from sortedList")        
        #for i in sortedList:
         #   print(i)

        return suggested_word 
    
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

def calcLetters(listwords):
    # given a list of words calculate 
    # the number of times each letter occurs
    letter_dict={}
    for word in listwords:
        for l in word:
            if l  in letter_dict.keys():
                letter_dict[l]+=1
            else:
                letter_dict[l]=1
    
    total=0
    for val in letter_dict.values():
        total+=val
    entropy=0
    for key in letter_dict.keys():
        letter_dict[key]=(letter_dict[key]*1.0/total)
        entropy=entropy+letter_dict[key]*math.log2(1/letter_dict[key])

    # we now assign a (quasi)probabilty to each word 
    # wich is the sum of the its letters probabbility
    list_word_prob=[]
    temp=0
    total=0
    for word in listwords:
        for l in word:
            temp=temp+letter_dict[l]
        list_word_prob.append([word,temp])
        total+=temp ## since the sum 
        temp=0
    entropy=0
    for t in list_word_prob:
        t[1]=t[1]/total
        entropy=entropy+t[1]*math.log2(1/t[1])

    for t in list_word_prob:
        print(f"{t[0]}:{t[1]}")
    print("The entropy for the list of words is:{}".format(entropy))


    
    return letter_dict

def getClue(goalword,attemptword):
    # function to get the clue given a goal word
    # and an attemptword. the function has to find the 
    # 'x', 'y' and 'g' at each position

    ### the algorithm works as follows
    ### we look for green first and store those index
    ### we then ignore them both in attemptword and goalword
    ## with the rest we look for yellow
    ## and then we do for grays

    clue=list('xxxxx')

    for i in range(0,5):
        if attemptword[i]==goalword[i]:
            clue[i]='g'

    for i in range(0,5):
        for j in range(0,5):
            if attemptword[i]==goalword[j] and clue[j]!='g':
                clue[i]='y'
    
    return  ''.join(clue)


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

def suggestWord(reducedList,wordleList):
    ## for all words in wordleList
    ## find how many different clues each word gives
    ## the one with the maximum number of clues is the suggest word
    result=[]
    for attemptword in wordleList:
        for goalword in reducedList:
            clue=getClue(goalword,attemptword) 
            clueCode=encodeClue(clue)
            result.append([goalword,attemptword,clue,clueCode])

    ## for each word that was an attempt word, we created a dictionary of code (keys)
    dict_attempt=dict(zip(wordleList,[[] for i in wordleList]))
    for row in result:
        if row[3] not in dict_attempt[row[1]]:
            dict_attempt[row[1]].append(row[3])
    
    #print("Printing dictionary")
    #for l in dict_attempt.items():
    #    print(f'{l[0]}:{l[1]}')

    max_word=[['',0] for i in range(10)]

    for d in dict_attempt.items():
        if len(d[1])>max_word[0][1]:
            max_word[0][0]=d[0]
            max_word[0][1]=len(d[1])
            max_word=quick_sort(max_word)
    
    print("The suggested words are:")
    for l in max_word:
        print(f"{l[0]}: {l[1]}")
    return [row[0] for row in max_word]


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
    print(getClue("arbor","aback"))
    print(getClue("ablob","abbey"))
   




    #w.PlayWordle()
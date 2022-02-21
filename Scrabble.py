

from sys import stdin
import math
import sys
import random


TILES_USED = 0 # records how many tiles have been returned to user
CELL_WIDTH = 3 # cell width of the scrabble board
SHUFFLE = False # records whether to shuffle the tiles or not

# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]

# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board

# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s,t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem//2
    s = t*rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t*rem
    return s

# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH*" "
    board_str =  "  |" + "|".join(getString(item," ") for item in range(len(Board)))  +"|"
    line1 = "--|" + "|".join(getString("","-") for item in range(len(Board)))  +"|"

 
    print(board_str)
    print(line1)
    
    for i in range(len(Board)):
        row = str(i) + " "*(2-len(str(i))) +"|"
        for j in range(len(Board)):
            row += getString(Board[i][j]," ") + "|"
        print(row)
        print(line1)
        
    print()

scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter,score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line= line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)


validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")


Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################


# this is the function to place the tiles on the board. This one specifically will place the word inputted onto the board horizontally
def horizontal(word):
    list = []
    value = 0
    #first it appends all letters of the word into a list
    for i in word:
        list.append(i)
        
    # puts every letter from the list into the board. The 'value' component will allow the board to keep moving horizontally by adding 1 each time to the location
    for letter in list:
        Board[location[0]][location[1]+value] = letter
        value += 1


# this is the function to place the tiles on the board. This one specifically will place the word inputted onto the board vertically
def vertical(word):
    value = 0
    list = []
    #first it appends all letters of the word into a list
    for i in word:
        list.append(i)
        
    # puts every letter from the list into the board. The 'value' component will allow the board to keep moving horizontally by adding 1 each time to the location
    for letter in list:
        Board[location[0]+ value][location[1]] = letter
        value += 1
        


#this function will check whether integers are used when inputting the location of the word. Numbers can only range from 0-15 as that is the maximum
#before this function, there is another function that splits the location at ':'
def locationchecker(location):
    numbers = ['1','2','3','4','5','6','7','8','9','0','10','11','12','13','14','15']

#location[0] will be the row, while location[1] will the be collums.
# if either location[0] and location[1] is not in 'numbers' then it will not work and return false
    if location[0] not in numbers:
        print('not interger, try again:')
        return False
    else:

        if location[1] not in numbers:
            print('not interger, try again:')
            return False

        else:
            return True
# this is a code just to change location[1] location[0] to integers from lists and location[2] to uppercase so that comparisons can be made later
def locationchanger(location):
    location[0] = int(location[0])
    location[1] = int(location[1])
    location[2] = location[2].upper()

#this function will check whether the inputted word is placed at the center of the board on the first turn
def boardcenter(location):

    locationchanger(location)
    #checks if row is the center of board
    if location[0] != BOARD_SIZE//2:
        print('The first move must be at the center of the board at:',BOARD_SIZE//2,':',BOARD_SIZE//2,':','h/v')
        return False
    else:
        #checks if collums is center of board
        if location[1] != BOARD_SIZE//2:
            print('The first move must be at the center of the board at:',BOARD_SIZE//2,':',BOARD_SIZE//2,':','h/v')
            return False
        else:
            return True


#this function will check if the word is within the dictionary
def dictionarytest (word):
    file = open("dictionary.txt","r")
    #goes through dictionary and strips /n
    for i in file:
        i = i.strip()
        #if a word in dictionary is the same as the word inputted, it will return true
        if i == word:
            return True
    else:
        print('Word not in dictionary')
        return False

#this function will go through myTiles and check if word can be made
def sorttiles(word):
    score = 0
    z = 0
    new_list = []
    #appends all tiles from myTiles to a new list
    for letter in myTiles:
        new_list.append(letter)
    for letter in word:
        #for each individual letter of word inputted, it should be able to remove a letter from myTiles, and 'z' is the counter of how many tiles are removed
        #if counter 'z' does not equal to the length of the word, then there was a letter it couldnt remove and therefore cannot be made using myTiles
        length_of_word = len(word)
        if letter in new_list:
            z = z + 1
            new_list.remove(letter)
    x = True

    if z!= length_of_word:
        z = 0
        print('this word cannot be made using your tiles')
        return False
 



    
        
#this function is to check whether the location and direction of the inputted word will fit into the board
def boardsizechecker(location):
    n = len(word)

    locationchanger(location)
    #checks which direction it is going
    if location[2] == 'H':
        #if 'n' which is length of word plus the location of collums exceeds the board size then it will not fit onto the board and returns false
        if n + location[1] > BOARD_SIZE:
            print('Not Within Board Range!')
            return False
        else:
            return True
    #checks the direction it is going
    elif location[2] == 'V':
        #if 'n' which is length of word plus the location of rows exceeds the board size then it will not fit onto the board and returns false
        if n + location[0] > BOARD_SIZE:
            print('Not Within Board Range!')
            return False
        else:
            return True


#this function combines the inputting word functions at the start with the getTiles, printBoard, printTiles functions together
def boardinput(word):

    #checks direction    
    if location[2] == 'H':
        #because the code will input letters that will connect the inputted word onto the board, the function will reverse the tiles so that it will remove the letters that were added to myTiles first
        #then it will reverse all the letters back
        for i in word:
            myTiles.reverse()
            myTiles.remove(i)
            myTiles.reverse()
        #proceeds into the standard inputting word horizontally, print board, getTiles, printTiles
        horizontal(word)
        printBoard(Board)
        getTiles(myTiles)
        printTiles(myTiles)
        
    #checks directions
    elif location[2] == 'V':
        #exactly the same as above except this time vertically
        for i in word:
            myTiles.reverse()
            myTiles.remove(i)
            myTiles.reverse()
        #proceeds into the standard inputting word vertically, print board, getTiles, printTiles
        vertical(word)
        printBoard(Board)
        getTiles(myTiles)
        printTiles(myTiles)

#this function will assemble all functions that check the inputted word together
#this is the firstloop as in the first word inputted, it has to be centered
#all individual functions explained above
def firstloop(word):

    if dictionarytest(word) == False:
        return False
    elif locationchecker(location) == False:
        return False

    elif boardcenter(location) == False:
        return False
    elif sorttiles(word) == False:
        return False
    elif boardsizechecker(location) == False:
        return False
    else:
        return True
    
#this is exactly the same as the first loop but it does not have the 'boardcenter' function
#all individual functions explained above
def secondloop(word):

    if dictionarytest(word) == False:
        return False
    elif locationchecker(location) == False:
        return False

    elif boardsizechecker(location) == False:
        return False
    elif letterchecker(word) == False:
        return False

    elif sorttiles(word) == False:
        return False

    else:
        return True
    
#this function will check whether the code will use the right format for location input    
def formatchecker(location):
    criteria = '1234567890VHvh:'
    criteria1 = True
    for i in location:
        if i not in criteria:
            print('Must be in row:col:direction format with only V or H as direction')
            criteria1 = False
            return False


#this function will check if the word can be connected onto the board
def letterchecker(word):
    #scorelist is the letters used to connect the word inputted onto the board
    #the scores of these letters are deducted later when calculating the score
    global scorelist
    alphabet = ['Q','W','E','R','T','Y','U','I','O','P','L','K','J','H','G','F','D','S','A','Z','X','C','V','B','N','M']
    scorelist = []
    testlist = []
    testlista = []
    testlistb = []
    lista = []
    value = 0
    wordlist = []
    for i in word:
        wordlist.append(i)
#this function will be divided into 'H' or 'V', horizontal or vertical and it will run depending on which is inputted
        
    #checks if any letters within the word inputted is on the board
    #if there is it will input into 'testlist'
    for letter in word:
        for i in range(BOARD_SIZE):
            if letter in Board[i]:
                testlist.append(letter)

    #this will check if a letter on the board is within 'testlist' which is the list that checks if any letters within the board inputted is on the board    
    if location[2] == 'H':
        for i in range(len(word)):
            if location[1] + i < BOARD_SIZE:
                #it will go through every collum with rows being station to see if a letter in word is in testlist
                #'i' is a counter to keep the board moving
                if Board[location[0]][location[1]+ i] in testlist:
                    lista.append(Board[location[0]][location[1]+ i])

    #exactly the same as above but for vertically
    if location[2] == 'V':
        for i in range(len(word)+1):
            if location[0] + i < BOARD_SIZE:
                if Board[location[0]+ i][location[1]] in testlist:
                    lista.append(Board[location[0]+ i][location[1]])





    #this function will check the location of each letter that is able to connect with the inputted word                
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for k in range(len(testlist)):
                if Board[i][j] == testlist[k] :
                    #testlist a and b will append all rows and collums of these letters that is able to connect with the inputted word          
                    testlista.append(i)
                    testlistb.append(j)



    #this will check if the word can fit onto the board
    #this assembles everything above in this function
    if location[2] == 'V':
        
        for letter in word:
            Board[location[0] + value][location[1]] == letter
            #goes through all the lists - testlista and b, lista to see if the word inputted contains the letter that connects it onto the board
            if location[1] in testlistb:
                    if location[0] + value in testlista:
                        if Board[location[0] + value][location[1]] in testlist:
                            inputboard = True
                            #this will check if the word will move any existing tiles on the board
                            #it will go through every row and the stationary collum to check if the present tiles on the board is the same as the ones in the word when the word inputted is printed onto the board
                            for length in range(BOARD_SIZE - location[0]):
                                if length < len(wordlist):
                                    if Board[location[0] +length][location[1]] in alphabet:
                                        if Board[location[0] +length][location[1]] == wordlist[length]:
                                            for i in word:
                                                #this will append all letters that will connect the word into myTiles
                                                #this will make sure sorttiles function will work
                                                #it will remove the letter from lista after it appends onto myTiles so that it does not append the same letter twice
                                                if i in lista:
                                                    myTiles.append(i)
                                                    scorelist.append(i)
                                                    lista.remove(i)
                                        #if letter is different to the one in the word imputted it means if the word is placed onto the board it will remove a existing letter from the board
                                        #therefore it will return False
                                        else:
                                            inputboard = False
                            if inputboard == True:
                                return True
                            
            value += 1


        else:
            print('Your word does not connect onto the board properly')
            return False
        
    #exactly same as above but instead, for horizontal
    if location[2] == 'H':
        for letter in word:
            Board[location[0]][location[1]+ value] == letter
            if location[0] in testlista:
                    if location[1]+ value in testlistb:
                        if Board[location[0] ][location[1] + value] in testlist:
                            inputboard = True
                            for length in range(BOARD_SIZE - location[1]):
                                if length < len(wordlist):
                                    if Board[location[0]][location[1] +length] in alphabet:
                                        if Board[location[0]][location[1] +length] == wordlist[length]:
                                            for i in word:
                                                if i in lista:
                                                    myTiles.append(i)
                                                    scorelist.append(i)
                                                    lista.remove(i)
                                        
                                        else:
                                            inputboard = False
                            if inputboard == True:
                                return True

                            
            value += 1
        else:
            print('Your word does not connect onto the board properly')
            return False

#this function is specifically for the finding of maximum scoring words from the dictionary, specifically horizontally
def horizontaldictionarytest(word, myTiles):
    global K0
    global K1
    global indexlist3
    global letternumber
    alphabet = ['Q','W','E','R','T','Y','U','I','O','P','L','K','J','H','G','F','D','S','A','Z','X','C','V','B','N','M']
    myTiles1 = []
    Boardlist = []
    indexlist1 = []
    indexlist2 = []
    indexlist3 = []
    letternumber = 0
    wordlist = []

    #checks if any letters on word can connect with ones on the board        
    for i in range(BOARD_SIZE):
        for letter in Board[i]:
            if letter in alphabet:
                Boardlist.append(letter)
    #checks what letters and where a letter or letters can connect on the board with inputted word
    for i in word:
        if i in Boardlist:
            for L0 in range(BOARD_SIZE):
                for L1 in range(BOARD_SIZE):
                    if Board[L0][L1] == i:
                        #indexlist1 is all the rows of letteres on the board that can connect with inputted word
                        #indexlist2 is all the collums of letteres on the board that can connect with inputted word
                        #indexlist3 is all the letters that can connect with the inputted word thats on the board
                        indexlist1.append(L0)
                        indexlist2.append(L1)
                        indexlist3.append(Board[L0][L1])
    
    #this will check if words from the dictionary can be made using the tiles on the board and tiles in myTiles
    myTiles1 = []
    for tiles in myTiles:
        myTiles1.append(tiles)
    inmytiles = True
    #checks if word can be made from myTiles
    for letter in word:
        if letter in myTiles1:
            myTiles1.remove(letter)
        else:
            #if letter in word not in myTiles it will check if it is on indexlist3 (letters that can connect the word onto the board)
            if letter in indexlist3:
                myTiles1.append(letter)
                myTiles1.remove(letter)
            else:
                inmytiles = False

    if inmytiles == True:
        # K0 and K1 are all the collums and rows possible on the board
        #this part of the function will go through the entire board
        for K0 in range(BOARD_SIZE):
            for K1 in range(BOARD_SIZE):
                z = 0
                c = 0


                doubleletter = 0
                #first it finds the letter that joins the word onto the board
                for joiningletter in word:

                    if joiningletter == Board[K0][K1]:

                        letternumber = 0
                        wordlist = []
                        for letters in word:
                            wordlist.append(letters)
                        #if it has found a letter that joins the word onto the board, then it will find the number of the letter in the word, eg T in BESTAIN will be number 4
                        for num2 in range(len(word)):
                            if wordlist[0] != joiningletter:
                                wordlist.remove(wordlist[0])
                                letternumber += 1

                        letternumber += 1
                       #checks for double letters eg. runnion (2 'n')         
                        if doubleletter == 1:
                            letternumber += 1
                        val = True
                        #checks if the inputted word can fit on the right side on the joining letter
                        for num3 in range(len(word) - letternumber):
                            if K1 + num3 < BOARD_SIZE:
                                #skips all empty spaces and goes to areas of the board that has a letter
                                if Board[K0][K1 + num3] in alphabet:
                                    #if the letter is the same as the one in the inputted word, then it signals that the word can fit
                                    if wordlist[num3] != Board[K0][K1 + num3]:
                                        val = False
                                else:
                                    if wordlist[num3] not in myTiles:
                                        val = False
                                
                                    
                            else:
                                val = False
        
                       #checks if the inputted word can fit on the left side on the joining letter                     
                        if val == True:
                            if K1 + len(word) - letternumber < BOARD_SIZE:
                                #checks where the word starts
                                if letternumber - 1 <= K1:
                                    wordlist = []
                                    start1 = K1 + 1 - letternumber
                                    inboard = True

                                    for letter1 in word:

                                        #this will go through all lists that has all the joining letters and checks if the word can fit into the board
                                        #does exact same thing as above but instead of the right side of the joining word, it does the left
                                        if letter1 not in myTiles:
                                            if letter1 in indexlist3:
                                                #if the board is in alphabet or not a empty space on the board
                                                if Board[K0][start1] in alphabet:
                                                    if Board[K0][start1] != letter1:
                                                        letternumber = 0
                                                        wordlist = []
                                                        inboard = False
                                                    #start1 + 1 will just move where the code is checking, 1 to the right
                                                    else:
                                                        start1 += 1
                                                        
                                                else:
                                                    inboard = False
                                            #if the letter isn't in indexlist3(a letter that can connect the word from the dictionary) then it won't work and return false       
                                            else:
                                                inboard = False
                                        else:
                                            if Board[K0][start1] in alphabet:
                                                if Board[K0][start1] != letter1:
                                                    inboard = False
                                            start1 += 1


                                    if inboard == True:
                                        #previously the code checked the left and right side of the joining letter to see if the word fits
                                        #this is the final check to see if the whole word fits from the start of the word to the finish
                                        starter = 0
                                        start = K0 + 1 - letternumber
                                        checkwordlist = []
                                        checkwordlist2 = []
                                        lastcheck = True
                                        #creates a duplicate myTiles list
                                        for tiles in myTiles:
                                            checkwordlist.append(tiles)
                                        #creates a list where it has all the letters from word inputted
                                        for letters in word:
                                            checkwordlist2.append(letters)
                                            

                                       #it will start from the start of where the word is going to be inputted and check if the word fits 
                                        for numb1 in range(len(word)):
                                            if start + numb1 < BOARD_SIZE:
                                                if checkwordlist2[numb1] != Board[K0][start+numb1]:
                                                    if checkwordlist2[numb1] in checkwordlist:
                                                        checkwordlist.remove(checkwordlist2[numb1])
                                                    else:
                                                        lastcheck = False               
                                        if lastcheck == True:
                                            return True


                                else:
                                    letternumber = 0
                                    wordlist = []
                            #this part is to see if there are double letters, so that the code will not identify the same letter twice
                            else:
                                wordlist = []
                                for letter12 in word:
                                    wordlist.append(letter12)
                                    #checks if the letter currently and next letter is the same
                                for doub in range(len(word)):
                                    if doub + 1 <= len(wordlist) -1:
                                        if wordlist[doub] == wordlist[doub+1]:
                                            doubleletter = 1

                            

#exactly the same as the horizontaldictionarytest from above but for vertical words
def verticaldictionarytest(word, myTiles):
    global K0
    global K1
    global indexlist4
    global letternumber

    alphabet = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'L', 'K', 'J', 'H', 'G', 'F', 'D', 'S', 'A', 'Z', 'X',
                'C', 'V', 'B', 'N', 'M']
    myTiles1 = []
    Boardlist = []
    indexlist1 = []
    indexlist2 = []
    indexlist4 = []
    letternumber = 0
    wordlist = []


    for i in range(BOARD_SIZE):
        for letter in Board[i]:
            if letter in alphabet:
                Boardlist.append(letter)

    for i in word:
        if i in Boardlist:
            for L0 in range(BOARD_SIZE):
                for L1 in range(BOARD_SIZE):
                    if Board[L0][L1] == i:
                        indexlist1.append(L0)
                        indexlist2.append(L1)
                        indexlist4.append(Board[L0][L1])

    myTiles1 = []
    for letters in myTiles:
        myTiles1.append(letters)
    inmytiles = True
    for letter in word:
        if letter in myTiles1:
            myTiles1.remove(letter)
        else:
            if letter in indexlist4:
                myTiles1.append(letter)
                myTiles1.remove(letter)
            else:
                inmytiles = False

    if inmytiles == True:
        for K1 in range(BOARD_SIZE):
            for K0 in range(BOARD_SIZE):
                z = 0
                c = 0

                doubleletter = 0
                for joiningletter in word:

                    if joiningletter == Board[K0][K1]:

                        letternumber = 0
                        wordlist = []
                        for letters in word:
                            wordlist.append(letters)

                        for num2 in range(len(word)):
                            if wordlist[0] != joiningletter:
                                wordlist.remove(wordlist[0])
                                letternumber += 1

                        letternumber += 1
                        if doubleletter == 1:
                            letternumber += 1
                        val = True

                        for num1 in range(len(word) - letternumber):
                            if K0 + num1 < BOARD_SIZE:
                                if Board[K0 + num1][K1] in alphabet:
                                    if wordlist[num1] != Board[K0 + num1][K1]:
                                        val = False
                                else:
                                    if wordlist[num1] not in myTiles:
                                        val = False



                            else:
                                val = False

                        if val:
                            if K0 + len(word) - letternumber < BOARD_SIZE:

                                if letternumber - 1 <= K0:
                                    wordlist = []
                                    start1 = K0 + 1 - letternumber
                                    withintheboard = True

                                    for letters2 in word:

                                        if letters2 not in myTiles:
                                            if letters2 in indexlist4:

                                                if Board[start1][K1] in alphabet:
                                                    if Board[start1][K1] != letters2:
                                                        letternumber = 0
                                                        wordlist = []
                                                        withintheboard = False
                                                    else:
                                                        start1 += 1
                                                else:
                                                    withintheboard = False
                                            else:
                                                withintheboard = False
                                        else:
                                            if Board[start1][K1] in alphabet:
                                                if Board[start1][K1] != letters2:
                                                    withintheboard = False
                                            start1 += 1

                                    if withintheboard == True:

                                        starter = 0
                                        start = K0 + 1 - letternumber
                                        checkwordlist = []
                                        checkwordlist2 = []
                                        lastcheck = True
                                        for i in myTiles:
                                            checkwordlist.append(i)

                                        for i in word:
                                            checkwordlist2.append(i)
                                            

                                            
                                        for numb4 in range(len(word)):
                                            if start + numb4 < BOARD_SIZE:
                                                if checkwordlist2[numb4] != Board[start +numb4][K1]:
                                                    if checkwordlist2[numb4] in checkwordlist:
                                                        checkwordlist.remove(checkwordlist2[numb4])
                                                    else:
                                                        lastcheck = False
                                        if lastcheck == True:

                                            return True

                                            
                                                


                                else:
                                    letternumber = 0
                                    wordlist = []
                            else:
                                wordlist = []
                                for letters3 in word:
                                    wordlist.append(letters3)
                                for doub in range(len(word)):
                                    if doub + 1 <= len(wordlist) - 1:
                                        if wordlist[doub] == wordlist[doub + 1]:
                                            doubleletter = 1


#this function will combine both vertical and horizontal dictionarytests together to check for the highest scoring word
def dictionarymaxtiles(myTiles):
    global Max_word
    file = open("dictionary.txt","r")
    alphabet = ['Q','W','E','R','T','Y','U','I','O','P','L','K','J','H','G','F','D','S','A','Z','X','C','V','B','N','M']
    Max_score = 0
    Max_word = ''
    H0 = 0
    H1 = ''
    H2 = 0
    H3 = 0
    V0 = 0
    V1 = ''
    V2 = 0
    V3 = 0
    #go through all words in the dictionary
    for k in file:
        k = k.strip()
        #word is more than the length of the board will be automatically removed
        if len(k) <= BOARD_SIZE:
            horizontaldictionarytest(k, myTiles)
            if horizontaldictionarytest(k, myTiles) == True:
                #if the word goes through the dictionarytest functions (horizontal) and it returns true, it will check if it fits onto the board
                myTiles2 = []
                for i in k:
                    myTiles2.append(i)
                start = K1 - letternumber + 1
                starter = 0
                for tilesonboard in Board[K0]:
                    if starter == start:
                        if tilesonboard in indexlist3:
                            if tilesonboard in myTiles2:
                                myTiles2.remove(tilesonboard)
                    else:
                        starter += 1

               #it will caculate the score for each letter of the word of the dictionary
                #this will run for all words in dictionary, and if one word beats another in score, then max score will change to the highest scoring word
                temp_score = 0
                for letter in myTiles2:
                    temp_score += getScore(letter)
                if temp_score > Max_score:
                    Max_score = temp_score
                    Max_word = k
                    H0 = Max_score
                    H1 = Max_word
                    H2 = K0
                    H3 = starter
                



            #exactly the same as above but for all words that is possible for vertical input
            verticaldictionarytest(k, myTiles)
            if verticaldictionarytest(k, myTiles) == True:

                myTiles3 = []
                for i in k:
                    myTiles3.append(i)
                    
                start = K0 - letternumber + 1
                starter = 0
                val = 0
                for numbers in range(BOARD_SIZE):
                    if starter == start:
                        if start + val < BOARD_SIZE:
                            if Board[start + val][K1] in indexlist3:
                                if Board[start + val][K1] in myTiles3:
                                    myTiles3.remove(Board[start + val][K1])
                                    val += 1
                                else:
                                    val +=1
                            else:
                                val +=1
                    else:
                        starter += 1
                #temp_score is the score for the current word inputted, if the next word from the dictionary has a higher tempt score, then Max score and Max word will be changed to the higher scoring word
                temp_score = 0
                for letter in myTiles3:
                    temp_score += getScore(letter)
                if temp_score > Max_score:
                    Max_score = temp_score
                    Max_word = k
                    V0 = Max_score
                    V1 = Max_word
                    V2 = start
                    V3 = K1
    #this checks if the vertical high score word is higher scoring or the horizontal
    #the code will print according to which is higher
    if V0 > H0:
        print('Maximum possible score in this move was:', V0,'with the word', V1, 'at', V2, ':', V3, ': V')

    if V0 < H0:
        print('Maximum possible score in this move was:', H0,'with the word', H1, 'at', H2, ':', H3, ': H')
    file.close() 


#because the first loop is a bit different to the second loop, and the word needs to be centered, another find maximum word from dictionary function is made                            
def maxtiles123(myTiles):
    global Max_word            
    Max_score = 0
    Max_word = ' '
    max_tile_list = []
    for letter in myTiles:
        max_tile_list.append(letter)

    


    
    file = open("dictionary.txt","r")
    for line in file:
        line = line.strip()
        given_tiles = True
        #checks if the length of the word can be placed at the center of the board
        #proceeds the same as the dictionary function above
        if len(line) <= (BOARD_SIZE // 2) +1:
            for letter in line:
                if letter in max_tile_list:
                    max_tile_list.remove(letter)
                else:
                    given_tiles = False
            
            if given_tiles == True:
                temp_score = 0
                for letter in line:
                    temp_score += getScore(letter)
                if temp_score > Max_score:
                    Max_score = temp_score
                    Max_word = line
        max_tile_list = []
        for letter in myTiles:
            max_tile_list.append(letter)
    print('Maximum possible score in this move was:', Max_score, 'with the word', Max_word, 'at', BOARD_SIZE // 2, ':',BOARD_SIZE // 2, ': H')
    file.close() 
                            
            




    
#checks the score of the word inputted
def scoring(word):
    global scoreofword
    scorewordlist = []
    scoreofword = 0
    
    for i in word:
        scorewordlist.append(i)
    #for every word in scorelist (the letters found to be connecting the word to the board from letterchecker function) it will remove the letter from the word inputted
    #makes sure that the score of the word doesnt contain letter that are already on the board
    for i in range(len(scorelist)):
        if scorelist[i] in scorewordlist:
            scorewordlist.remove(scorelist[i])

    for i in scorewordlist:
        scoreofword += getScore(i)
        






                    

                  






        


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

############################################ start of the code #####################################################################################################################################
numbers = '1234567890'
variables = 'HV'
totalscore = 0

#input word
word = input("Enter your word word:").upper()
if word == '***':
    print('bye')
else:
    
    location = input("Enter the location in row:col:direction format:")
    #checks if the word is in the format needed
    while formatchecker(location) == False:
        word = input("Enter your word word:").upper()
        location = input("Enter the location in row:col:direction format:")
        
    location = location.split(':')
        



#goes through firstloop
while word != '***':
    x = firstloop(word)
    
    if x == True:
        #if first loop is sucessfull then it will tally score and give the max word that is possible
        #then it will break to the second loop below
        for i in word:
            totalscore += getScore(i)
        maxtiles123(myTiles)
        if Max_word == word:
            print('Well done, your word was the max scoring word')
        print('Your score this turn:', totalscore)
        print('Your total score is:', totalscore)
        boardinput(word)
        break

    #if x is false it will tell the user to try again
    if x == False:
        word = input("Enter your word word:").upper()
        if word == '***':
            break
        location = input("Enter the location in row:col:direction format:")
        
        while formatchecker(location) == False:
            word = input("Enter your word word:").upper()
            location = input("Enter the location in row:col:direction format:")

        location = location.split(':')

            



#enter second loop
while word != '***':
    
    word = input("Enter your word word:").upper()
    if word == '***':
            break
    location = input("Enter the location in row:col:direction format:")
    while formatchecker(location) == False:
        word = input("Enter your word word:").upper()
        if word == '***':
            break
        location = input("Enter the location in row:col:direction format:")
    location = location.split(':')
        
    
    myTilesmaxword = []
    for i in myTiles:
        myTilesmaxword.append(i)
    
    y = secondloop(word)
    #because if y == False, then it will still change myTiles list, so to prevent that, a list is created before it changes it so that it can revert back to the same list later on
    if y == False:
        myTiles = myTilesmaxword
    #if the secondloop is true then it will tally score and give the highest scoring word possible from dictionary
    #if the secondloop is false then it will repeat the while loop

    
    if y == True:
        dictionarymaxtiles(myTilesmaxword)
        myTilesmaxword = []
        if word == Max_word:
            print('Well done, your word was the max scoring word')
        scoring(word)
        totalscore += scoreofword
        print('Your score this move:', scoreofword)
        print('Your total score is:', totalscore)
        
        boardinput(word)


       








        






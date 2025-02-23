import json
import random
from enum import Enum
from constants import *



class Rarity(Enum):
    WHITE = 0
    BLUE = 1
    GREEN = 2
    ORANGE = 3
    LIGHT_RED = 4
    PINK = 5
    LIGHT_PURPLE = 6
    LIME = 7
    YELLOW = 8
    CYAN = 9
    RED = 10
    PURPLE = 11
    RAINBOW = 12
    FIERY_RED = 13
    AMBER = 14

class KnockbackType(Enum):
    NO = 0
    EXTREMELY_WEAK = 1
    VERY_WEAK = 2
    WEAK = 3
    AVERAGE = 4
    STRONG = 5
    VERY_STRONG = 6
    EXTREMELY_STRONG = 7
    INSANE = 8

class SpeedType(Enum):
    SNAIL = 0
    EXTREMELY_SLOW = 1
    VERY_SLOW = 2
    SLOW = 3
    AVERAGE = 4
    FAST = 5
    VERY_FAST = 6
    INSANELY_FAST = 7

class WeaponData:
    def __init__(self, input_filename=""):
        self.weaponDict = {}
        self.filename = input_filename
        self.initWeaponList()
        self.solutionWeapon = random.choice(list(self.weaponDict))
    
    def initWeaponList(self):
        with open(self.filename, 'r') as fileObj:
            dataObj = json.load(fileObj)
        self.weaponDict = dataObj['weaponData']
    
    def search(self, queryWord):
        returnList = []
        for each_item in self.weaponDict:
            if each_item['rawName'].lower().startswith(queryWord.lower()):
                returnList.append(each_item)
        return returnList

class UserDataConfig:
    def __init__(self):
        self.hintOneFlag = False
        self.hintTwoFlag = False
        self.hintThreeFlag = False
        self.hintTwoStr = ""
        self.onNewLine = False
    
    def reset(self):
        self.hintOneFlag = False
        self.hintTwoFlag = False
        self.hintThreeFlag = False
        self.hintTwoStr = ""
        self.onNewLine = False
    
    def generateHintTwoStr(self, tooltip):
        if not self.hintTwoFlag:
            print("There was an issue generating the hint two string: '/hint2' is not enabled")
            return
        newStr = ""
        if 'tooltip' in tooltip:
            for each_tooltip in tooltip['tooltip']:
                newStr = newStr + '\n      '
                for each_letter in each_tooltip:
                    if each_letter == ' ' or random.randrange(0, 2) == 1:
                        newStr = newStr + each_letter
                    else:
                        newStr = newStr + UNIDENTIFIED_LETTER_CHAR
                
        self.hintTwoStr = newStr
    
    def printHintThreeStr(self, guessAmount, weaponName):
        if not self.hintThreeFlag:
            print("There was an issue generating the hint three string: '/hint3' is not enabled")
        showableChars = guessAmount - 10
        for each_letter in weaponName:
            if showableChars > 0 or each_letter == ' ':
                print(each_letter, end='')
            else:
                print(UNIDENTIFIED_LETTER_CHAR, end='')
            showableChars -= 1
        print()



def displayGuesses(guessList, correctItem, userData):
    txt = HORIZONTAL_SEPERATOR_CHAR + "{itemInfo:" + WHITESPACE_FILL_CHAR +"^{length}}"
    headerTxt = "{itemInfo:" + WHITESPACE_FILL_CHAR + "<10}"
    tempStr = ""
    statusStr = ""
    reprintIndex = None

    tempLen = 0
    curIteration = 0
    alreadyFoundBool = False
    for each_guess in guessList:
        tempLen += getLongestAttribute(each_guess) + 1
        if tempLen > MAX_LINE_LENGTH and not alreadyFoundBool:
            reprintIndex = curIteration
            alreadyFoundBool = True
        curIteration += 1
    tempLen += 10
    if userData.onNewLine:
        print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')
    else:
        print(f"{CORNER_TABLE_CHAR}", end='')
    lenOfGuess = 0
    for i in range(0, 10):
        print(VERTICAL_SEPERATOR_CHAR, end='')
    for each_guess in guessList:
        lenOfGuess += getLongestAttribute(each_guess) + 1
        if lenOfGuess > MAX_LINE_LENGTH:
            break
        else:
            for eachLetter in range(0, getLongestAttribute(each_guess) + 1):
                print(VERTICAL_SEPERATOR_CHAR, end='')
    if userData.onNewLine:
        print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')
    else:
        print(f"{CORNER_TABLE_CHAR}", end='')
    print()

    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')
    print(headerTxt.format(itemInfo="Name"),end="")
    tempLen = 0
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if each_item['data']['name'] == correctItem['data']['name']:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        else:
            statusStr = " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        print(txt.format(itemInfo=each_item['data']['name'] + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

   
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="DamageType"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if each_item['data']['damageType'] == correctItem['data']['damageType']:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        else:
            statusStr = " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        print(txt.format(itemInfo=each_item['data']['damageType'] + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

    
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Damage"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if int(each_item['data']['damage']) > int(correctItem['data']['damage']):
            statusStr = " ({low})".format(low=DOWN_INDC_CHAR)
        elif int(each_item['data']['damage']) < int(correctItem['data']['damage']):
            statusStr = " ({up})".format(up=UP_INDC_CHAR)
        else:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        print(txt.format(itemInfo=each_item['data']['damage'] + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

 
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Knockback"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if convertKnockbackToEnum(each_item['data']['knockback']) > convertKnockbackToEnum(correctItem['data']['knockback']):
            statusStr = " ({low})".format(low=DOWN_INDC_CHAR)
        elif convertKnockbackToEnum(each_item['data']['knockback']) < convertKnockbackToEnum(correctItem['data']['knockback']):
            statusStr = " ({up})".format(up=UP_INDC_CHAR)
        else:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        print(txt.format(itemInfo=each_item['data']['knockback'] + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

    
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Speed"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if convertSpeedToEnum(each_item['data']['speed']) > convertSpeedToEnum(correctItem['data']['speed']):
            statusStr = " ({low})".format(low=DOWN_INDC_CHAR)
        elif convertSpeedToEnum(each_item['data']['speed']) < convertSpeedToEnum(correctItem['data']['speed']):
            statusStr = " ({up})".format(up=UP_INDC_CHAR)
        else:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        print(txt.format(itemInfo=each_item['data']['speed'] + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

    
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Rarity"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if int(each_item['data']['rarity']) > int(correctItem['data']['rarity']):
            statusStr = " (V)"
        elif int(each_item['data']['rarity']) < int(correctItem['data']['rarity']):
            statusStr = " ({up})".format(up=UP_INDC_CHAR)
        else:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        print(txt.format(itemInfo=enumRarityToString(int(each_item['data']['rarity'])) + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

  
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Autoswing"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if each_item['data']['autoswing'] == correctItem['data']['autoswing']:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        else:
            statusStr = " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        print(txt.format(itemInfo=str(each_item['data']['autoswing']) + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

   
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Material"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        if each_item['data']['material'] == correctItem['data']['material']:
            statusStr = " ({correct})".format(correct=CORRECT_INDC_CHAR)
        else:
            statusStr = " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        print(txt.format(itemInfo=str(each_item['data']['material']) + statusStr, length=getLongestAttribute(each_item)),end="")
    print(HORIZONTAL_SEPERATOR_CHAR)

   
    print(f"{HORIZONTAL_SEPERATOR_CHAR}", end='')  
    print(headerTxt.format(itemInfo="Obtained"),end="")
    curIteration = 0
    for each_item in guessList:
        if curIteration == reprintIndex:
            break
        curIteration += 1
        for each_obt in each_item['data']['obtained']:
            tempStr += each_obt + "_"
        tempStr = tempStr[:-1].replace("_","/")
        statusStr = getObtainedChar(each_item, correctItem)
        print(txt.format(itemInfo=tempStr + statusStr, length=getLongestAttribute(each_item)),end="")
        tempStr = ""
    print(HORIZONTAL_SEPERATOR_CHAR)

    if reprintIndex != None:
        userData.onNewLine = True
        displayGuesses(guessList[reprintIndex:], correctItem, userData)
    else:
        tempLen = 0
        for each_guess in guessList:
            tempLen += getLongestAttribute(each_guess) + 1
        tempLen += 10
        print(CORNER_TABLE_CHAR, end='')
        for i in range(0, tempLen):
            print(VERTICAL_SEPERATOR_CHAR, end='')
        print(CORNER_TABLE_CHAR)
        userData.onNewLine = False
    
def getLongestAttribute(check):
    lenCtr = 0
    dataObj = check['data']
    if len(dataObj['name']) > lenCtr:
        lenCtr = len(dataObj['name'])
    if len(dataObj['damageType']) > lenCtr:
        lenCtr = len(dataObj['damageType'])
    if len(dataObj['damage']) > lenCtr:
        lenCtr = len(dataObj['damage'])
    if len(dataObj['knockback']) > lenCtr:
        lenCtr = len(dataObj['knockback'])
    if len(dataObj['speed']) > lenCtr:
        lenCtr = len(dataObj['speed'])
    if getLengthOfObtained(dataObj['obtained']) > lenCtr:
        lenCtr = getLengthOfObtained(dataObj['obtained'])
    if len(enumRarityToString(int(dataObj['rarity']))) > lenCtr:
        lenCtr = len(enumRarityToString(int(dataObj['rarity'])))
    lenCtr += 4
    return lenCtr

def enumRarityToString(value):
    return str(Rarity(value)).split(".")[1].replace("_", " ").title()

def enumKnockbackToString(value):
    return str(KnockbackType(value)).split(".")[1].replace("_", " ").title()

def convertKnockbackToEnum(kbstr):
    if kbstr == "No knockback":
        return 0
    elif kbstr == "Extremely weak":
        return 1
    elif kbstr == "Very weak":
        return 2
    elif kbstr == "Weak":
        return 3
    elif kbstr == "Average":
        return 4
    elif kbstr == "Strong":
        return 5
    elif kbstr == "Very strong":
        return 6
    elif kbstr == "Extremely weak":
        return 7
    else:
        return 8

def convertSpeedToEnum(kbstr):
    if kbstr == "Snail":
        return 0
    elif kbstr == "Extremely slow":
        return 1
    elif kbstr == "Very slow":
        return 2
    elif kbstr == "Slow":
        return 3
    elif kbstr == "Average":
        return 4
    elif kbstr == "Fast":
        return 5
    elif kbstr == "Very fast":
        return 6
    else:
        return 7

def getLengthOfObtained(obtained):
    lenCtr = 0
    for each_obtain in obtained:
        lenCtr += len(each_obtain)
        lenCtr += 1
    lenCtr -= 1
    return lenCtr

def getObtainedChar(item, correct):
    tempCounter = 0
    # if the lengths are different 
    # if item has 2 and correct as 1
    if len(item['data']['obtained']) > len(correct['data']['obtained']):
        # if correct appears in item, return 50% true
        for each_element in correct['data']['obtained']:
            if not each_element in item['data']['obtained']:
                return " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        # otherwise, return false
        return " ({semi})".format(semi=SEMI_INDC_CHAR)
    # if item has 1 and correct has 2
    elif len(item['data']['obtained']) < len(correct['data']['obtained']):
        # if item appears in correct, return true
        for each_element in item['data']['obtained']:
            if not each_element in correct['data']['obtained']:
                return " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)
        # otherwise, return false
        return " ({correct})".format(correct=CORRECT_INDC_CHAR)
    # if the lengths are the same
    else:
        for each_element in item['data']['obtained']:
            if each_element in correct['data']['obtained']:
                tempCounter += 1
    # if all elements in item appear in correct
        if tempCounter == len(item['data']['obtained']):
        # return true    
            return " ({correct})".format(correct=CORRECT_INDC_CHAR)
    # if not all elements in item appear in correct
        elif tempCounter > 0:
        # return 50%
            return " ({semi})".format(semi=SEMI_INDC_CHAR)
    # if nothing is in common,
        else:
        # return false  
            return " ({wrong})".format(wrong=INCORRECT_INDC_CHAR)

def displayHintStatus(userGuesses, userData, solutionWeapon):
    print(f"You have guessed {len(userGuesses)} times. ")
    outStrList = []
    outCmdList = []
    outStr = ""
    outCmd = ""
    # display status of options
    if not userData.hintOneFlag and len(userGuesses) >= HINT_ONE_GUESS_AMOUNT:
        outStrList.append("'Selling Price'")
        outCmdList.append("'/hint1'")
    if not userData.hintTwoFlag and len(userGuesses) >= HINT_TWO_GUESS_AMOUNT:
        outStrList.append("'Tooltip'")
        outCmdList.append("'/hint2'")
    if not userData.hintThreeFlag and len(userGuesses) >= HINT_THREE_GUESS_AMOUNT:
        outStrList.append("'Partial Name'")
        outCmdList.append("'/hint3'")
    
    if len(outStrList) > 0:
        for i in outStrList:
            outStr += i + ', '
        outStr = outStr[:-2]
        for i in outCmdList:
            outCmd += i + ', '
        outCmd = outCmd[:-2]
        print(f"- You now have access to  {outStr}  via  {outCmd}.")

    # list already enabled options
    if userData.hintOneFlag and len(userGuesses) >= HINT_ONE_GUESS_AMOUNT:
        print(f"   - Hint - Selling Price: {solutionWeapon['data']['sell']}")
    if userData.hintTwoFlag and len(userGuesses) >= HINT_TWO_GUESS_AMOUNT:
        print("   - Hint - Tooltip: ", end='')
        if len(userData.hintTwoStr) == 0:
            print("Solution Weapon does not have a Tooltip")
        else:
            print(userData.hintTwoStr)
    if userData.hintThreeFlag and len(userGuesses) >= HINT_THREE_GUESS_AMOUNT:
        print("   - Hint - Partial Name: ", end='')
        userData.printHintThreeStr(len(userGuesses), solutionWeapon['data']['name'])
    





def game():
    print("New game has started. (Type '/help' for more)")
    print()
    x = WeaponData("weapons.json")
    searchedWeapon = None
    guessList = []
    userData = UserDataConfig()

    #print(x.solutionWeapon)
    while x.solutionWeapon != searchedWeapon:
        displayHintStatus(guessList, userData, x.solutionWeapon)

        userInput = input("Guess a weapon: ")
        userInput = userInput.strip().title().replace(" ", "_") \
                             .replace("\'", "%27").replace("_Of_", "_of_") \
                             .replace("_The_", "_the_")
        myList = x.search(userInput)
        if userInput[0] == '/':
            if userInput == "/Hint1":
                if userData.hintOneFlag:
                    print("You've already enabled '/hint1'")
                else:
                    userData.hintOneFlag = True
                    print("'/help1' command successful. Enabled Selling Price Hint")
                    if not len(guessList) >= HINT_ONE_GUESS_AMOUNT:
                        print(f"(This command will not activate until {HINT_ONE_GUESS_AMOUNT} guesses)")
            elif userInput == "/Hint2":
                if userData.hintTwoFlag:
                    print("You've already enabled '/hint2'")
                else:
                    userData.hintTwoFlag = True
                    userData.generateHintTwoStr(x.solutionWeapon['data'])
                    print("'/help2' command successful. Enabled Tooltip Hint")
                    if not len(guessList) >= HINT_TWO_GUESS_AMOUNT:
                        print(f"(This command will not activate until {HINT_TWO_GUESS_AMOUNT} guesses)")
            elif userInput == "/Hint3":
                if userData.hintThreeFlag:
                    print("You've already enabled '/hint3'")
                else:
                    userData.hintThreeFlag = True
                    print("'/help3' command successful. Enabled Partial Hint")
                    if not len(guessList) >= HINT_THREE_GUESS_AMOUNT:
                        print(f"(This command will not activate until {HINT_THREE_GUESS_AMOUNT} guesses)")
            elif userInput == "/Help":
                print("nah fuck you (this command doesn't do anything yet lol my bad)")
            else:
                print(f"There was an issue processing command '{userInput[1:]}'")
            
        elif len(myList) == 0:
            print(f"There was an error finding weapon {userInput}, please try again.")
            searchedWeapon = None
        else:
            print(f"There are {len(myList)} weapons that match \'{userInput}\'")
            iteration = 1
            for each_item in myList:
                print(f"{iteration}: {each_item['data']['name']}")
                iteration += 1
            print(f"{iteration}: ... Go back")
            userInput = input("Please input the number: ")
            if userInput.isnumeric():
                userInput = int(userInput)
            else:
                userInput = -1

            if userInput == -1:
                print("There was an error processing your input. (It probably wasn't a number)")
            elif userInput < iteration:
                searchedWeapon = myList[userInput - 1]
                guessList.append(searchedWeapon)
                print()
                print(f"Current Guess Amount: {len(guessList)}")
                displayGuesses(guessList, x.solutionWeapon, userData)
            else:
                print("Going back...")
        print()
    
    print(f"Congratulations! You've guessed {x.solutionWeapon['data']['name']} in {len(guessList)} guesses!")


def main():
    outerUserInput = "Hello"
    print("Welcome to the local Terradle game, coded by Zach")
    while outerUserInput[0].lower() != 'n':
        game()
        outerUserInput = input("Would you like to play again? [Y/N]: ")  
    print("Thanks for playing!")

main()



# def newSearch(dick):
#     returnList = []
#     for each_item in dick:
#         if len(each_item['data']['obtained']) > 1:
#             returnList.append(each_item)
#     return returnList

# y = WeaponData("weapons.json")

# myList = newSearch(y.weaponDict)

# for cur_weapon in myList:
#     print(cur_weapon['data']['name'], end=': ')
#     for each_method in cur_weapon['data']['obtained']:
#         print(each_method, end=' ')
#     print()
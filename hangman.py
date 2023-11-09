# Author: Yonah Tenenbaum
# Date: 4/9/2021
# File: hangman.py
# Description: This program will allow the user to play a game of hangman. The word is chosen at random from a textfile of 55900 words. The user guesses letters until he either loses (runs out of guesses) or wins

# Hangman Game 

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # For every character of the secret word
    for i in secret_word:
        # If the iterated character does not exist in a list of user guesses
        if i not in letters_guessed:
            return False    
    # Otherwise the word has been guessed
    return True




def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # blank_word: Will contain the user's guessed letters with "_ " subsituted when there's a letter they haven't guessed
    blank_word = ""
    # For every character of the secret word
    for i in secret_word:
        # If the iterated character does not exist in a list of user guesses
        if i not in letters_guessed:
            # Append "_ " to the black_word string
            blank_word += "_ "
        else:
            # Otherwise, append the current iterated letter to blank_word, since it has been guessed
            blank_word += i
    return blank_word

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    
    # Set abc equal to a string containing all the lowercase letters of the alphabet
    abc = string.ascii_lowercase
    # Declare short_abc which will contain all the letters the user hasn't guessed yet
    short_abc = ""
    # For every character in abc
    for i in abc:
        # If the iterated letter hasn't been already guessed by the user
        if i not in letters_guessed:
            # Append the iterated letter to short_abc
            short_abc += i
    return short_abc

def consonant_vowel(new_guess,guesses):
    '''
    new_guess: the user's current guess
    guesses: the current number of remaining guesses
    Will determine whether the guess is a vowel or a consonant, and will subtract the according number of guesses
    returns: The new number of guesses
    '''
    # Declare vowels to be equal to a list of all the vowels
    vowels = ['a','e','i','o','u']
    # If the user's guess is a vowel
    if new_guess in vowels:
        # Subtract 2 guesses
        guesses -= 2
    else:
        # Otherwise, subtract 1 guess
        guesses -= 1
    return guesses

def warning(warnings,new_guess,guesses,reason):
    '''
    warnings: The number of warnings the user has left
    new_guess: A string which is the user's current guess
    guesses: The number of guessses the user has left
    reason: A reason as to why warning() was called
    returns: 
        warnings: The remaining number of warnings
        guesses: The remaing number of guesses
    
    This function is called when the user is required to be warned about something.
    '''

    # Subtract 1 warning
    warnings -= 1
    # If there is only now 1 warning left
    if warnings == 1:
        # Ensure proper grammer by changing "warnings" to "warning"
        w_plural_or_single = "warning"
    # Otherwise
    else:
        # Ensure proper grammer by changing "warning" to "warnings"
        w_plural_or_single = "warnings"    
    # If the user runs out of warnings
    if warnings < 0:
        print("You have no warnings left so you lose one guess: ",end="")
        #=======================================================================
        # if reason == "invalid":
        #     
        # # If the reason is anything but "dup", which is short for "duplicate", and indicates that warning() was called due to multiple guesses of the same letter
        # elif reason != "dup":
        #     # Check if the guess is a vowel or a consonant, and remove the correct number of guesses
        #     guesses = consonant_vowel(new_guess, guesses)
        # # Otherwise, since it was a duplicate letter, the program doesn't care whether it was a vowel or a consonant
        # else:
        #     print("You have 0 warnings left so you lose one guess: ",end="")
        #     # Subtract 1 guess as a penalty for running out of warnings
        #=======================================================================
        guesses -= 1
            
    # Otherwise, if the user hasn't run out of guesses
    else:
        print("You have",warnings,w_plural_or_single,"left: ",end="")
    return warnings,guesses

def get_score(guesses,secret_word):
    '''
    guesses: the number of guesses that were remaining at the end of the game
    secret_word: The word that was chosen by the computer
    returns: total_score, which is the guesses remaining * the number of unique letters in secret_word
    '''
    # Declare no_dup_sec_word (No Duplicate Secret Word) to an empty list, which will fill up with every unique letter of secret_word
    no_dup_sec_word = []
    # For every letter in secret_word
    for i in secret_word:
        # If the current iterated letter doesn't already exist in no_dup_sec_word
        if i not in no_dup_sec_word:
            # Append the current iterated letter to no_dup_sec_word
            no_dup_sec_word.append(i)
    # Set the total score equal to the number of remaining guesses multiplied by the number of unique letters of secret_word
    total_score = guesses * len(no_dup_sec_word)
    return total_score

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    * If the user enters "?", they will be given a chance to guess the word. If they get it wrong, they will lose a guess.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    won = False
    # over will change to True when the game ends
    over = False
    # Set letters_guessed equal to an empty list, which will fill up with the letters that are guessed
    letters_guessed = []
    # Set words_guessed equal to an empty list, which will fill up with the words that are guessed
    words_guessed = []
    
    # Set the user's allowed guesses to 6
    guesses = 6
    # Set the user's warnigns to 3
    warnings = 3
    len_secret_word = len(secret_word)
    # variable that will change to "guess" when there is only one guess left, to maintain the correct usage of singular and plural
    g_plural_or_single = "guesses"
    # variable that will change to "warning" when there is only one warning left, to maintain the correct usage of singular and plural
    w_plural_or_single = "warnings"
    # Welcome the user, maintaining proper grammar
    print("Welcome to the game Hangman!\nI am thinking of a word that is",len_secret_word,"letters long.")
    # Let the user know how many warnings they have left, maintaining proper grammar
    print("You have",warnings,w_plural_or_single,"left.\n-----------")
    # While the variable 'over' is set to False
    while not over:
        # if there is one guess left
        if guesses == 1:
            # Change "guesses" to "guess" to maintain proper grammar
            g_plural_or_single = "guess"
        else:
            # Change "guess" to "guesses" to maintain proper grammar
            g_plural_or_single = "guesses"
        # Tell the user how many guesses are left, maintaining proper grammar
        print("You have",guesses,g_plural_or_single,"left.")
        # Tell the user which letters are still available to guess
        print("Available letters:",get_available_letters(letters_guessed))
        # Ask the user to input their guess
        new_guess = str.lower(input("Please guess a letter: "))
        # If the user entered "?"
        if new_guess == "?":
            # Ask the user to enter their guess for the word, and change the input to lowercase
            word_guess = str.lower(input("Please enter a word: "))
            # If the word has not been guessed already
            if word_guess not in words_guessed: 
                # If the input contains only letters
                if str.isalpha(word_guess):
                    # Add the input to words_guessed 
                    words_guessed.append(word_guess)
                    # If the user's guess matches the secret_word
                    if word_guess == secret_word:
                        won = True
                        # Set over to True so the main loop will end
                        over = True
                    # Otherwise
                    else:
                        print("I'm sorry, that is not the correct word: ", end="")
                        # Subtract 1 guess
                        guesses -= 1
                else:
                    print("Oops! That is not a valid word. ",end="")
                    # Subtract a warning and the correct number of guesses, with warning()
                    warnings,guesses = warning(warnings,new_guess,guesses,"dup")    
            else:
                print("Oops! You've already guessed that word. ",end="")
                # Subtract a warning and the correct number of guesses, with warning()
                warnings,guesses = warning(warnings,new_guess,guesses,"dup")
        else:
            # If the user's guess hasn't been guessed already
            if new_guess not in letters_guessed:
                # If the user's guess was a valid letter and was 1 character long
                if str.isalpha(new_guess) and len(new_guess) == 1:
                    # Add the guess to the list of already guessed letters
                    letters_guessed.append(new_guess)
                    # If the guessed letter exists in the secret word
                    if new_guess in secret_word:
                        print("Good guess: ",end="")
                    else:
                        print("Oops! That letter is not in my word: ",end="")
                        # Check if the guess was a vowel or a consonant, and remove the correct number of guesses
                        guesses = consonant_vowel(new_guess, guesses)
                else:
                    print("Oops! That is not a valid letter. ",end="")
                    # Subtract a warning and the correct number of guesses, with warning()
                    warnings,guesses = warning(warnings,new_guess,guesses,"invalid")
            else:
                print("Oops! You've already guessed that letter. ",end="")
                reason = "dup"
                # Subtract a warning and the correct number of guesses, with warning()
                warnings,guesses = warning(warnings,new_guess,guesses,reason)
        # If the user has guessed the whole word
        if is_word_guessed(secret_word, letters_guessed) == True:
            won = True
            over = True
            print(secret_word)
        # If the user hasn't won
        if not won:
            # Print the secret word with all the letters that haven't been guessed yet replaced with "_ "
            print(get_guessed_word(secret_word,letters_guessed))  
        print("------------")

        # If the user runs out of guesses
        if guesses <= 0:
        
            won = False
            over = True
        # If the user lost the game
    
    if not won:
        print("Sorry, you ran out of guesses. The word was ",secret_word,".",sep="")
    elif won:
        print("Congratulations, you won!\nYour total score for this game is:",get_score(guesses,secret_word))
    return won,guesses
    return won,guesses

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # gap_match is always True until it's False, where it will stay that way until the function runs again
    gap_match = True
    # my_word_no_line will fill up with the correctly guessed characters
    my_word_no_line = ""
    # For the number of characters in my_word
    for i in range(len(my_word)):
        # If the subtring of my_word equal to the current interation of the for loop is not equal to "_"
        if my_word[i] != "_":
            # Append that substring to my_word_no_line
            my_word_no_line += my_word[i]
    # Set repeat_letters equal to a list where every entry is another letter from my_word_no_line
    repeat_letters = list(my_word_no_line)
    # If the length of my_word_no_line is equal to the length of other_word
    if len(my_word_no_line) == len(other_word):
        # For the number of characters in my_word_no_line
        for x in range(len(my_word_no_line)):
            # If the substring of my_word_no_line equal to the current iteration of the for loop is not equal to " "
            if my_word_no_line[x] != " ":
                # If that subtring is not equal to the substring of the substring of other_word equal to the current iteration of the for loop
                if my_word_no_line[x] != other_word[x]:            
                    gap_match = False
            else:
                # If the substring of other_word equal to the current iteration of the for loop already exists in repeat_letters
                if other_word[x] in repeat_letters:
                    gap_match = False
    # Otherwise, if the lengths don't match
    else:           
        gap_match = False
    return gap_match
    



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # For every entry in the list wordlist
    for i in wordlist:
        # If the current iterated word has the possibility of being the secret_word
        if match_with_gaps(my_word, i):
            # Print that current iterated word
            print(i,end=" ")
    return



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    * If the user enters "?", they will be given a chance to guess the word. If they get it wrong, they will lose a guess.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    won = False
    # over will change to True when the game ends
    over = False
    # Set letters_guessed equal to an empty list, which will fill up with the letters that are guessed
    letters_guessed = []
    # Set words_guessed equal to an empty list, which will fill up with the words that are guessed
    words_guessed = []
    
    # Set the user's allowed guesses to 6
    guesses = 6
    # Set the user's warnigns to 3
    warnings = 3
    len_secret_word = len(secret_word)
    # variable that will change to "guess" when there is only one guess left, to maintain the correct usage of singular and plural
    g_plural_or_single = "guesses"
    # variable that will change to "warning" when there is only one warning left, to maintain the correct usage of singular and plural
    w_plural_or_single = "warnings"
    # Welcome the user, maintaining proper grammar
    print("Welcome to the game Hangman!\nI am thinking of a word that is",len_secret_word,"letters long.")
    # Let the user know how many warnings they have left, maintaining proper grammar
    print("You have",warnings,w_plural_or_single,"left.\n-----------")
    # While the variable 'over' is set to False
    while not over:
        # if there is one guess left
        if guesses == 1:
            # Change "guesses" to "guess" to maintain proper grammar
            g_plural_or_single = "guess"
        else:
            # Change "guess" to "guesses" to maintain proper grammar
            g_plural_or_single = "guesses"
        # Tell the user how many guesses are left, maintaining proper grammar
        print("You have",guesses,g_plural_or_single,"left.")
        # Tell the user which letters are still available to guess
        print("Available letters:",get_available_letters(letters_guessed))
        # Ask the user to input their guess
        new_guess = str.lower(input("Please guess a letter: "))
        
        # If the user enters "*"
        if new_guess == "*":
            print("Possible word matches are:",end=" ")
            # Call show_possible_matches which will print all the possible matches
            show_possible_matches(get_guessed_word(secret_word,letters_guessed))
            print("\n")
        # If the user entered "?"
        elif new_guess == "?":
            # Ask the user to enter their guess for the word, and change the input to lowercase
            word_guess = str.lower(input("Please enter a word: "))
            # If the word has not been guessed already
            if word_guess not in words_guessed: 
                # If the input contains only letters
                if str.isalpha(word_guess):
                    # Add the input to words_guessed 
                    words_guessed.append(word_guess)
                    # If the user's guess matches the secret_word
                    if word_guess == secret_word:
                        won = True
                        # Set over to True so the main loop will end
                        over = True
                    # Otherwise
                    else:
                        print("I'm sorry, that is not the correct word: ", end="")
                        # Subtract 1 guess
                        guesses -= 1
                else:
                    print("Oops! That is not a valid word. ",end="")
                    # Subtract a warning and the correct number of guesses, with warning()
                    warnings,guesses = warning(warnings,new_guess,guesses,"dup")    
            else:
                print("Oops! You've already guessed that word. ",end="")
                # Subtract a warning and the correct number of guesses, with warning()
                warnings,guesses = warning(warnings,new_guess,guesses,"dup")
        else:
            # If the user's guess hasn't been guessed already
            if new_guess not in letters_guessed:
                # If the user's guess was a valid letter and was 1 character long
                if str.isalpha(new_guess) and len(new_guess) == 1:
                    # Add the guess to the list of already guessed letters
                    letters_guessed.append(new_guess)
                    # If the guessed letter exists in the secret word
                    if new_guess in secret_word:
                        print("Good guess: ",end="")
                    else:
                        print("Oops! That letter is not in my word: ",end="")
                        # Check if the guess was a vowel or a consonant, and remove the correct number of guesses
                        guesses = consonant_vowel(new_guess, guesses)
                else:
                    print("Oops! That is not a valid letter. ",end="")
                    # Subtract a warning and the correct number of guesses, with warning()
                    warnings,guesses = warning(warnings,new_guess,guesses,"invalid")
            else:
                print("Oops! You've already guessed that letter. ",end="")
                reason = "dup"
                # Subtract a warning and the correct number of guesses, with warning()
                warnings,guesses = warning(warnings,new_guess,guesses,reason)
        # If the user has guessed the whole word
        if is_word_guessed(secret_word, letters_guessed) == True:
            won = True
            over = True
            print(secret_word)
        # If the user hasn't won
        if not won:
            # Print the secret word with all the letters that haven't been guessed yet replaced with "_ "
            print(get_guessed_word(secret_word,letters_guessed)) 
        print("------------")
        # If the user runs out of guesses
        if guesses <= 0:
            won = False
            over = True
            
    # If the user lost the game
    if not won:
        print("Sorry, you ran out of guesses. The word was ",secret_word,".",sep="")
    elif won:
        print("Congratulations, you won!\nYour total score for this game is:",get_score(guesses,secret_word))
    return won,guesses

if __name__ == "__main__":
    # Set secret_word equal to a random word from the wordlist
    secret_word = choose_word(wordlist)
    # Uncomment the next line to cheat:
    #print(secret_word)

    win_or_lose,guesses = hangman_with_hints(secret_word)
    




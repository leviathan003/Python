import random
import string
from wordlist import wordslist

words=wordslist
word = random.choice(words).upper()
lives=len(word)+2
word_letter=set(word)
used_letter=set()
alphabet=set(string.ascii_uppercase)
letter=''

while len(word_letter)>0 and lives > 0:
    word_list = [letter if letter in used_letter else ' _ ' for letter in word]
    print("You have ",lives," lives left!!")
    print("Letters used are: "," ".join(used_letter))
    print('Current Word: '," ".join(word_list))
    
    letter=input("\nEnter a Letter:  ").upper()
    if letter in alphabet-used_letter: 
        used_letter.add(letter)
        if letter in word_letter:
            word_letter.remove(letter)
        else:
            lives-=1
            print("Letter not in Word!!")
    elif letter in used_letter:
        print("Already Used..Try again!!")
    else:
        print("Invalid Character!!")
    
word_list = [letter if letter in used_letter else ' _ ' for letter in word]
print('Current Word: '," ".join(word_list))

if lives==0:
    print("You died! The correct word was: ",word,"\n")
else:
    print("Yay! You got the correct word: "," ".join(word_list),"\n")
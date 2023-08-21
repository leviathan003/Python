import string

def ceasar(text,alphabets,shift):

    def shift_alphabet(alphabet):
        return alphabet[shift:]+alphabet[:shift]
    
    shifted_alphabets=tuple(map(shift_alphabet,alphabets))
    final_alphabet="".join(alphabets)
    final_shifted_alphabets="".join(shifted_alphabets)
    table=str.maketrans(final_alphabet,final_shifted_alphabets)

    return text.translate(table)

plain_text="Text Here !!"
print(ceasar(plain_text,[string.ascii_lowercase,string.ascii_uppercase,string.punctuation],7))
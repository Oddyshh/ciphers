from caesar import CaesarShift
from math import inf
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

cipher = CaesarShift()

class Vigenere:
    def __init__(self, language=None, keyword=None):
        self.language = language
        self.keyword = keyword
        self.key_dict = {}
        self.keyword_letters = {}
        self.spacing_dict = {}
        self.plaintext = ""
        self.ciphertext = ""
        self.letters_dict = {}
        self.decoded_letters_dict = {}
        self.letters = cipher.letters
        self.letters_upper = cipher.letters_upper
        self.freq_dict = cipher.eng_freq_dict
        self.change_dict = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ý': 'Y'}
        self.translation_dict = {}

##################################################
### PREPARE FOR ENCODING, DECODING AND SOLVING ###
##################################################
    
    # REPLACE ALL IRRELEVANT SYMBOLS, NUMBERS AND SPACES #
    def replace(self, text):
        text = text.replace(' ', '').replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(';', '').replace('\'', '').replace('\"', '').replace('(', '').replace(')', '').replace(':', '').replace('-', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('&', '').replace('*', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '')
        return text

    # GET KEYWORD FOR ENCODING OR DECODING #
    def get_keyword(self):
        self.keyword = str(input("Enter keyword: ")).upper()
        return self.keyword

    # GET LENGTH OF KEYWORD FOR ENCODING OR DECODING #
    def get_keylength(self):
        keylength = len(self.keyword)
        return keylength

    # DIVIDE THE TEXT INTO PARTS BASED ON LENGTH OF THE KEYWORD #
    def make_letter_dictionary(self, text, keylength):
        for i in range(keylength):
            letter = "L{0}".format(i+1)
            part = text[i: len(text)+1: keylength]
            self.letters_dict[letter] = part
            self.decoded_letters_dict[letter] = ""
        return self.letters_dict

    # MAKE AN ENCODING DICTIONARY OF THE CORRESPONDING LETTERS BASED ON THE KEYWORD #
    def make_encode_key_dictionary(self, keylength, keyword):
        for i in range(keylength):
            shift = self.letters_upper.index(keyword[i])
            shift_letters = self.letters_upper[shift:] + self.letters_upper[:shift]
            letter = "L{0}".format(i+1)
            self.key_dict[letter] = {key:value for key, value in zip(self.letters, shift_letters)}
        return self.key_dict

    # MAKE A DECODING DICTIONARY OF THE CORRESPONDING LETTERS BASED ON THE KEYWORD #
    def make_decode_key_dictionary(self, keylength, keyword):
        for i in range(keylength):
            shift = self.letters_upper.index(keyword[i])
            shift_letters = self.letters_upper[shift:] + self.letters_upper[:shift]
            letter = "L{0}".format(i+1)
            self.key_dict[letter] = {key:value for key, value in zip(shift_letters, self.letters)}
        return self.key_dict

    # TRANSLATE EVERY LETTERGROUP IN PLAIN TEXT WITH CORRESPONDING SHIFT LETTERS #
    def make_translation(self, translation_dict, letters_dict, text):
        for key, value in letters_dict.items():
            letter = key
            trans_letters = value
        
            translation = trans_letters.maketrans(translation_dict[letter])
            new_letters = trans_letters.translate(translation)
            self.translation_dict[letter] = new_letters
        return self.translation_dict

#########################################
### PREPARE EXTRA ACTIONS FOR SOLVING ###
#########################################

    # REPLACE ACCENTED LETTERS WITH THEIR PLAIN COUNTERPARTS #
    def change_letters_with_accents(self, text, change_dict):
        translation = text.maketrans(change_dict)
        self.ciphertext = text.translate(translation)
        return self.ciphertext 

    # GET LENGTH AND SPACING FOR REPEATED SEQUENCES #
    def get_sequence_length(self):
        sequence_length = int(input("Enter sequence length: "))
        return sequence_length

    def get_sequence_count(self):
        sequence_count = int(input("Enter sequence count: "))
        return sequence_count

    # FIND THE SPACING FOR EACH SEQUENCE FOR EVERY INTANCE IN THE CIPHER TEXT #
    def find_sequence_spacing(self, ciphertext, length, count):
        sequence_spacing = {}
        for sublength in range(length, (len(ciphertext) // count)):
            for i in range(0, len(ciphertext) - sublength):
                sequence = ciphertext[i:i+sublength]
                cnt = ciphertext.count(sequence)
                if cnt >= count and sequence not in sequence_spacing:
                    sequence_spacing[sequence] = cnt
    
        # FIND THE INDEX OF THE SEQUENCES #
        sequence_index = {}
        for key in sequence_spacing.keys():
            indices = []
            for i in range(len(ciphertext)):
                if ciphertext[i:i+len(key)] == key:
                    indices.append(i)
                sequence_index[key] = indices

        # MAKE A LIST OF THE INDEXES #
        index_list = []
        for value in sequence_index.values():
            index_list.append(list(value))

        # MAKE A LIST FOR THE SPACING BETWEEN THE SEQUENCES #
        spacing_list = [[] for list in index_list]
        for i in range(len(index_list)):
            while len(index_list[i]) != 1:
                spacing = index_list[i][-1] - index_list[i][-2]
                index_list[i].pop()
                spacing_list[i].append(spacing)

        # FINDING THE MINIMUM VALUE OF THE SPACINGS #
        min_spaces = []
        for lst in spacing_list:
            min_space = lst
            min = inf
            for i in range(len(min_space)):
                if min_space[i] < min:
                    min = min_space[i]
            min_spaces.append(min)

        return sequence_spacing, min_spaces

    # CREATE A TABLE WITH SEQUENCES, THEIR COUNT AND SPACINGS #
    def create_table(self, min_spaces, sequence_spacing):
        sequences = sequence_spacing.keys()
        spacing_dict = {key:value for key, value in zip(sequences, min_spaces)}

        sequence_table = PrettyTable(['Sequence', 'Repeat Spacing', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'])

        for key, value in spacing_dict.items():
            table_list = ''
            table_list += key
            table_list += ' ; '
            table_list += str(value)
            count = 2
            while count <= 25:
                if value % count == 0:
                    table_list += ' ; x'
                else:
                    table_list += ' ;  '
                count += 1

            table_list = table_list.split(';')
            sequence_table.add_row(table_list)

        print(sequence_table)

    # CHANGE THE LENGTH OR COUNT OF THE REPEATED SEQUENCES IF THERE ARE NO GOOD RESULTS IN TABLE#
    def change_length_count(self):
        change = input("Do you want to change the sequence length or count? Y/N: " ).upper()
        return change

    # ENTER SUSPECTED KEYLENGTH IN ORDER TO START SOLVING #
    def enter_keylength(self):
        keylength = int(input("Enter the suspected length of the key: "))
        if keylength not in range(1000):
            print("Invalid choice. Enter a number.")
            self.enter_keylength()
        return keylength

###########################################################
### PREPARE FOR FREQUENCY ANALYSIS PER CIPHER TEXT PART ###
###########################################################

    # CHOOSE A LETTER TO START FREQUENCY ANALYSIS #
    def choose_letter_to_decode(self):
        choice = input("\nDo you want to choose a letter to decode? Y/N: ").upper()
        return choice   

    def letter_choice(self, keylength):    
        choose_letter = int(input("Choose a letter to decode: "))
        if choose_letter > keylength or choose_letter in self.letters or choose_letter in self.letters_upper:
            print("Invalid choice. Try again.")
            self.choose_letter_to_decode(keylength)
                
        return choose_letter

    # DIVIDE THE CIPHER TEXT INTO PARTS BASED ON KEY LENGTH AND RETURN THE PART FOR SELECTED LETTER #
    def get_cipher_part(self, letter, letters_dict):
        for key in letters_dict.keys():
                key = "L" + str(letter)
                cipher_part = letters_dict[key]

        return cipher_part

#####################################################################
### UPDATING RELEVANT DICTIONARIES AFTER SOLVING SELECTED LETTERS ###
#####################################################################

    # UPDATE THE DICTIONARY WITH PARTS THAT HAVE BEEN SOLVED FOR SELECTED LETTER #
    def update_decoded_dict(self, plain_part, choose_letter):
        letter = "L" + str(choose_letter)
        self.decoded_letters_dict[letter] = plain_part

        return self.decoded_letters_dict

    # UPDATE KEYWORD WHEN A LETTER IS SOLVED #
    def update_keyword_letters(self, letter_choice, shift):
        letter = "L" + str(letter_choice)
        self.keyword_letters[letter] = self.letters_upper[shift]

        return self.keyword_letters

#################################################
### FINAL STEPS OF REARRANGING SOLVED LETTERS ###
#################################################

    # MAKE A LIST OF ALL THE TRANSLATED LETTERS PER KEYWORD LETTER #
    def get_letter_list(self, translation_dict):
        letters = []
        for value in translation_dict.values():
            letters.append(list(value))
        return letters

    # GET CIPHER TEXT BY ADDING LETTERS TO TEXT AND REMOVING THEM FROM THE LIST #
    def get_new_text(self, letter_list):
        new_text = ""
        for i in range(len(letter_list)):
            while len(letter_list[i]) > 0:
                for i in range(len(letter_list)):
                    try:
                        new_text += letter_list[i].pop(0)
                    except IndexError:
                        new_text += ""
        #print(ciphertext)
        return new_text

#############################################
### PRINTING RESULTS IN A READABLE FORMAT ###
#############################################

    # PRINT KEYWORD AFTER SOLVING THE CODE #
    def solved_keyword(self, keyword_letters):
        keyword = ""
        for value in keyword_letters.values():
            keyword += value
        
        return keyword.upper()

    # PRINT THE ENCODED RESULTS IN A READABLE FORMAT #
    def print_encode_results(self, keyword, plaintext, ciphertext):
        print("\n===========================================================")
        print("\nThe plain text was: \n")
        print(plaintext)
        print("\n===========================================================")
        print("\nThe cipher text is: \n")
        print(ciphertext)
        print("\n===========================================================")
        print("\nThe keyword was: " + keyword)
        print("\n===========================================================\n")

    # PRINT THE DECODED AND SOLVED RESULTS IN A READABLE FORMAT #
    def print_decode_results(self, keyword, plaintext, ciphertext):
        print("\n===========================================================")
        print("\nThe cipher text was: \n")
        print(ciphertext)
        print("\n===========================================================")
        print("\nThe plain text is: \n")
        print(plaintext)
        print("\n===========================================================")
        print("\nThe keyword was: " + keyword)
        print("\n===========================================================\n")

#########################################################################
### ENCODER, DECODER AND SOLVER METHODS TO ACTUALLY DO THE COOL PARTS ###
#########################################################################

    # ENCODE PLAIN TEXT BASED ON A KEYWORD INTO CIPHER TEXT TO KEEP YOUR SECRETS EVEN MORE SAFE #
    def encoder(self, plaintext=None, keyword=None):

        # GET PLAIN TEXT IF NONE IS KNOWN YET #
        if plaintext == None:
            self.plaintext = cipher.get_plaintext()
        else:
            self.plaintext = plaintext.lower()

        # GET KEYWORD IF NONE IS KNOWN YET #
        if keyword == None:
            self.keyword = self.get_keyword()
        else:
            self.keyword = keyword.upper()

        # PERFORM NECESSARY ACTIONS TO GET THE TRANSLATION #
        self.plaintext = self.replace(self.plaintext)
        keylength = self.get_keylength()
        letters_dict = self.make_letter_dictionary(self.plaintext, keylength)
        key_dict = self.make_encode_key_dictionary(keylength, self.keyword)
        trans_dict = self.make_translation(key_dict, letters_dict, self.plaintext)
        letters_list = self.get_letter_list(trans_dict)
        self.ciphertext = self.get_new_text(letters_list)

        # PRINTING THE RESULTS #
        self.print_encode_results(self.keyword, self.plaintext, self.ciphertext.upper())

        # ASK USER TO TRY AGAIN #
        self.again()

    # DECODE CIPHER TEXT INTO PLAIN TEXT BASED ON A KNOWN KEYWORD IN ORDER TO READ THE SECRET MESSAGE! #
    def decoder(self, ciphertext=None, keyword=None):
        
        # GET CIPHER TEXT IF NONE IS KNOWN YET #
        if ciphertext == None:
            self.ciphertext = cipher.get_ciphertext()
        else:
            self.ciphertext = ciphertext.upper()

        # GET KEYWORD IF NONE IS KNOWN YET #
        if keyword == None:
            self.keyword = self.get_keyword()
        else:
            self.keyword = keyword.upper()

        # PERFORM NECESSARY ACTIONS TO GET THE TRANSLATION #
        self.ciphertext = self.replace(self.ciphertext)
        keylength = self.get_keylength()
        letters_dict = self.make_letter_dictionary(self.ciphertext, keylength)
        key_dict = self.make_decode_key_dictionary(keylength, self.keyword)
        trans_dict = self.make_translation(key_dict, letters_dict, self.ciphertext)
        letters_list = self.get_letter_list(trans_dict)
        self.plaintext = self.get_new_text(letters_list)

        # PRINTING THE RESULTS #
        self.print_decode_results(self.keyword, self.plaintext.lower(), self.ciphertext)

        # ASK USER TO TRY AGAIN #
        self.again()

    # CRACK SOMEBODY ELSE'S SECRET MESSAGES WITHOUT KNOWING THE KEYWORD #
    def solver(self, ciphertext=None):
        
        # GET CIPHER TEXT IF NONE IS KNOWN YET #
        if ciphertext == None:
            self.ciphertext = cipher.get_ciphertext()
        else:
            self.ciphertext = ciphertext.upper()

        # MAKE TEXT READY FOR PROCESSING #
        self.ciphertext = self.replace(self.ciphertext)
        self.ciphertext = self.change_letters_with_accents(self.ciphertext, self.change_dict)
        
        # GIVE USER CHANCE TO CHANGE LENGTH AND COUNT IN CASE SEQUENCE TABLE DOESN'T HAVE USEFUL RESULTS #
        change = self.change_length_count()
        while change == "Y":
            sequence_length = self.get_sequence_length()
            sequence_count = self.get_sequence_count()
            sequence_spacing, min_spaces = self.find_sequence_spacing(self.ciphertext, sequence_length, sequence_count)
            self.create_table(min_spaces, sequence_spacing)
            change = self.change_length_count()
        
        # ENTER KEY LENGTH, MAKE DICTIONARY OF LETTERS AND THEIR CORRESPONDING PARTS OF THE CIPHER TEXT #
        keylength = self.enter_keylength()
        letters_dict = self.make_letter_dictionary(self.ciphertext, keylength)
        
        # MAKE SURE USER IS ABLE TO CHOOSE ANOTHER LETTER AFTER SOLVING CURRENT LETTER #
        choose_letter = self.choose_letter_to_decode()
        while choose_letter == "Y":
            letter_choice = self.letter_choice(keylength)
            cipher_part = self.get_cipher_part(letter_choice, letters_dict)

            # USE METHODS FROM CAESAR SHIFT TO DO A FREQUENCY ANALYSIS #
            count_dict = cipher.count_letters(cipher_part)
            code_freq_dict = cipher.find_frequency_per_letter(count_dict)
            letters, freqs, code_letters, code_freqs = cipher.make_freq_lists(self.freq_dict, code_freq_dict)
            cipher.plot_bar_chart(letters, freqs, code_letters, code_freqs)

            # USE METHODS FROM CAESAR SHIFT IN ORDER TO SHIFT THE ALPHABET AND CONVERT CIPHER TEXT TO PLAIN TEXT FOR THE SOLVED PART OF THE SELECTED LETTER #
            shift = cipher.get_shift()
            shift_upper = cipher.shift_alphabet_upper(shift)
            translation_dict = cipher.make_decoder_dict(shift_upper)
            translation = cipher.make_translation(translation_dict, cipher_part)

            # UPDATE RELEVANT DICTIONARIES AND PRINT PROGRESS #
            self.update_decoded_dict(translation, letter_choice)
            keyword_letters = self.update_keyword_letters(letter_choice, shift)
            print("\n", self.decoded_letters_dict, "\n")
            print("KEYWORD = ", keyword_letters, "\n")

            choose_letter = self.choose_letter_to_decode()

        # FINAL STEPS OF REARRANGING THE SOLVED LETTERS INTO READABLE TEXT #
        letters_list = self.get_letter_list(self.decoded_letters_dict)
        self.plaintext = self.get_new_text(letters_list) 

        # PRINTING THE RESULTS #
        self.print_decode_results(self.solved_keyword(keyword_letters), self.plaintext.lower(), self.ciphertext)
        
        # ASK USER TO TRY AGAIN #
        self.again()



##################################################################################################
### CHOOSE AN ACTION TO PERFORM: ENCODE, DECODE OR SOLVE AND OPTION TO TRY AGAIN WHEN FINISHED ###
##################################################################################################

    # CHOOSE ACTION TO PERFORM #
    def choice(self):
        choice = input("\nWhat do you want to do?\n\n1.Encode \n2.Decode \n3.Solve \n\nEnter 1, 2 or 3: ")
        if choice == "1":
            self.encoder()
        elif choice == "2":
            self.decoder()
        elif choice == "3":
            self.solver()
        else:
            print("\nInvalid input. Try again!\n")
            choice = self.choice()

    # GIVE OPTION TO TRY AGAIN #
    def again(self):
        again = input("Do you want to try again? Y/N: ").upper()
        if again == "Y":
            self.choice()
        elif again == "N":
            print("\nOK, goodbye!")
        else:
            print("\nInvalid choice. Try again!")
            self.again()    
        

vigenere = Vigenere()
print(vigenere.choice())


        




    





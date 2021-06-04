import matplotlib.pyplot as plt
import numpy as np

class CaesarShift:
    def __init__(self, language=None):
        self.language = language
        self.plaintext = ""
        self.ciphertext = ""
        self.shift = 0
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.letters_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.freq_dict = {}
        self.eng_freq_dict = {'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.2, 'k': 0.8, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.1, 'r': 6.0, 's': 6.3, 't': 9.1, 'u': 2.8, 'v': 1.0, 'w': 2.4, 'x': 0.2, 'y': 2.0, 'z': 0.1, 'aa': 8.2, 'bb': 1.5, 'cc': 2.8, 'dd': 4.3, 'ee': 12.7, 'ff': 2.2, 'gg': 2.0, 'hh': 6.1, 'ii': 7.0, 'jj': 0.2, 'kk': 0.8, 'll': 4.0, 'mm': 2.4, 'nn': 6.7, 'oo': 7.5, 'pp': 1.9, 'qq': 0.1, 'rr': 6.0, 'ss': 6.3, 'tt': 9.1, 'uu': 2.8, 'vv': 1.0, 'ww': 2.4, 'xx': 0.2, 'yy': 2.0, 'zz': 0.1}
        self.dutch_freq_dict = {'a': 7.49, 'b': 1.58, 'c': 1.24, 'd': 5.93, 'e': 18.91, 'f': 0.81, 'g': 3.40, 'h': 2.38, 'i': 6.50, 'j': 1.46, 'k': 2.25, 'l': 3.57, 'm': 2.21, 'n': 10.03, 'o': 6.06, 'p': 1.57, 'q': 0.009, 'r': 6.41, 's': 3.73, 't': 6.79, 'u': 1.99, 'v': 2.85, 'w': 1.52, 'x': 0.04, 'y': 0.035, 'z': 1.39, 'aa': 7.49, 'bb': 1.58, 'cc': 1.24, 'dd': 5.93, 'ee': 18.91, 'ff': 0.81, 'gg': 3.40, 'hh': 2.38, 'ii': 6.50, 'jj': 1.46, 'kk': 2.25, 'll': 3.57, 'mm': 2.21, 'nn': 10.03, 'oo': 6.06, 'pp': 1.57, 'qq': 0.009, 'rr': 6.41, 'ss': 3.73, 'tt': 6.79, 'uu': 1.99, 'vv': 2.85, 'ww': 1.52, 'xx': 0.04, 'yy': 0.035, 'zz': 1.39}
        self.translation_dict = {}

##################################################
### PREPARE FOR ENCODING, DECODING AND SOLVING ###
##################################################

    # SET LANGUAGE TO ENGLISH OR DUTCH #
    def set_language(self):
        if self.language == "EN":
            self.freq_dict = self.eng_freq_dict
        if self.language == "DU":
            self.freq_dict = self.dutch_freq_dict
        if self.language == None:
            self.language = input("\nType \"EN\" for English or \"DU\" for Dutch: ").upper()
            self.set_language()

    # ENTER THE CIPHER TEXT FOR DECODING OR SOLVING #
    def get_ciphertext(self):
        self.ciphertext = input("\nEnter the ciphertext: \n")
        return self.ciphertext.upper()

    # ENTER THE PLAIN TEXT TO ENCODE #
    def get_plaintext(self):
        self.plaintext = input("\nEnter the plaintext: \n")
        return self.plaintext.lower()

    # ENTER THE NUMBER TO DETERMINE HOW MANY SPACES THE ALPHABET SHOULD BE SHIFTED #
    def get_shift(self):
        self.shift = int(input("\nWhat shift has been used / do you want to use?: "))
        if self.shift > 25 or self.shift < -25:
            print("Cannot shift more than 25 times. Try again!")
            self.get_shift()
        return self.shift

    # SHIFT THE ALPHABET THE SPECIFIED AMOUNT OF SPACES FOR ENCODING #
    def shift_alphabet(self, shift):
        shift_alphabet = self.letters[shift:] + self.letters[:shift]
        return shift_alphabet

    # SHIFT THE ALPHABET THE SPECIFIED AMOUNT OF SPACES FOR DECODING #
    def shift_alphabet_upper(self, shift):
        shift_alphabet = self.letters_upper[shift:] + self.letters_upper[:shift]
        return shift_alphabet

    # MAKE A TRANSLATION DICTIONARY TO CHANGE PLAIN LETTERS TO CORRESPONDING CIPHER LETTERS #
    def make_encoder_dict(self, shift):
        shift_alphabet = self.shift_alphabet(shift)

        for i in range(len(self.letters)):
            for i in range(len(shift_alphabet)):
                self.translation_dict[self.letters[i]] = shift_alphabet[i]
        return self.translation_dict

    # MAKE A TRANSLATION DICTIONARY TO CHANGE CIPHER LETTERS TO CORRESPONDING PLAIN LETTERS #
    def make_decoder_dict(self, shift_alphabet):

        for i in range(len(shift_alphabet)):
            for i in range(len(self.letters)):
                self.translation_dict[shift_alphabet[i]] = self.letters[i]
        return self.translation_dict

    # TRANSLATE THE PLAIN LETTERS TO CIPHER LETTERS AND VICE VERSA #
    def make_translation(self, translation_dict, text):
        trans = text.maketrans(translation_dict)
        translation = text.translate(trans)
        return translation

###########################################################
### PREPARE FOR FREQUENCY ANALYSIS PER CIPHER TEXT PART ###
###########################################################

    # COUNT HOW MANY TIMES A LETTER APPEARS IN THE CIPHER TEXT #
    def count_letters(self, text):
        code_letter_count = {}
        for i in range(len(self.letters_upper)):
            count = text.count(self.letters_upper[i])
            code_letter_count[self.letters_upper[i]] = count
        return code_letter_count

    # CALCULATE FREQUENCY PER LETTER IN THE CIPHER TEXT #
    def find_frequency_per_letter(self, count_dict):
        code_freq_dict = {}
        total = 0
        for letter, count in count_dict.items():
            total += count
        for letter, count in count_dict.items():
            frequency = round((count / total) * 100, 1)
            code_freq_dict[letter] = frequency
        return code_freq_dict

    # PREPARING LISTS FOR FREQUENCY ANALYSIS #
    def make_freq_lists(self, freq_dict, code_freq_dict):
        letters = []
        freqs = []
        for key, value in freq_dict.items():
            letters.append(key)
            freqs.append(value)

        code_letters1 = []
        code_freqs1 = []
        for key, value in code_freq_dict.items():
            code_letters1.append(key)
            code_freqs1.append(value)

        code_letters2 = []
        code_freqs2 = []
        for key, value in code_freq_dict.items():
            code_letters2.append(key+key)
            code_freqs2.append(value)

        code_letters = code_letters1 + code_letters2
        code_freqs = code_freqs1 + code_freqs2

        return letters, freqs, code_letters, code_freqs

    # PLOTTING THE BAR CHARTS FOR FREQUENCY ANALYSIS #
    def plot_bar_chart(self, letters, freqs, code_letters, code_freqs):
        plt.subplots(2)
        plt.subplot(2,1,1)
        plt.bar(letters, freqs)
        plt.xlabel('', fontsize= 10)
        plt.title("English Frequencies")

        plt.subplot(2,1,2)
        index = np.arange(len(code_letters))
        ax1 = plt.gca()
        ax1.bar(code_letters, code_freqs)
        ax1.set_xticks(code_letters)
        ax1.set_xticklabels(code_letters, fontsize= 10)
        ax2 = ax1.twiny()
        ax2.set_xticks(range(len(code_letters)))
        ax2.set_xticklabels(index, fontsize= 10)
        ax2.set_xlim(ax1.get_xlim())
        plt.title("Code Frequencies")

        plt.show()

#############################################
### PRINTING RESULTS IN A READABLE FORMAT ###
#############################################

    # PRINT THE ENCODED RESULTS IN A READABLE FORMAT #
    def print_encode_results(self, shift, plaintext, ciphertext):
        print("\n===========================================================")
        print("\nThe plain text was: \n")
        print(plaintext)
        print("\n===========================================================")
        print("\nThe cipher text is: \n")
        print(ciphertext)
        print("\n===========================================================")
        print("\nThe shift was: " + str(shift))
        print("\n===========================================================\n")

    # PRINT THE DECODED AND SOLVED RESULTS IN A READABLE FORMAT #
    def print_decode_results(self, shift, plaintext, ciphertext):
        print("\n===========================================================")
        print("\nThe cipher text was: \n")
        print(ciphertext)
        print("\n===========================================================")
        print("\nThe plain text is: \n")
        print(plaintext)
        print("\n===========================================================")
        print("\nThe shift was: " + str(shift))
        print("\n===========================================================\n")


#########################################################################
### ENCODER, DECODER AND SOLVER METHODS TO ACTUALLY DO THE COOL PARTS ###
#########################################################################

    # ENCODE PLAIN TEXT INTO CIPHER TEXT TO KEEP YOUR SECRETS SAFE! #
    def encoder(self, plaintext=None, shift=None):
        
        # GET PLAIN TEXT IF NONE IS KNOWN YET #
        if plaintext == None:
            self.plaintext = self.get_plaintext()
        else:
            self.plaintext = plaintext.lower()

        # GET SHIFT IF NONE IS KNOWN YET #
        if shift == None:
            self.shift = self.get_shift()
        else:
            self.shift = int(shift)

        # PERFORM NECESSARY ACTIONS TO ENCODE THE PLAIN TEXT #

        self.shift_alphabet(self.shift)
        translation_dict = self.make_encoder_dict(self.shift)
        self.ciphertext = self.make_translation(translation_dict, self.plaintext)

        # PRINTING THE RESULTS #
        self.print_encode_results(self.shift, self.plaintext, self.ciphertext.upper())
        
        # ASK USER TO TRY AGAIN #
        self.again()

        return self.ciphertext.upper()

    # DECODE CIPHER TEXT INTO PLAIN TEXT IN ORDER TO READ THE SECRET MESSAGE! #
    def decoder(self, ciphertext=None, shift=None):
        
        # GET CIPHER TEXT IF NONE IS KNOWN YET #
        if ciphertext == None:
            self.ciphertext = self.get_ciphertext()
        else:
            self.ciphertext = ciphertext.upper()

        # GET SHIFT IF NONE IS KNOWN YET #
        if shift == None:
            self.shift = self.get_shift()
        else:
            self.shift = int(shift)

        # PERFORM NECESSARY ACTIONS TO DECODE THE CIPHER TEXT #
        shift_alphabet = self.shift_alphabet_upper(self.shift)
        translation_dict = self.make_decoder_dict(shift_alphabet)
        self.plaintext = self.make_translation(translation_dict, self.ciphertext)

        # PRINTING THE RESULTS #
        self.print_decode_results(self.shift, self.plaintext.lower(), self.ciphertext)
        
        # ASK USER TO TRY AGAIN #
        self.again()

        return self.plaintext.lower()

    # CRACK SOMEBODY ELSE'S SECRET MESSAGES #
    def solver(self, ciphertext=None):
        
        # SET THE LANGUAGE TO EITHER DUTCH OR ENGLISH #
        self.language = self.set_language()

        # GET CIPHER TEXT IF NONE IS KNOWN YET #
        if ciphertext == None:
            self.ciphertext = self.get_ciphertext()
        else:
            self.ciphertext = ciphertext.upper()

        # PERFORM ACTIONS NECESSARY FOR FREQUENCY ANALYSIS #
        count_dict = self.count_letters(self.ciphertext)
        code_freq_dict = self.find_frequency_per_letter(count_dict)
        letters, freqs, code_letters, code_freqs = self.make_freq_lists(self.freq_dict, code_freq_dict)
        self.plot_bar_chart(letters, freqs,  code_letters, code_freqs)

        # USE DECODER TO SOLVE THE CODE #
        self.plaintext = self.decoder(self.ciphertext)

        return self.plaintext.lower()

##################################################################################################
### CHOOSE AN ACTION TO PERFORM: ENCODE, DECODE OR SOLVE AND OPTION TO TRY AGAIN WHEN FINISHED ###
##################################################################################################

    def choice(self):
        choice = int(input("\nWhat do you want to do?\n\n1.Encode \n2.Decode \n3.Solve \n\nEnter 1, 2 or 3: "))
        if choice == 1:
            self.encoder()
        elif choice == 2:
            self.decoder()
        elif choice == 3:
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


#caesar = CaesarShift()
#caesar.choice()


from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import movie_reviews
from nltk.tokenize import PunktSentenceTokenizer
import os
import nltk

print("Wanna work with new text or movie reviews?")
print("\n\n\n\n1) Press 1 for new text")
print("2) Press 2 for movie reviews")

s = input()
count = 0
os.system('cls')

if s== '1':
    print("Enter text")
    text = input()

elif s == '2':
    print ("Choose polarity from the following:\n\n\n")
    print ("Press 1 for positive movie reviews")
    print ("Press 2 for negative movie reviews")

    polarity = input()

    if polarity == '1':
        for i in movie_reviews.fileids('pos'):
            print(i)
            count = count + 1
            if count%20 == 0:
                print ('\n\nTo load more press Space and Enter else just press Enter')
                loading = input()
                if loading == ' ':
                    os.system('cls')
                    continue
                else:
                    break
        print()
    elif polarity == '2':
        for i in movie_reviews.fileids('neg'):
            print (i)
            count = count + 1
            if count%20 == 0:
                print ('\n\nTo load more press Space and Enter else just press Enter')
                loading = input()
                if loading == ' ':
                    os.system('cls')
                    continue
                else:
                    break
        print()

    print ("Enter a file name from above")
    file_name = input()

    text = movie_reviews.raw(file_name)

    training = movie_reviews.raw("neg/cv018_21672.txt")
    
    custom_tokenizer = PunktSentenceTokenizer(training) 

count = 0
for i in custom_tokenizer.tokenize(text):
    count = count + 1
    print (count,') ',i)

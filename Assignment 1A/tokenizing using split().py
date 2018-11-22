from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import movie_reviews
import re,os,nltk


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

    
count = 0


for i in sent_tokenize(text):
    count = count + 1
    print (count,') ',i)

print ("Enter sentence number for further analysis.")

sent_no = int(input())

sent = sent_tokenize(text)[sent_no-1]

os.system('cls')
print ("Tokenizing words using split()")

for i in sent.split():
    print (i)

input("press enter")
print ("Tokenizing words using split(')")

for i in sent.split():
    for j in i.split("'"):
        print(j)

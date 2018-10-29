from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import movie_reviews
import re
import os
import nltk

print("Wanna work with new text or movie reviews?")
print("\n\n\n\n1) Press 1 for new text")
print("2) Press 2 for movie reviews")


def isItJustANumberOrADate(gotNumber,words):
    no=1
    date = 0
    num = 0
    number = int(gotNumber)
    while(True):
        if number+2 >= len(words):
            break;
        if (words[number+no][1:] == "anuary") or (words[number+no][1:] == "ebruary") or (words[number+no][1:] == "arch") or (words[number+no][1:] == "pril") or (words[number+no][1:] == "ay") or (words[number+no][1:] == "une") or (words[number+no][1:] == "uly") or (words[number+no][1:] == "ugust") or (words[number+no][1:] == "eptember") or (words[number+no][1:] == "ctober") or (words[number+no][1:] == "ovember") or (words[number+no][1:] == "ecember"):
            no= no+1
            date = date+1
        elif (words[number+no][1:] == "undred") or (words[number+no][1:] == "housand") or (words[number+no][1:] == "illion"):
            no= no +1
        else:
            break;
        

    while(no>0):
        no= no - 1
        print(words[number]," ",end = "")
        number= number + 1
    
    if date == 1:
        print("\t\t\tDATE")
    else:
        print("\t\t\tNUMBER")
    return number-1;


def isItAnEntity(gotNumber,words):
    number = int(gotNumber)
    word = nltk.word_tokenize(words[number])
    tag = nltk.pos_tag(word)
    if (tag[0][1] == "NNP") or (tag[0][1] == "NN"):
        print(tag[0][0],"\t\t\tEntity")


s = input()
count = 0
os.system('cls')

if s== '1':
    print("\n\nEnter text")
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

print ("\n\n\nEnter sentence number for further analysis.")

sent_no = int(input())

sent = sent_tokenize(text)[sent_no-1]

os.system('cls')

word_list = word_tokenize(sent)

Cap_word = re.compile(r"[A-Z]")
i=0
while(True):
    if(word_list[i].isdigit()):
        number = isItJustANumberOrADate(i,word_list)
        while word_list[number] != word_list[i]:
            i = i + 1
    elif(Cap_word.match(word_list[i][0])):
        isItAnEntity(i,word_list)
    i = i + 1
    if i >= len(word_list):
        break;


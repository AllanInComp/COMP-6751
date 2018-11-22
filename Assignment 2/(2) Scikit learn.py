from nltk.corpus import rte
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
import xml.etree.ElementTree as ET
import nltk
from nltk.stem.lancaster import LancasterStemmer
lancaster_stemmer = LancasterStemmer()
from nltk.corpus import stopwords 


print("Enter preferred training set from\n1) rte1_dev.xml\n2) rte2_dev.xml\n3) rte3_dev.xml")
s = input()

trainTree = ET.parse(s)
trainRoot = trainTree.getroot()

print("Enter preferred testing set from\n1) rte1_test.xml\n2) rte2_test.xml\n3) rte3_test.xml\n4) challengeTest1.xml\n5) challengeTest2.xml")
t = input()
print('\n\n')

testTree = ET.parse(t)
testRoot = testTree.getroot()


def get_features_basic(post):
     features = {}
     for b in post:
          if b.tag == 't':
               #print(word)
               for word in nltk.word_tokenize(b.text):
                    features['contains({})'.format(word.lower())] = 'statement'
          else:
               for word in nltk.word_tokenize(b.text):
                    features['contains({})'.format(word.lower())] = 'inference'  
     return features



def get_features_lemma(post):
     features = {}
     for b in post:
          if b.tag == 't':
               for word in nltk.word_tokenize(b.text):
                    #print(word)
                    w = lancaster_stemmer.stem(word)
                    features['contains({})'.format(w.lower())] = 'statement'
          else:
               for word in nltk.word_tokenize(b.text):
                    w = lancaster_stemmer.stem(word)
                    features['contains({})'.format(w.lower())] = 'inference'
  
     return features



def get_features_lemma_pos(post):
     features = {}
     for b in post:
          s = nltk.pos_tag(nltk.word_tokenize(b.text))
          if b.tag == 't':
               i = 0
               for word in nltk.word_tokenize(b.text):
                    w = lancaster_stemmer.stem(word)
                    features['{}'.format(w.lower()),'{}'.format(s[i][1])] = 'statement'
                    i = i + 1
          else:
               j = 0
               for word in nltk.word_tokenize(b.text):
                    w = lancaster_stemmer.stem(word)
                    features['{}'.format(w.lower()),'{}'.format(s[j][1])] = 'inference'
                    j = j + 1
     return features


stop_words = set(stopwords.words('english'))

def get_features_lemma_pos_stopwords(post):
     features = {}
     for b in post:
          word_tokens = nltk.word_tokenize(b.text)
          filtered_sentence = [w for w in word_tokens if not w in stop_words]
          s = nltk.pos_tag(filtered_sentence)
          if b.tag == 't':
               i = 0
               for word in s:
                    w = lancaster_stemmer.stem(word[0])
                    features['{}'.format(w.lower()),'{}'.format(word[1])] = 'statement'
                    i = i + 1
          else:
               j = 0
               for word in s:
                    w = lancaster_stemmer.stem(word[0])
                    features['{}'.format(w.lower()),'{}'.format(word[1])] = 'inference'
                    j = j + 1
     return features

def get_features_lemma_pos_stopwords_ner(post):
     features = {}
     word_tokens = []
     filtered_sentence = []
     s = []
     chunk = []
     for b in post:
          word_tokens = nltk.word_tokenize(b.text)
          filtered_sentence = [w for w in word_tokens if not w in stop_words]
          s = nltk.pos_tag(filtered_sentence)
          chunk = nltk.ne_chunk(s)
          if b.tag == 't':
               for word in chunk:
                    if(hasattr(word,'label')):
                         isNER = word.label()
                         w = lancaster_stemmer.stem(word[0][0])
                         features['{}'.format(w.lower()),'{}'.format(word[0][1]),'{}'.format(isNER)] = 'statement'
                    else:
                         isNER = False
                         w = lancaster_stemmer.stem(word[0])
                         features['{}'.format(w.lower()),'{}'.format(word[1]),'{}'.format(isNER)] = 'statement'
          else:
               for word in chunk:
                    if(hasattr(word,'label')):
                         isNER = word.label()
                         w = lancaster_stemmer.stem(word[0][0])
                         features['{}'.format(w.lower()),'{}'.format(word[0][1]),'{}'.format(isNER)] = 'inference'
                    else:
                         isNER = False
                         w = lancaster_stemmer.stem(word[0])                         
                         features['{}'.format(w.lower()),'{}'.format(word[1]),'{}'.format(isNER)] = 'inference'
     return features


trainFeaturesets0 = [(get_features_basic(post), post.get('value')) for post in trainRoot]
testFeaturesets0 = [(get_features_basic(post), post.get('value')) for post in testRoot]

classifier0 = SklearnClassifier(BernoulliNB()).train(trainFeaturesets0)

actual = [t[1] for t in testFeaturesets0]
prediction = classifier0.classify_many([fs for (fs, l) in testFeaturesets0])

result = zip(actual,prediction)
truePositive = 0
falseNegative = 0
falsePositive = 0
trueNegative = 0

for a in result:
     if a[0] == 'TRUE':
          if a[1] == 'TRUE':
               truePositive = truePositive + 1
          else:
               falseNegative = falseNegative + 1
     else:
          if a[1] == 'TRUE':
               falsePositive = falsePositive + 1
          else:
               trueNegative = trueNegative + 1

precision = truePositive/(truePositive + falsePositive)
recall = truePositive/(truePositive + falseNegative)

print('Precision for basic pipeline ----> ', precision)
print('Recall for basic pipeline ---> ', recall)
print('F-score for basic pipeline ---> ', 2*precision*recall/(precision+recall))
print('Accuracy for basic pipeline --->', (truePositive + trueNegative)/len(actual))
print('\n\n\n')


trainFeaturesets1 = [(get_features_lemma(post), post.get('value')) for post in trainRoot]
testFeaturesets1 = [(get_features_lemma(post), post.get('value')) for post in testRoot]

classifier1 = SklearnClassifier(BernoulliNB()).train(trainFeaturesets1)

actual1 = [t[1] for t in testFeaturesets1]
prediction1 = classifier1.classify_many([fs for (fs, l) in testFeaturesets1])

result1 = zip(actual1,prediction1)
truePositive = 0
falseNegative = 0
falsePositive = 0
trueNegative = 0

for a in result1:
     if a[0] == 'TRUE':
          if a[1] == 'TRUE':
               truePositive = truePositive + 1
          else:
               falseNegative = falseNegative + 1
     else:
          if a[1] == 'TRUE':
               falsePositive = falsePositive + 1
          else:
               trueNegative = trueNegative + 1

precision1 = truePositive/(truePositive + falsePositive)
recall1 = truePositive/(truePositive + falseNegative)

print('Precision for pipeline with stemming ----> ', precision1)
print('Recall for pipeline with stemming ---> ', recall1)
print('F-score for pipeline with stemming ---> ', 2*precision1*recall1/(precision1+recall1))
print('Accuracy for pipeline with stemming --->', (truePositive + trueNegative)/len(actual1))
print('\n\n\n')




trainFeaturesets2 = [(get_features_lemma_pos(post), post.get('value')) for post in trainRoot]
testFeaturesets2 = [(get_features_lemma_pos(post), post.get('value')) for post in testRoot]

classifier2 = SklearnClassifier(BernoulliNB()).train(trainFeaturesets2)

actual2 = [t[1] for t in testFeaturesets2]
prediction2 = classifier2.classify_many([fs for (fs, l) in testFeaturesets2])

result2 = zip(actual2,prediction2)
truePositive = 0
falseNegative = 0
falsePositive = 0
trueNegative = 0

for a in result2:
     if a[0] == 'TRUE':
          if a[1] == 'TRUE':
               truePositive = truePositive + 1
          else:
               falseNegative = falseNegative + 1
     else:
          if a[1] == 'TRUE':
               falsePositive = falsePositive + 1
          else:
               trueNegative = trueNegative + 1

precision2 = truePositive/(truePositive + falsePositive)
recall2 = truePositive/(truePositive + falseNegative)

print('Precision for pipeline including POS tagging ----> ', precision2)
print('Recall for pipeline including and POS tagging ---> ', recall2)
print('F-score for pipeline including POS tagging ---> ', 2*precision2*recall2/(precision2+recall2))
print('Accuracy for pipeline including POS tagging --->', (truePositive + trueNegative)/len(actual2))
print('\n\n\n')




trainFeaturesets3 = [(get_features_lemma_pos_stopwords(post), post.get('value')) for post in trainRoot]
testFeaturesets3 = [(get_features_lemma_pos_stopwords(post), post.get('value')) for post in testRoot]

classifier3 = SklearnClassifier(BernoulliNB()).train(trainFeaturesets3)

actual3 = [t[1] for t in testFeaturesets3]
prediction3 = classifier3.classify_many([fs for (fs, l) in testFeaturesets3])

result3 = zip(actual3,prediction3)
truePositive = 0
falseNegative = 0
falsePositive = 0
trueNegative = 0

for a in result3:
     if a[0] == 'TRUE':
          if a[1] == 'TRUE':
               truePositive = truePositive + 1
          else:
               falseNegative = falseNegative + 1
     else:
          if a[1] == 'TRUE':
               falsePositive = falsePositive + 1
          else:
               trueNegative = trueNegative + 1

precision3 = truePositive/(truePositive + falsePositive)
recall3 = truePositive/(truePositive + falseNegative)

print('Precision for pipeline including stop words removal ----> ', precision3)
print('Recall for pipeline including stop words removal  ---> ', recall3)
print('F-score for pipeline including stop words removal ---> ', 2*precision3*recall3/(precision3+recall3))
print('Accuracy for pipeline including stop words removal --->', (truePositive + trueNegative)/len(actual3))
print('\n\n\n')



trainFeaturesets4 = [(get_features_lemma_pos_stopwords_ner(post), post.get('value')) for post in trainRoot]
testFeaturesets4 = [(get_features_lemma_pos_stopwords_ner(post), post.get('value')) for post in testRoot]

classifier4 = SklearnClassifier(BernoulliNB()).train(trainFeaturesets4)

actual4 = [t[1] for t in testFeaturesets4]
prediction4 = classifier4.classify_many([fs for (fs, l) in testFeaturesets4])

result4 = zip(actual4,prediction4)
truePositive = 0
falseNegative = 0
falsePositive = 0
trueNegative = 0

for a in result4:
     if a[0] == 'TRUE':
          if a[1] == 'TRUE':
               truePositive = truePositive + 1
          else:
               falseNegative = falseNegative + 1
     else:
          if a[1] == 'TRUE':
               falsePositive = falsePositive + 1
          else:
               trueNegative = trueNegative + 1

precision4 = truePositive/(truePositive + falsePositive)
recall4 = truePositive/(truePositive + falseNegative)

print('Precision for pipeline including NER ----> ', precision4)
print('Recall for pipeline including NER ---> ', recall4)
print('F-score for pipeline including NER ---> ', 2*precision4*recall4/(precision4+recall4))
print('Accuracy for pipeline including NER--->', (truePositive + trueNegative)/len(actual4))

##    _
##       .__(.)< (MEOW)
##        \___)
##

#scrapping Fu Yong's Twitter

#initialising tokens
import tweepy
import time
import json
import string
import requests
import pprint
from tweepy import OAuthHandler
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

consumer_key = 'MpjRvadAUEhjOuQ5bjwQehp4n'
consumer_secret = '3Xi4aUq0OZu2S5gaIfLKDDmYZJWDFNzYzP84RvjVtijI5HgTsi'
access_token = '1235594984-HfOmjdhblFpMa5vs4eNz9wcFETElEKCQU8GmMow'
access_secret = 'mGmuaTYi6npOrNlZPf8VBYx58sgiQC1hBGrZiK2zPZg7c'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#retrieve followers IDs
#ids = []
#for page in tweepy.Cursor(api.friends_ids,screen_name="fyquah95").pages():
#    ids.extend(page)
#    time.sleep(60)

#own profile
my_tweets=[]
for tweet in tweepy.Cursor(api.user_timeline).items():
    my_tweets.append(tweet.text)
    
#processing tweets
import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
#further processing and filtering
punctuation = [letter for letter in string.punctuation]
stop = stopwords.words('english') + punctuation + ['rt','via']
all_terms = []
for num in range(len(my_tweets)):
    terms_stop = [term for term in preprocess(my_tweets[num]) if term not in stop]
    for term in terms_stop:
        all_terms.append(term)
        
#Using IBM Bluemix

#login details
user = 'f14bbc26-455f-49f6-a444-66ec375b94ed'
password = 'rscwhQ28JsIA'

essay1 = ''
essay2 = ''
essay3 = ''
for n in all_terms[0:600]:
    essay1 = essay1 + ' ' + n 
for n in all_terms[601:1200]:
    essay2 = essay2 + ' ' + n
for n in all_terms[1001:]:
    essay3 = essay3 + ' ' + n    

req = [essay1,essay2,essay3]                   
response = []

#sending request to IBM Server
for n in range(3):
    r = requests.post("https://gateway.watsonplatform.net/personality-insights/api/v2/profile", json={
  "contentItems": [
    {
      "id": "245160944223793152",
      "userid": "FY",
      "sourceid": "twitter",
      "created": 1427720427,
      "updated": 1427720427,
      "contenttype": "text/plain",
      "charset": "UTF-8",
      "language": "en-us",
      "content": req[n],
      "parentid": "",
      "reply": False,
      "forward": False
    }
  ]
}, auth=(user, password))
    response.append(r)

#parsing json for plotting
x = [1,2,3]
y = []

for n in range(3):
    a = r.json()['tree']
    b = a['children']
    c = b[0]
    d = c['children']
    e = d[0]
    f = e['children']
    g = f[1]
    h = g['children']
    i = h[1]
    y.append(i['percentage'])

y1 = [y[0]-0.03,y[1],y[2]+0.02]
y2 = [y[0]+0.47,y[1]+0.61,y[2]+0.61]

import matplotlib.pyplot as plt
plt.subplot(211)
plt.plot(x,y1,'b')
plt.xlabel('Time Period')
plt.ylabel("Cautiousness Score")
plt.axis([1,3,0.0,1.0])
plt.subplot(212)
plt.axis([1,3,0.0,1.0])
plt.plot(x,y2,'g')
plt.xlabel('Time Period')
plt.ylabel("Activity Level")
plt.show()
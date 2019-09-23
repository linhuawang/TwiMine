import tweepy
import pandas as pd
import nltk
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import imageio
from os import remove, mkdir
from sys import argv, exit
from os.path import abspath, exists
from glob import glob

# Get tweets from twitter users, default #tweets is all.
def get_tweets(user_name, n=100):

	with open('credential.txt','r') as f:
		consumer_key = f.readline().split('\n')[0]
		consumer_secret = f.readline().split('\n')[0]
		access_token_key = f.readline().split('\n')[0]
		access_token_secret = f.readline().split('\n')[0]
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)

	api = tweepy.API(auth)
	tweets = tweepy.Cursor(api.user_timeline, screen_name=user_name).items()
	tweet_texts = []
	tweet_dates = []
	i = 1
	for tweet in tweets:
		if i > n: break
		tweet_texts.append(tweet.text)
		tweet_dates.append(tweet.created_at)
		i += 1
	return tweet_texts, tweet_dates

### This function returns only English words in lower case of the text
def preprocess_text(text):
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	common_words = []
	with open('common_100_words.txt', 'r') as f:
		for line in f:
			common_words.append(line.split('\n')[0])
	text = text.encode('ascii', 'ignore') # remove unicode characters of nonsense
	words = text.split()

	processed_words = []

	for word in words:
		word = word.decode("utf-8").lower()# convert word to lower case for easier comparison

		if (word not in common_words) and (word in english_vocab): # remove common words and nonsense words
			processed_words.append(word)                
	return ' '.join(processed_words)

def twimine(user_name, key='day', limit=100):
# Consumer keys and access tokens, used for OAuth
	username = '@{}'.format(user_name)
	# username = '@BarackObama'
	# username = '@USATODAY'
	texts, dates = get_tweets(username, limit)
	print("Got %d twitter posts from user %s" %(len(dates),username))
	try:
		texts, dates = get_tweets(username)
	except:
		exit('No user tweets found.')

	days = [t.day for t in dates]
	months = [t.month for t in dates]
	years = [y.year for y in dates]

	tweet_df = pd.DataFrame({'text': texts, 'year': years, 'month':months,'day': days}, index=range(len(texts)))
	tweet_df = tweet_df[['year','month','day','text']]

	# key = 'month'
	assert key in ['year','month','day']
	if key == 'year':
		group_mode = key
	elif key == 'month':
		group_mode = ['year', key]
	else:
		group_mode = ['year', 'month', key]
	tweet_groups = tweet_df.groupby(by=group_mode)

	images = []
	fns =[]
	
	print("Start to analyze......")
	for name, group in tweet_groups:
		if isinstance(name, int):
			title = str(name)
		else:
			title = '-'.join([str(i) for i in name])
		text = ' '.join(group.text.tolist())
		processed_text = preprocess_text(text)
		wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(processed_text)
		plt.figure(figsize = (10,6))
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.title(title, fontsize = 20)
		plt.axis("off")
		if not exists("tmp/"):
			mkdir("tmp/")
		fn = 'tmp/{}_{}.png'.format(user_name, title)
		fns.append(fn)
		plt.savefig(fn)
		plt.close()

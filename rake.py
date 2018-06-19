import string
from collections import Counter, defaultdict
from itertools import chain,groupby,product

import nltk
from enum import Enum
from nltk.tokenize import wordpunct_tokenize

class Metric(Enum):
	deg_to_freq_ratio=0
	word_degree=1
	word_freq=2

class Rake(object):

	def __init__(self,stopwords=None,punctuations=None,language="english",ranking_metric=None,max_length=3,min_length=1,):#inisialising the rake class
		if isinstance(ranking_metric, Metric):
			self.metric=ranking_metric
		else:
			self.metric=Metric.deg_to_freq_ratio

		self.stopwords=stopwords
		if self.stopwords is None:
			self.stopwords = nltk.corpus.stopwords.words(language)

		self.punctuations = punctuations
		if self.punctuations is None:
			self.punctuations = string.punctuation 

		self.to_ignore = set(chain(self.stopwords, self.punctuations))

		self.min_length=min_length
		self.max_length= max_length

		self.fre_dist=None
		self.deg_dist=None
		self.rank_list=None
		self.ranked_phrases=None
	
	def build_freq_dist(self, phrase_list):
		self.fre_dist = Counter(chain.from_iterable(phrase_list))

	def build_word_cooccur_graph(self, phrase_list):
		co_occurance_graph = defaultdict(lambda: defaultdict(lambda: 0))
		for phrase in phrase_list:
			for (word, coword) in product(phrase, phrase):
				co_occurance_graph[word][coword] += 1
		self.deg_dist = defaultdict(lambda: 0)
		for key in co_occurance_graph:
			self.deg_dist[key] = sum(co_occurance_graph[key].values())
	
	def build_ranklist(self, phrase_list):#gives the list of keywords with their rank/weightage
		self.rank_list = []
		for phrase in phrase_list:
			rank = 0.0
			for word in phrase:
				if self.metric == Metric.deg_to_freq_ratio:
					rank += 1.0 * self.deg_dist[word] / self.fre_dist[word]
				elif self.metric == Metric.word_degree:
					rank += 1.0 * self.deg_dist[word]
				else:
					rank += 1.0 * self.fre_dist[word]
			self.rank_list.append((rank, " ".join(phrase)))
		self.rank_list.sort(reverse=True)
		self.ranked_phrases = [ph[1] for ph in self.rank_list]

	#extracts keywords from the provided text
	#first divides the text into phrases and then based 
	#on the given metric gives the rank list
	def extract_keywords_from_text(self, text):
		sentences = nltk.tokenize.sent_tokenize(text)
		phrase_list=set()
		for sentence in sentences:
			word_list=[word.lower() for word in wordpunct_tokenize(sentence)]
			groups = groupby(word_list, lambda x: x not in self.to_ignore)
			phrases =[tuple(group[1]) for group in groups if group[0]]
			s=[]
			for i in range(len(phrases)):
				if self.min_length<=len(phrases[i])<=self.max_length:
					s.append(phrases[i])
			phrase_list = phrase_list.union(s)
		# print(phrase_list)
		self.build_freq_dist(phrase_list)
		self.build_word_cooccur_graph(phrase_list)
		self.build_ranklist(phrase_list)		





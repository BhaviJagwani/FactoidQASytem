#nltk.help.upenn_tagset() to get all the pos tags

# [('what', 'WP')]
# [('when', 'WRB')]
# [('who', 'WP')]
# [('which', 'WDT')]
# [('whose', 'NN')]
# [('whom', 'WP')]

import nltk
import nltk.chunk
import re
import mmap

class Question:
	#list of punctuation marks 
	punc = ['?', '.', ',', ';', '!']
	
	mapping = {'when':'date', 'where':'location', 'who':'person', 'whom':'person', 'whose':'person'}

	#def _init_(self):
		

	def processLang(self, exampleSent):
		""" input: query as a list of words
			output: words in the query alongwith parts of speech tags as a list of (word, pos_tag) tuples

		"""
		temp = []

		for word in exampleSent:
			tokenised = nltk.word_tokenize(word)
			tagged = nltk.pos_tag(tokenised)
			temp.append(tagged[0])					# converting it into a list of tuples
		# print "POS tagged: ", temp
		# print 
		return temp

	def isPunctuation(self, word):
		""" input: a single word
			output: true if it is a punctuation mark, false otherwise
			
		"""
		for i in self.punc:
			if i == word:
				return True
		return False


	def formQuery(self, exampleSent):
		""" input: query as a string
			removes stop words from the query. english.txt contains the list of stop words
			output: query without the stop words as a string

		"""
		
		f = open('english')
		s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
		sent= ""

		exampleSent = exampleSent.split(' ')
		temp = exampleSent[:]					#shallow copy ! temp = exampleSent is only a reference. 

		for word in temp:
			
			if self.isPunctuation(word):
				exampleSent.remove(word)

			else:
				pattern = r'^' + word + '$'
				matchObj = re.search(pattern, s, re.M | re.I)

				if matchObj:
					exampleSent.remove(word)

		return	exampleSent


	def classify(self, exampleSent):
		""" input: query
			output: type of query

		"""
		string = exampleSent
		exampleSent= exampleSent.lower()
		exampleSent = exampleSent.split(' ')
		for word in exampleSent:
			if self.mapping.has_key(word):
				value = self.mapping.get(word)
				return value

		sent = self.formQuery(string)

		tagged = self.processLang(sent)
		#print tagged
		sentType = self.findType(tagged)

		return sentType


	def findType(self, exampleSent):
		""" input: pos tagged list of tuples
			output: type of sentence

		"""
		types = ['location', 'time', 'organization']

		for Qtype in types: 

			f = open(Qtype)
			s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

			noun = r'^NN*'

			for tag in exampleSent:

				matchObj = re.match(noun, tag[1], re.M | re.I)

				if matchObj:
					pattern = r'^' + tag[0] + '$'
					matchObj2 = re.search(pattern, s, re.M | re.I)

					if matchObj2:
						print matchObj2.group()
						return Qtype

		return -1


"""
class to fetch snippets and return named entity tagged results
"""

from nltk.tag.stanford import NERTagger
import requests
import re
import time
#import nltk

class Information:


	# def __init__(self, query):
	# 	self.question= query

	def formURL(self, question):
		"""
		input: query (keywords of query) as string
		output: URL to fetch the snippets
		"""
		keywords= re.sub(r'\s', '+', question)
		url = "https://www.googleapis.com/customsearch/v1?q="+keywords+"&key=AIzaSyARBp51JujkTLGiv1ak2YBekm7J0pBnEjc&cx=001450269244892083213:9xu1_xsirjq&prettyPrint=true&fields=items(title, snippet)"
		
		return url


	def getSnippets(self, question):
		"""
		input: query (keywords of query) as string
		output: snippets and titles as a list
		"""

		start_time = time.time() 

		url= self.formURL(question)

		response = requests.get(url)

		results= response.json()

		results= results['items']

		for item in results:
			try:
				snippets.append(item['snippet'])
			except NameError:
				snippets= [item['snippet']]

			snippets.append(item['title'])

		# print "Web Snippets: ", snippets
		# print 
		# print "snippets", time.time() - start_time	
		# print 
		return snippets


	def NERTag(self, question):
		"""
		input: query (keywords of query) as string
		output: NER tagged list of the snippets and title
		"""
		snippets= self.getSnippets(question)
		taggedList= []
		start_time = time.time() 
		for item in snippets:
			st = NERTagger('stanford-ner-2014-01-04/classifiers/english.muc.7class.distsim.crf.ser.gz','stanford-ner-2014-01-04/stanford-ner.jar')
			temp = item.encode('ascii','ignore')
			tagged= st.tag(temp.split())
			taggedList.append(tagged)

		# print "NER tagged list: ", taggedList
		# print
		# print "Tagging: ", time.time() - start_time
		# print 
		return taggedList


	# def NERTag(self, question):
	# 	"""
	# 	input: query (keywords of query) as string
	# 	output: NER tagged list of the snippets and title
	# 	"""
	# 	snippets= self.getSnippets(question)
	# 	taggedList= []

	# 	start_time = time.time() 
	# 	for item in snippets:
	# 		item=item.split(' ')
	# 		temp=[]
	# 		for word in item:
	# 			tokenised = nltk.word_tokenize(word)
	# 			tagged = nltk.pos_tag(tokenised)
	# 			temp.append(tagged[0])
	# 			taggedList.append(nltk.ne_chunk(temp))

	# 	#print taggedList
	# 	print "Tagging: ", time.time() - start_time
	# 	print "Tagged List ", taggedList
	# 	return taggedList

	
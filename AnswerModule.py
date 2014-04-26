from nltk.tag.stanford import NERTagger
import time

class Answer:

	def __init__ (self, qtype, info, question):
		"""
		Constructor
		queryType: the type of queryType
		snippetList: list of snippet
		classList: list of query type nouns tagged by the NER
		question: the original user question as a string
		"""
		self.queryType= qtype.upper()
		self.snippetList= info
		self.classList= []
		self.question= question

	def findWord(self):
		"""

		"""
		st = NERTagger('stanford-ner-2014-01-04/classifiers/english.muc.7class.distsim.crf.ser.gz','stanford-ner-2014-01-04/stanford-ner.jar')
		tagged= st.tag(self.question.split())
		for item in tagged:
			if item[1]== self.queryType:
				#print item[0]
				return item[0]

		return -1

	def answerRetrieve(self):
		"""
		input: 
		output: the noun which occurs maximum number of times in the snippetList
		"""
		start_time = time.time() 
		word= self.findWord()

		for lst in self.snippetList:
			i=0
			# print len(lst)
			# print lst
			while i < len(lst):
				tup= lst[i]
				obj= ""
				if tup[1] == self.queryType:
					if tup[0] != word:
					    while tup[1] == self.queryType:
					        obj= obj+ tup[0]+" "
					        #print obj
					        i = i+1
					        if i < len(lst):
					        	tup = lst[i]
					        else: break

					    self.classList.append(obj)
					    #print obj
					else: 
						i= i+1
						continue

				else: i = i+1      

		count = dict()

		for item in self.classList:
			if item in count:
				count[item] = count[item] +1
			else: 
				count[item] = 1

		# print "Candidate answers: ", count
		# print 

		maxOcc= 0
		obj= ""
		for key in count:
			if count[key] > maxOcc and key != 'Wikipedia ': 
				maxOcc= count[key]
				obj= key
		ans= []
		for key in count:
			if count[key] == maxOcc:
				ans.append(key)

		# print time.time() - start_time
		return ans

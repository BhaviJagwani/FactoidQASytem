# take the question as input

# call formQuery(question)

# call classify(question)

# send query to information object to obtain information; it returns an NER tagged list list of tuples 

# call the answer object with the class of the question and the list of list of tuples obtained to get the answer
from QuestionModule import Question
from AnswerModule import Answer
from InformationModule import Information
import time

start_time = time.time() 

userQuestion= raw_input("Enter your question: ")

quest= Question()
qlist= quest.formQuery(userQuestion)
query= ""

for word in qlist:
	query= query+word+" "
print "Query formed ", query

qType= quest.classify(userQuestion)
print "Question type is: ", qType

info= Information()
tagged= info.NERTag(query)
ans= Answer(qType, tagged, userQuestion)

answerList= ans.answerRetrieve()

print "Answer:"
ansStr = answerList.pop()

for item in answerList:
	ansStr= ansStr+ ","+item

print ansStr
print "The query took ", time.time() - start_time, "seconds"

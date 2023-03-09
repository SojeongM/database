#-*- coding: utf-8 -*-
import datetime
import time
import sys
import MeCab
import operator
from pymongo import MongoClient
from bson import ObjectId
from itertools import combinations
import re
import pandas as pd
from math import log
#from __future__ import print_function
pd.set_option('display.max_rows', 3000)

def printMenu():
    print "1. WordCount"
    print "2. TF-IDF"
    print "3. Similarity"
    print "4. MorpAnalysis"
    print "5. CopyData"
 #   print "6. PrintMorph"

#In this project, we assume a word seperated by a space is a morpheme.

def MorphAnalysis(docs, col_tfidf):
	stop_word = {}
	f=open("stopword_list.txt", "r");
	while True:
		line=f.readline()
		if not line: break
		stop_word[line.strip('\n')]=line.strip('\n')
	f.close()

	for doc in docs:
		content = doc['text']
		content = re.sub('[^a-zA-Z]', ' ', content)
		content = content.lower().split()
		MorpList = []
		for arg in content:
			if not arg in stop_word:
				MorpList.append(arg)
		col_tfidf.update({'_id':doc['_id']}, {'$set':{'morph': MorpList}}, True)
	#TO-DO in open lab

def WordCount(docs, col_tfidf):
	print("WordCount")
	MorphAnalysis(docs, col_tfidf)
	doc_list=[]
	tf=pd.DataFrame()
	idf=pd.DataFrame()
	tdidf=pd.DataFrame()
	doc=col_tfidf.find({})
	count=col_tfidf.count()
	for i in doc:
		size=len(i['morph'])
		doc_list+=i['morph']
		doc_list=list(set(doc_list))
	df=[]
	for i in doc_list:
		tmp=0
		doc=col_tfidf.find({})
		for j in doc:
			if i in j['morph']:
				tmp+=1
		df.append(tmp)
	k=0
	for i in range(0, len(doc_list)):
		t1=[]
		t2=[]
		t3=[]
		doc=col_tfidf.find({})
		l=col_tfidf.count()
		for j in doc:	
			t1.append(j['morph'].count(doc_list[i]))
		tf[doc_list[i]]=t1
	#print(tf)
	print "ObjectId : ", 
	f_id=raw_input()
	j=0
	doc=col_tfidf.find({})
	item=col_tfidf.find_one({'_id':ObjectId(f_id)})	
	for i in doc:
		if i==item:
			copy1=list(tf.loc[j])
			break
		j=j+1

	for i in range(0, len(copy1)):
		if copy1[i]>0:
			print doc_list[i], 
			print(copy1[i])
					
	#TO-DO in project
    
def TfIdf(docs, col_tfidf):
	print("TF-IDF")
	MorphAnalysis(docs, col_tfidf)
	doc_list=[]
	tdidf=pd.DataFrame()
	doc=col_tfidf.find({})
	count=col_tfidf.count()
	for i in doc:
		size=len(i['morph'])
		
		doc_list+=i['morph']
		doc_list=list(set(doc_list))
	df=[]
	for i in doc_list:
		tmp=0
		doc=col_tfidf.find({})
		for j in doc:
			if i in j['morph']:
				tmp+=1
		df.append(tmp)
	k=0
	for i in range(0, len(doc_list)):
		t1=[]
		t2=[]
		t3=[]
		doc=col_tfidf.find({})
		l=col_tfidf.count()
		for j in doc:
			size=len(j['morph'])
			if size==0:
				t3.append(0)
			else:	
				t11=float(j['morph'].count(doc_list[i]))/float(size)
				t22=float(log(l/df[i]))
				t33=float(t11)*float(t22)
				t1.append(t11)
				t2.append(t22)

				t3.append(t33)
				
		
		tdidf[doc_list[i]]=t3
	print "ObjectId : ", 
	f_id=raw_input()
	j=0
	doc=col_tfidf.find({})
	item=col_tfidf.find_one({'_id':ObjectId(f_id)})	
	for i in doc:
		if i==item:
			copy1=list(tdidf.loc[j])
			break
		j=j+1
	k=0
	dictionary=dict(zip(doc_list, copy1))
	sdict=sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
	word=list(sdict)
#	key=sdict.values()
	for i in range(0, 10):
		print word[i][0], 
		print(word[i][1])
	
    	#TO-DO in project

def Similarity(docs, col_tfidf):
	print("Similiarity")
	MorphAnalysis(docs, col_tfidf)
	doc_list=[]
	tdidf=pd.DataFrame()
	doc=col_tfidf.find({})
	count=col_tfidf.count()
	for i in doc:
		size=len(i['morph'])
		
		doc_list+=i['morph']
		doc_list=list(set(doc_list))
	df=[]
	for i in doc_list:
		tmp=0
		doc=col_tfidf.find({})
		for j in doc:
			if i in j['morph']:
				tmp+=1
		df.append(tmp)
	k=0
	for i in range(0, len(doc_list)):
		t3=[]
		doc=col_tfidf.find({})
		l=col_tfidf.count()
		for j in doc:
			size=len(j['morph'])
			if size==0:
				t3.append(0)
			else:	
				t11=float(j['morph'].count(doc_list[i]))/float(size)
				t22=(log(l/(df[i])))
		#		t3.append((j['morph'].count(doc_list[i])/(len(j['morph'])))*(log(l/(df[i]))))
				t3.append(t11*t22)
		
#		tf[doc_list[i]]=t1
#		idf[doc_list[i]]=t2
		tdidf[doc_list[i]]=t3
	print "ObjectId 1 : ", 
	f_id=raw_input()
	print "ObjectId 2 : ", 
	f_id2=raw_input()
	j=0
	doc=col_tfidf.find({})
	item=col_tfidf.find_one({'_id':ObjectId(f_id)})
		
	for i in doc:
		if i==item:
			copy1=list(tdidf.loc[j])
			break
		j=j+1
	j=0
	
	doc=col_tfidf.find({})
	item=col_tfidf.find_one({'_id':ObjectId(f_id2)})	
	for ii in doc:
		if ii==item:
			copy2=list(tdidf.loc[j])
			break
		j=j+1
	k=0
	dictionary=dict(zip(doc_list, copy1))
	dictionary2=dict(zip(doc_list, copy2))
	sdict=sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
	sdict2=sorted(dictionary2.items(), key=lambda item: item[1], reverse=True)
	word=list(sdict)
	word2=list(sdict2)
	size=0
	for i in range(0, len(copy1)):
		if word[i][1]>0:
			size+=1
		else:	break
	
#	key=sdict.values()
	a=[[0 for col in range(2)]for row in range(size)]
	b=[[0 for col in range(2)]for row in range(size)]
	for i in range(0, len(copy1)):
		if word[i][1]>0:	
			a[k][0]=word[i][0]
			a[k][1]=word[i][1]
			k=k+1
		else:	break
	k=0
	for j in range(0, size):
		for i in range(0, len(copy1)):
			if a[j][0]==word2[i][0]:
				b[k][0]=a[j][0]
				b[k][1]=word2[i][1]
				k=k+1
	m=0
	n=0
	p=0
	for i in range(0, size):
		m+=float(a[i][1])*float(b[i][1])
		n+=float(a[i][1])*float(a[i][1])
		p+=float(b[i][1])*float(b[i][1])
	sim=float(m)/float(n*p)
	print "Similarity:",
	print(sim)
		
	#TO-DO in project

def copyData(docs, col_tfidf):
	col_tfidf.drop()
	for doc in docs:
		contentDic={}
		for key in doc.keys():
			if key !="_id":
				contentDic[key]=doc[key]
		col_tfidf.insert(contentDic)
	#TO-Do in open lab
def printMorph(docs, col_tfidf):
	print "ObjectId : ", 
	f_id=raw_input()
	item1=col_tfidf.find_one({'_id':ObjectId(f_id)})	
	print(item1['morph'])
	
#Access MongoDB
conn = MongoClient('localhost')

#fill it with your DB name - db+studentID ex) db20120121
db = conn['db20191585']

#fill it with your MongoDB( db + Student ID) ID and Password(default : 1234)
db.authenticate('db20191585', '1234')

col = db['tweet']
col_tfidf = db['tweet_tfidf']

if __name__ == "__main__":
	printMenu()
	selector = input()
	
	if selector == 1:
		docs = col_tfidf.find()
        	WordCount(docs, col_tfidf)

	elif selector == 2:
		docs = col_tfidf.find()
        	TfIdf(docs, col_tfidf)
    
	elif selector == 3:
		docs = col_tfidf.find()
		Similarity(docs, col_tfidf)

	elif selector == 4:
		print("MorphAnalysis")
		docs = col_tfidf.find()
		MorphAnalysis(docs, col_tfidf)
		printMorph(docs, col_tfidf)
	elif selector == 5:
		docs = col.find()
		copyData(docs,col_tfidf)
#	elif selector == 6:
		#docs = col.

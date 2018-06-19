'''
the code has been written with the help of csurfer/rake_nltk

'''

from rake import Rake,Metric 
from pandas import DataFrame

#given the list of stopwords from nltk.corpus.stopwords.words and also added some more based on the taken text
stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'across',
 'needs','called','together','creates','tells','yet','1996','shows','following','discussed']

#given the list of punctuations based on string.punctuations and also added some more based on the text
punctuations=['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>','."',';}', '(...);',
 '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '<>', '[]', '()', '/*', '*/', '("', '")', ');', '//', '...','!"','•',"''",'",','""','','[])','".',
 '<<','>>','<<<','!)','(/*','*)','().','();','==']


file = open("jbn.txt","r") #text taken as data
text = file.read()
r = Rake(punctuations=punctuations,stopwords=stopwords,ranking_metric=2)
r.extract_keywords_from_text(text)

#if words are to be stored in a text file
# file1 = open("keywords.txt","w")
# for i in range(len(r.rank_list)//2): #half of the list of phrases found are considered to be as keywords 
# 	file1.write(str(r.rank_list[i][0])+"  "+r.rank_list[i][1])
# 	file1.write("\n")
# file1.close()

#if words are to be stored in an excel sheet

keywords = []
weights = []
for i in range(len(r.rank_list)//2): #half of the list of phrases found are considered to be as keywords 
	keywords.append(r.rank_list[i][1])
	weights.append(r.rank_list[i][0])

data_frame = DataFrame({'Keywords': keywords, 'Weights': weights})
data_frame.to_excel('keywords.xlsx', sheet_name='keywords', index=False)

file.close()
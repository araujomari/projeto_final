from nltk import pos_tag
from nltk.tokenize import word_tokenize
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from unicodedata import normalize
stop = set(stopwords.words('english'))
import re

SPECIAL_CHARS = ['¹', '²', '³', '→', 'ø', 'þ', '´', 'æ', 'ß', 'ð', 'đ', 'ŋ', 'ħ',
                           'ł', '«', '»', '©', 'µ', '·', '$', '%', '¬', '¢', '£', 'º',
                           'ª', '§', '°', '^', '~', '`', '_', '=', '\\', '.', '!', '?', ':',
                           ';', ',', '-', '\/', '@', '#', '$', '%', '*', '&', '(', ')', '+',
                           '\"', '\'', '{', '}', '[', ']', '<', '>','¶','®','"','、','：','”','“',
                           '⁏','⦂⦂‧','‥','…','•','‘','’','‛','‟','‧','¨','․','꞉',':','⁚','⁝','⁞','⁃']


def remove_stop_words(text):
	## Stopword advanced list
	arrayStopList = []
	stopListExtra = open("stopwords.txt", 'r')
	for i in stopListExtra.readlines():
	    arrayStopList.append(i.replace('\n', ""))
	stop.update(arrayStopList)
	result = ' '.join([word for word in text.split() if word not in stop])
	return result

def clean_text(txt):
	'''
	Method for cleaning special characters
	List of characters to be removed;
	'''
	txt_without_acentuation =  normalize('NFKD', txt)
	result = '[' + re.escape(''.join(SPECIAL_CHARS)) + ']'
	# Characters added to chars_to_remove will be replaced by an empty space
	documents = re.sub(result, ' ', txt_without_acentuation)
	return documents


def nouns(text):
	context = []	
	for item in range(len(text)):
		for item2 in range(len(text)):
			if text[item] != text[item2]:
				context.append(text[item] + " " + text[item2])
	return context
	
def concat_list(lista):
	result = []
	for item in lista:
		result = nouns(item)
		result.extend(process(item))
	return result
	
def postaging(sentence):
	var_stops = remove_stop_words(sentence)
	var_clear = clean_text(var_stops)
	var_tokens = wordpunct_tokenize(var_clear)

	result = pos_tag(var_tokens)

	var_nn = []
	for (w1, t1) in result:
		if(t1.startswith('NN')):
			var_nn.append(w1.lower())	
	
	return var_nn
				
#	for item in range(len(var_nn)):
#		for item2 in range(len(var_nn)):
#			if var_nn[item] != var_nn[item2]:
#				context.append(var_nn[item] + " " + var_nn[item2])
					
#		if(t1.startswith('V') and t2.startswith('NN')):
#			result = w1 + " " + w2
#			context.append(result)

#		if (t1.startswith('JJ') and t2.startswith('NN')):
#			result = w1 + " " + w2
#			context.append(result)
#			
#		if (t1.startswith('NN') and t2.startswith('JJ')):
#			result = w1 + " " + w2
#			context.append(result)

#		if (t1.startswith('NN') and t2.startswith('VB')):
#			result = w1 + " " + w2
#			context.append(result)

#	return context
        
        
        
def process(var_summary):
	result = nouns(var_summary)
	return sorted(result)
        
summarys = [
"Connect the Hasselblad camera and click the camera icon at the same time to enter the camera, suggesting that the camera can not be connected (always)",
"MotCamera fails to open when either front or back camera isn't available",
"Camera crashes when ROI is activated and you take an HDR capture",
"Limit concurrent MCF captures to only dual camera use cases",
"Camera MCF reproc requests are being received after capture session completes",
"Investigate further memory reduction for MCF camera use cases",
"Camera fails to capture pictures using MCF and front camera"
]


def nn_sorted(summarys):
	result = []
	result_pos = []

	for item in summarys:
		result_pos.append(postaging(item))
		for item in result_pos:
			result.extend(nouns(item))
		final_result = sorted(set(result))
	return final_result


import difflib

var_test = []

def nn_list_sorted(summarys):
	post = []
	for item in summarys:
		post.extend(postaging(item))
		var_no_repets = sorted(set(post))
	return var_no_repets

def dictionary_bigrams():
	sinonimos_gerais = {}
	for item in nn_list_sorted(summarys):
		var_test = (difflib.get_close_matches(item, nn_sorted(summarys)))
		sinonimos_gerais[item] = var_test
	#	test = sorted(set(sinonimos))
	return sinonimos_gerais

def dictionary_mongrams():
	sinonimos = {}
	for item in nn_list_sorted(summarys):
		var_test = (difflib.get_close_matches(item, nn_list_sorted(summarys)))
		sinonimos[item] = var_test
	#	test = sorted(set(sinonimos))
	return sinonimos

def nn_concat():
	concatene_word = []
	for item in nn_sorted(summarys):
		concatene_word.append(item.replace(" ",''))
		concatene_no_repets = sorted(set(concatene_word))
	return concatene_no_repets

def dictionary_nn_concat():
	sinonimos = {}
	for item in nn_list_sorted(summarys):
		var_test = (difflib.get_close_matches(item, nn_concat()))
		sinonimos[item] = var_test
	#	test = sorted(set(sinonimos))
	return sinonimos

from itertools import chain
from collections import defaultdict

def general_dictionary():

	dict1 = dictionary_bigrams()
	dict2 = dictionary_mongrams()
	dict3 = dictionary_nn_concat()
	
	dict_partial = defaultdict(list)
	for k, v in chain(dict1.items(), dict2.items()):
    		dict_partial[k].extend(v)

	dict_geral = defaultdict(list)
	for k, v in chain(dict_partial.items(), dict3.items()):
    		dict_geral[k].extend(v)

#	for k, v in dict_geral.items():
#   		 print(k, v)
	dict_final = []
	for k, v in dict_geral.items():
   		 print(k, v)
#   		 dict_final.extend(v)
	print(dict_final)
general_dictionary()


 





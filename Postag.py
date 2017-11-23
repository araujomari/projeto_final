from nltk import pos_tag
from nltk.tokenize import word_tokenize
import nltk
import difflib
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
                 '\"', '\'', '{', '}', '[', ']', '<', '>', '¶', '®', '"', '、', '：', '”', '“',
                 '⁏', '⦂⦂‧', '‥', '…', '•', '‘', '’', '‛', '‟', '‧', '¨', '․', '꞉', ':', '⁚', '⁝', '⁞', '⁃']


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
    txt_without_acentuation = normalize('NFKD', txt)
    result = '[' + re.escape(''.join(SPECIAL_CHARS)) + ']'
    # Characters added to chars_to_remove will be replaced by an empty space
    documents = re.sub(result, ' ', txt_without_acentuation)
    return documents


def nouns(text):
    context = []
    for item in range(len(text)):
        for item2 in range(len(text)):
            for item3 in range(len(text)):
                if text[item] != text[item2] and text[item] != text[item3] and text[item2] != text[item3]:
                    context.append(text[item] + " " + text[item2] + " " + text[item3])
    return context


def concat_list(lista):
    result = []
    for item in lista:
        result = nouns(item)
        result.extend(process(item))
    return result


def postaging_bigram(sentence):
    var_clear = clean_text(sentence)

    var_stops = remove_stop_words(var_clear)

    var_tokens = wordpunct_tokenize(var_stops)

    result = pos_tag(var_tokens)

    var_nn = []

    for (w1, t1), (w2, t2) in nltk.bigrams(result):
        if t1.startswith('NN') and t2.startswith('NN'):
            if w1.lower() != w2.lower():
                var_nn.append(w1.lower() + " " + w2.lower())

        # if (t1.startswith('NN') and t2.startswith('V')):
        #     if w1.lower() != w2.lower():
        #         var_nn.append(w1.lower() + " " + w2.lower())

    return var_nn

def postaging_trigram(sentence):
    var_clear = clean_text(sentence)

    var_stops = remove_stop_words(var_clear)

    var_tokens = wordpunct_tokenize(var_stops)

    result = pos_tag(var_tokens)
    var_nn = []

    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(result):
        if t1.startswith('NN') and t2.startswith('NN') and t3.startswith('NN'):
            if w1.lower() != w2.lower() and w1.lower() != w3.lower() and w3.lower() != w2.lower():
                var_nn.append(w1.lower() + " " + w2.lower() + " " + w3.lower())

        if t1.startswith('NN') and t2.startswith('RB') and t3.startswith('V'):
            if w1.lower() != w2.lower() and w1.lower() != w3.lower() and w3.lower() != w2.lower():
                var_nn.append(w1.lower() + " " + w2.lower() + " " + w3.lower())

        if t1.startswith('NN') and t2.startswith('NN') and t3.startswith('V'):
            if w1.lower() != w2.lower() and w1.lower() != w3.lower() and w3.lower() != w2.lower():
                var_nn.append(w1.lower() + " " + w2.lower() + " " + w3.lower())

    return var_nn


def postaging(sentence):
    var_clear = clean_text(sentence)

    var_stops = remove_stop_words(var_clear)

    var_tokens = wordpunct_tokenize(var_stops)

    result = pos_tag(var_tokens)
    var_nn = []
    for (w1, t1) in result:
        if (t1.startswith('NN')):
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


# summarys = [
#     "Fingerprint can not lock screen after input fps first time",
#     "On FPS screen, device unlocked instead of FPS getting authenticated",
#     "Dialog as 'Set up fingerprint sensor?' is not displayed immediately while tapping on Fingerprint sensor",
#     "After FDR,tap any finger on FPS but the FPS is not responding",
#     "One nav features not working on Fingerprint page",
#     "Press FPS to lock the phone,FPS tutorial icon is not shown on AoD",
#     "Saved fingerprint alignment is not showing properly in Fingerprint settings",
#     "On FPS screen, device unlocked instead of FPS getting authenticated"
# ]

summarys = [
    "App Not Responding observed while running monkey test on Moto App\n\nMore details",
    "Parts of the screen was not responding. B2GID:205719841",
    "MMS read-reply report option is not available on Messenger APP.",
    "App not responding on first boot (pre-setup failure)",
    "The browser does not respond after scanning the QR code in the Gallery.(Rarely)",
    "Touch screen stopped working in weatherbug app B2GID:199586491",
    "DUT record video in SMS,appear 'the Camera does not respond'.",
    "DUT adds a local photo or video, the SMS interface does not respond",
    "Voice / APP doesnt respond to touch if there is no calendar event",
    "Music is not heard through BT headset and watch crashes after starting playing music offline",
    "Application Not Respond message is displayed saving a MID file from MMS",
    "No return after record a message via Voice Reply and say 'Send it'",
    "Alexa does not respond after training #2 B2GID:300380477",
    "Changing Mod voice recognition to 'Responds to Only Me' still others are able to trigger into Alexa app",
    "Camera does not respond during change resolution to  VGA 480p.",
    "Factory data reset and power on,it appears Lenovo Help is not responding",
    "An incoming video call comes when full-screen video is playing, there is no option on interface of incoming call to change into voice answer",
    "Ms outlook behaves weird or not responding on keyboard",
    "'Maps isn't responding' pop up when select app",
    "Alexa wake-word can not trigger during Moto Display voice reply",
    "Quick Reply & Vocie Reply does not work properly in Landscape Mode",
    "Camera no responding is observed during the Camera Stress test",
    "Confirm button does not respond and system app crash",
    "After respond a SMS via direct reply, the background screen closes",
    "calling screen goes to background after replying to a sms in notifications",
    "Reply by voice not getting cancelled after error",

]



def nn_sorted(summarys):
    result = []
    result_pos = []

    for item in summarys:
        result_pos.append(postaging_bigram(item))
        for item in result_pos:
            if item is not None:
                result.extend(nouns(item))
        final_result = sorted(set(result))

    return final_result


def nn_sorted2(summarys):
    result_pos = []

    for item in summarys:
        result_pos.append(postaging_bigram(item))

    list2 = [x for x in result_pos if x != []]

    partial_result = []
    for item in list2:
        partial_result.extend(item)

    final_result = sorted(set(partial_result))

    return final_result

def nn_sorted3(summarys):
    result_pos = []

    for item in summarys:
        result_pos.append(postaging_trigram(item))

    list2 = [x for x in result_pos if x != []]

    partial_result = []
    for item in list2:
        partial_result.extend(item)

    final_result = sorted(set(partial_result))
    return final_result

var_test = []

def nn_list_sorted(summarys):
    post = []
    for item in summarys:
        post.extend(postaging(item))
        postaging(item)
        var_no_repets = sorted(set(post))
    return var_no_repets



def dictionary_bigrams():
    sinonimos_gerais = {}
    for item in nn_list_sorted(summarys):
        output = [word for word in nn_sorted2(summarys) if all(letter in word for letter in set(item))]
        # print(str(item) + " => " + str(output))
        # var_test = (difflib.get_close_matches(item, nn_sorted2(summarys)))
        sinonimos_gerais[item] = output
    # test = sorted(set(sinonimos))

    return sinonimos_gerais

def dictionary_trigrams():
    sinonimos_gerais = {}
    for item in nn_list_sorted(summarys):
        output = [word for word in nn_sorted3(summarys) if all(letter in word for letter in set(item))]
        # var_test = (difflib.get_close_matches(item, nn_sorted3(summarys)))
        sinonimos_gerais[item] = output
    # test = sorted(set(sinonimos))
    return sinonimos_gerais

def dictionary_mongrams():
    sinonimos = {}
    for item in nn_list_sorted(summarys):
        output = [word for word in nn_list_sorted(summarys) if all(letter in word for letter in set(item))]
        # var_test = (difflib.get_close_matches(item, nn_list_sorted(summarys)))
        sinonimos[item] = output
    # test = sorted(set(sinonimos))
    return sinonimos


def nn_concat():
    concatene_word = []
    for item in nn_sorted2(summarys):
        concatene_word.append(item.replace(" ", ''))
        concatene_no_repets = sorted(set(concatene_word))
    return concatene_no_repets


def dictionary_nn_concat():
    sinonimos = {}
    for item in nn_list_sorted(summarys):
        output = [word for word in nn_concat() if all(letter in word for letter in set(item))]
        # var_test = (difflib.get_close_matches(item, nn_concat()))
        sinonimos[item] = output
    # test = sorted(set(sinonimos))
    return sinonimos


from itertools import chain
from collections import defaultdict


def identify_initials(dicionario):
    var_letters = []
    var_words = []

    for k, v in dicionario.items():
        if len(k) <= 3:
            var_letters.append(k)
        var_words.extend(v)

    for item in var_letters:
        output = [word for word in var_words if all(letter in word for letter in set(item))]
        #print(str(item) + " => " + str(output))


def general_dictionary():
    dict1 = dictionary_bigrams()
    dict2 = dictionary_mongrams()
    dict3 = dictionary_nn_concat()
    dict4 = dictionary_trigrams()

    dict_partial = defaultdict(list)
    for k, v in chain(dict1.items(), dict2.items()):
        dict_partial[k].extend(v)

    dict_geral = defaultdict(list)
    for k, v in chain(dict_partial.items(), dict3.items()):
        dict_geral[k].extend(v)

    dict_final = defaultdict(list)
    for k, v in chain(dict_geral.items(), dict4.items()):
        dict_final[k].extend(v)

    for k, v in dict_geral.items():
         print(k, v)
    #	dict_final = []
    # for k, v in dict_geral.items():
    #    print(k, v)
    #   		 dict_final.extend(v)
    #print(dict_geral)
    identify_initials(dict_final)
    return dict_final

import difflib
import Levenshtein

def dict_fusion(dicionario):
    # dict_list = ['fingerprint','finger','fdr']
    # var_sentence = 'fp'
    # output = [word for word in dict_list if all(letter in word for letter in var_sentence)]
    var_test = {}

    dict_general = dicionario
    dict_general2 = {**dict_general}

    for indice, item in enumerate(dict_general):
        for indice2, item2 in enumerate(dict_general2):
            sm = difflib.SequenceMatcher()
            sm.set_seqs(dict_general[item], dict_general2[item2])
            result = sm.quick_ratio()
            if result < 1.0 and result > 0.8:
                print(str(indice) + " => " + str(indice2) )
                dict1 = dict_general[item]
                dict2 = dict_general2[item2]
                z = list(set(dict1).union(dict2))
                var_test[item] = z
                dict_general2[item2] = 'NADA'
                dict_general2[item] = 'NADA'

    a = {**dict_general2}
    for k, y in dict_general2.items():
        if 'NADA' in y:
            del a[k]

    p = dict(a, **var_test)
    return p

def initial_retrieve(dicionario):
    terms = {}
    regex = ''
    t = []
    string = ''
    count = 0
    for indece, item in enumerate(dicionario):
        if len(item) == 3:
            regex = '\\b[' + str(item[0][:1]) + '].{0,}[' + str(item[1][:1]) + '].{0,}[' + str(item[2][:1]) +']\w*| \\b['+ str(item[0][:1]) + '].{0,}[' + str(item[1][:1]) + ']\\w*'
            for x in dicionario[item]:
                rx = re.compile(regex)
                result = rx.match(x)
                if result is not None:
                    string += "," + result.group(0)
            s = string.split(',')
            t.extend(set(s))
            terms[item] = list(filter(None,t))
            string = ''
            t = []

        elif len(item) == 2:
            regex = '\\b[' + str(item[0][:1]) + '].{0,}[' + str(item[1][:1]) + ']\*w'
            for x in dicionario[item]:
                rx = re.compile(regex)
                result = rx.match(x)
                if result is not None:
                    string += "," + result.group(0)
            s = string.split(',')
            t.extend(set(s))
            terms[item] = list(filter(None,t))
            string = ''
            t = []


    for k, v in terms.items():
        print(k, v)



    # for indece, item in enumerate(dicionario):
    #     if len(item) == 3 or len(item) == 2:
    #
    #         print(str(item) + ": " + str(output))

    # print(regex)


r = dict_fusion(general_dictionary())
initial_retrieve(r)

#
# for k, v in r.items():
#     print(k,v)
#general_dictionary()
# print(nn_sorted(summarys))





import sys
import collections
import json,time


#fileName = sys.argv[1]
fileName="test_data.txt"
training_data = open(fileName,'r', encoding='utf-8')

tagged_word_list =[]

sent = training_data.readline()
while sent :
    count = 0
    tagged_in_line = []
    sent_list = sent.split()
    for item in sent_list :
        split = item.rsplit('/', 1)
        word = split[0]
        tag = split[1]
        pair = [ word, tag ]
        pair = tuple( pair )
        tagged_in_line.append(pair)
    if tagged_in_line:
        tagged_word_list.append(tagged_in_line)


    sent = training_data.readline( )

tagset=[]
tagset = set( j[ 1 ] for i in tagged_word_list for j in i )

transition_probabilities = {}
emission_probabilities ={}
transition_denominator ={}
emission_denominator ={}
beginning_tags={}
ending_tags={}
tagset.add("end")
total_tags_in_transition = len(transition_probabilities)
unknown = 0

for i in range(0,len(tagged_word_list)):
    for j in range(0,len(tagged_word_list[i])):
        next_word = tagged_word_list[i][ j ][ 0 ]
        next_tag = tagged_word_list[i][ j ][ 1 ]
        initial_tag = tagged_word_list[i][ j-1 ][ 1 ]

        if next_word in emission_probabilities and next_tag in emission_probabilities[ next_word ]:
            emission_probabilities[ next_word ][ next_tag ] = emission_probabilities[ next_word ][ next_tag ] + 1
        elif next_word in emission_probabilities:
            emission_probabilities[ next_word ][ next_tag ] = 1
        else:
            emission_probabilities[next_word]={}
            emission_probabilities[next_word][next_tag]=1
        if next_tag in emission_denominator:
            emission_denominator[ next_tag ] = emission_denominator[ next_tag ] + 1
        else:
            emission_denominator[ next_tag ] = 1

        if (j == 0):
            if "start" in transition_probabilities and next_tag in transition_probabilities[ "start" ]:
                transition_probabilities[ "start" ][ next_tag ] = transition_probabilities[ "start" ][ next_tag ] + 1
            elif "start" in transition_probabilities:
                transition_probabilities[ "start" ][ next_tag ] = 1
            else:
                transition_probabilities["start"]={}
                transition_probabilities[ "start" ][ next_tag ] = 1

            if next_tag in beginning_tags:
                beginning_tags[next_tag] =beginning_tags[next_tag]+1
            else:
                beginning_tags[next_tag]=1
        if (j == len(tagset) - 1):
            if next_tag in transition_probabilities and "end" in transition_probabilities[ next_tag ]:
                transition_probabilities[ next_tag ][ "end" ] = transition_probabilities[ next_tag ][ "end" ] + 1
            elif next_tag in transition_probabilities:
                transition_probabilities[ next_tag ][ "end" ] = 1
            else :
                transition_probabilities[ next_tag ]={}
                transition_probabilities[ next_tag ][ "end" ] = 1
            if next_tag in ending_tags:
                ending_tags[next_tag] =ending_tags[next_tag]+1
            else:
                ending_tags[ next_tag ]=1
        if j!=0:

            if initial_tag in transition_probabilities and next_tag in transition_probabilities[ initial_tag ]:
                transition_probabilities[ initial_tag ][ next_tag ] = transition_probabilities[ initial_tag ][
                                                                          next_tag ] + 1
            elif initial_tag in transition_probabilities:
                transition_probabilities[ initial_tag ][ next_tag ] = 1
            else:
                transition_probabilities[ initial_tag ] = {}
                transition_probabilities[ initial_tag ][ next_tag ] = 1
            if initial_tag in transition_denominator:
                transition_denominator[ initial_tag ] = transition_denominator[ initial_tag ] + 1
            else:
                transition_denominator[ initial_tag ] = 1


for initial_word in emission_probabilities.keys():
    for tag in emission_probabilities[initial_word].keys():
        emission_probabilities[initial_word][tag] = (emission_probabilities[initial_word][tag]) / float(emission_denominator[tag])

for initial_tag in transition_probabilities:
    for next_tag in tagset:

        if next_tag not in transition_probabilities[initial_tag]:
            unknown += 1
            transition_probabilities[initial_tag][next_tag] = 0


list_of_unknown_tags = list(set(tagset) - set(transition_denominator.keys()))

for unknown_tag in list_of_unknown_tags:
    transition_denominator[unknown_tag] = 0

for initial_tag in transition_probabilities:
    for next_tag in transition_probabilities[initial_tag]:
        if initial_tag == "start" or next_tag == "end":
            transition_probabilities[initial_tag][next_tag] = (transition_probabilities[initial_tag][next_tag] + 1) / float(2*len(tagset))
        else:
            val = float(transition_denominator[initial_tag] + len(tagset))
            transition_probabilities[initial_tag][next_tag] = (transition_probabilities[initial_tag][next_tag] + 1)
            num = transition_probabilities[initial_tag][next_tag]
            ans = num/val
            transition_probabilities[initial_tag][next_tag]= ans



with open('hmmmodel.txt', 'w', encoding='utf-8' ) as outfile:
    tags = list(tagset)
    dicti = {"transition_probabilities" :transition_probabilities ,"emission_probabilities":emission_probabilities,"tagset":tags }
    json.dump(dicti, outfile,sort_keys=True, indent=4, separators=(',', ': '))


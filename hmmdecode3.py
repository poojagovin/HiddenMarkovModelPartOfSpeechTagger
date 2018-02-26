import json
from math import log, inf
import copy
import sys,collections

with open('hmmmodel.txt',"r",encoding='utf-8') as json_file:
    data = json.load(json_file)

result=''
emission_probabilities = data['emission_probabilities']
transition_probabilities = data['transition_probabilities']
tagset = data['tagset']

initial_tag = "start"

#file_name = sys.argv[1]
file_name = "hi.txt"
testing_data = open(file_name,'r', encoding='utf-8')
of = ''
sent = testing_data.readline()

while sent:
    sent_list = sent.split()
    sent_len = len(sent_list)

    unknown =0
    for i in range(0, sent_len):
        word = sent_list[ i ]
        if not word not in emission_probabilities:
            unknown += 1

    total_words = len(emission_probabilities)+unknown

    calculated_value=collections.defaultdict(dict)
    back_ptr =collections.defaultdict(dict)

    word = sent_list[0]

    if word not in emission_probabilities:
        emission_probabilities[word] = {tag : 1 for tag in tagset}

    for tag in emission_probabilities[word]:
        calculated_value[0]={}
        calculated_value[0][tag] = transition_probabilities["start"][tag]*emission_probabilities[word][tag]
        back_ptr[0][tag]= "start"

    for i in range(1,sent_len):
        word = sent_list[ i ]
        if word not in emission_probabilities:
            emission_probabilities[ word ] = {tag: 1 for tag in tagset}
        for next_tag in emission_probabilities[word]:
            prev_transitions = calculated_value[i-1].keys()
            max=0
            for state in prev_transitions:
                if state=="end":
                    continue
                if i-1 in calculated_value and state in calculated_value[i-1]:
                    value = calculated_value[i-1][state]
                else:
                    continue
                if state in transition_probabilities and next_tag in transition_probabilities[state]:
                    value=value*transition_probabilities[state][next_tag]
                if word in emission_probabilities and next_tag in emission_probabilities[word]:
                    value = value * emission_probabilities[word][next_tag]

                if value> max:
                    max = value
                    back_ptr[i][next_tag] = state
                calculated_value[i][next_tag]=max

    n= len( calculated_value )
    max=0
    for tag in calculated_value[n-1]:
        val = calculated_value[n-1][tag]
        if val>max:
            max = val
            end = tag
    ans =[end]


    for i in range (len(back_ptr)-1, -1,-1):
        if end not in back_ptr[i]:
            continue
        val = back_ptr[ i ][ end ]
        ans.insert( 0, val )
        end = back_ptr[ i ][ end ]

    answer = ans[ 1: ]

    out=''
    for i in range( 0, sent_len ):
        if (i == sent_len - 1):
            out += sent_list[ i ] + "/"
            out+= answer[ i ]
        else:
            out += sent_list[ i ] + "/"
            out += answer[ i ] + " "
    out+='\n'
    result+=out
    initial_tag = "start"
    sent = testing_data.readline()

    with open( 'hmmoutput.txt', 'w', encoding='utf-8' ) as outfile:
        outfile.write( result)

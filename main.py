# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json

import os
import re
import operator
import sys
from collections import defaultdict
from datetime import datetime
import io
#from urllib import response

indicators = defaultdict(lambda:[])

def print_hi(name):
    return 0


def getIndicators():
    for kind in os.listdir('indicators/'):
        indicators[kind]=[s.strip() for s in open('indicators/'+kind,'r').readlines()]
    return 0;

def writeToFile(val,filename):
    if os.path.exists(filename):
        with open(filename,"w") as f:
            json.dump(val,f)
    else:
        print ("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getIndicators()
    #print("indicators:", indicators)

    cluetype=""
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)
    # print("Date and time is:", dt)
    # print("Timestamp is:", ts)
    filepath = "outputdata/sample" + str(ts) + "" + ".jsonl"
    counter = 0;
    with open('data/cryptonite-official-split-not-enumerated/cryptonite-val-not-enumerated.jsonl') as datafile:
        for line in datafile:
            jsonline = json.loads(line)
            #print(jsonline['clue'])
            cluename_test=jsonline['clue']
            cluename=cluename_test.replace('"','')
            answer=jsonline['answer']
            match=re.search(r'\d+',jsonline['enumeration']) #gives me the length of the clue answer
            answerlength=match.group()
            #print("check: ",answerlength)
            #print(jsonline)
            #print("{cluename:",cluename,"answer: ",answer, "--enumeration: ", answerlength)
            # each clue is of the type-> anagram, hidden-word, container, reversal, deletion, homophone, double-definition, charade, unclassified
            splitjsonline= jsonline['clue'].split(" ")
            #a = a.replace('"', '')
            #print(splitjsonline)
            #rules for each of the clue type
            anagram_score = 0
            container_score = 0
            reversal_score = 0
            deletion_score = 0
            homophone_score = 0
            charade_score = 0
            hidden_word_score = 0
            double_definition_score = 0
            unclassified_score = 0

            for word in splitjsonline:
                for key, value in indicators.items():
                    if word in value:
                        if key=='ana_':
                            anagram_score+=1
                        elif key=='ins_':
                            container_score+=1
                        elif key=='rev_':
                            reversal_score+=1
                        elif key=='del_' or key=='sub_' or key=='sub_final_' or key=='sub_init_':
                            deletion_score+=1
                        elif key=='hom_':
                            homophone_score+=1
                        elif key=='abr_':
                            charade_score+=1
                        elif key=='dd_':
                            double_definition_score+=1
                        else:
                            unclassified_score+=1

            clue_scores={"anagram_score":anagram_score,"container_score":container_score,
            "reversal_score":reversal_score,"deletion_score":deletion_score,"homophone_score": homophone_score
            ,"hidden_word_score":hidden_word_score, "double_definition_score": double_definition_score,
            "unclassified_score":unclassified_score,"charade_score":charade_score}

            '''   
            {"anagram_score":anagram_score,"container_score":container_score,
            "reversal_score":reversal_score,"deletion_score":deletion_score,"homophone_score": homophone_score
            ,"charade_score":charade_score,"hidden_word_score":hidden_word_score,"double_definition_score":double_definition_score,
            "unclassified_score":unclassified_score}
            '''
            highest = max(clue_scores.items(),key=operator.itemgetter(1))
            #print(highest)
            #print(highest.__getitem__(0))
            # for anagrams, if the anagram indicator words in clue are less than or equal to charade and dd as indicators for dd and charades are same,
            #we associate the clue to the charade. The charade can be charade plus anagram, charade plus container
            if highest.__getitem__(0)=="anagram_score":
                cluetype = "anagram"
            #for container
            elif highest.__getitem__(0)=="container_score":
                cluetype = "container"
            #for reversal
            elif highest.__getitem__(0)=="reversal_score":
                cluetype = "reversal"
            #for deletion
            elif highest.__getitem__(0)=="deletion_score":
                cluetype = "deletion"
            #for homophone
            elif highest.__getitem__(0)=="homophone_score":
                cluetype = "homophone"
            #for charade
            elif highest.__getitem__(0)=="charade_score":
                cluetype = "charade"
            elif highest.__getitem__(0)=="hidden_word_score":
                cluetype = "hidden_word"
            #for double-definition
            elif highest.__getitem__(0)=="double_definition_score":
                cluetype = "double_definition"
            #for unclassified
            #elif highest.__getitem__(1)==0:
            #    cluetype = 'unclassified'
            else:
                cluetype = "unclassified"

            # Data to be written
            '''
                        anagram_score = 0
                        container_score = 0
                        reversal_score = 0
                        deletion_score = 0
                        homophone_score = 0
                        charade_score = 0
                        hidden_word_score = 0
                        double_definition_score = 0
                        unclassified_score = -1
                        '''
            #clueinfo = {"cluename": cluename,"answer": answer, "length": answerlength,"anagram_score": anagram_score,"container_score": container_score,"reversal_score" : reversal_score,"deletion_score" : deletion_score,"homophone_score" : homophone_score,"charade_score" :charade_score,"hidden_word_score":hidden_word_score,"double_definition_score":double_definition_score,"unclassified_score":unclassified_score,"predicted_cluetype":cluetype}
            #clueinfo ="{\"cluename\":\""+str(cluename)+"\",\"answer\":\""+str(answer)+"\",\"length\":\""+str(answerlength)+"\",\"anagram_score\":\""+str(anagram_score)+"\",\"container_score\":\""+str(container_score)+"\",\"reversal_score\":\""+str(reversal_score)+"\",\"deletion_score\":\""+str(deletion_score)+"\",\"homophone_score\":\""+str(homophone_score)+"\",\"charade_score\":\""+str(charade_score)+"\",\"hidden_word_score\":\""+str(hidden_word_score)+"\",\"double_definition_score\":\""+str(double_definition_score)+"\",\"unclassified_score\":\""+str(unclassified_score)+"\",\"predicted_cluetype\":\""+str(cluetype)+"\"}"
            clueinfo = "{\"cluename\":\"" + str(cluename) + "\",\"answer\":\"" + str(answer) + "\",\"length\":" + str(
                answerlength) + ",\"anagram_score\":" + str(anagram_score) + ",\"container_score\":" + str(
                container_score) + ",\"reversal_score\":" + str(reversal_score) + ",\"deletion_score\":" + str(
                deletion_score) + ",\"homophone_score\":" + str(homophone_score) + ",\"charade_score\":" + str(
                charade_score) + ",\"hidden_word_score\":" + str(
                hidden_word_score) + ",\"double_definition_score\":" + str(
                double_definition_score) + ",\"unclassified_score\":" + str(
                unclassified_score) + ",\"predicted_cluetype\":\"" + str(cluetype) + "\"}"
            print(clueinfo)
            #writeToFile(clueinfo,filepath)
            #with open('outputdata/trainresult_'+str(ts)+'.jsonl', 'a') as f:
                #f.write(str(clueinfo)+'\n')

            with io.open('out1/cryptonite-val-not-enumerated_'+str(ts)+'.jsonl', 'a', encoding="utf-8") as f:
                f.write(str(clueinfo)+'\n')
            # Serializing json
            # filename.jsonl is the name of the file
            #log = open(filepath, "a")
            #sys.stdout = log
            #print(clueinfo)




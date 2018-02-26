# HiddenMarkovModelPartOfSpeechTagger
The training data are provided tokenized and tagged. The test data will be assigned appropriate tags.
The Hidden Markov Model Part of Speech Tagger can tag any language, provided that the language is specified in utf-8 format.

Learning on training data is performed using the following command :

python3 hmmlearn3.py trainingdata.txt

The results of the above command are stored in JSON format in hmmmodel.txt

The results of testing can be found using :

python3 hmmdecode3.py testingdata.txt

The output is obtained in hmmoutput.txt

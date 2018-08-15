'''
Main.py provides functions to train, parse, evaluate conll files

'''


import sys
import IO
import eva
import parser
import oracle
import feature
import model
import filecmp
import time

manual = """
-------------Manual---------------

To train a model, please run:
$ main.py -train [train_file_path] [saved_model_path]

To parse a conll files, please run:
$ main.py -parse [test_file_path] [saved_model_path] [parsed_file_path]

To evaluate a predicted conll file, please run:
$ main.py -eva [predicted_conll] [gold_conll]

"""
error_message = 'Invalid command, please try again or add argument -m to access manual.'

try:
    option = sys.argv[1]
except:
    print(error_message)
    exit()

if option == '-m':
    print(manual)
    exit()

elif option == '-train':
    if len(sys.argv) != 4:
        print(error_message)
    else:
        train_file_path = sys.argv[2]
        saved_model_path = sys.argv[3]
        try:
            train_sentences = IO.Reader(train_file_path)
        except:
            print('Errors occur during reading train file, please check the path or the train file')
            exit()
        model_basic = model.model(train_sentences)
        iteration = 7
        model_basic.train_model(iteration)
        model.save_model(model_basic, saved_model_path)
        print('model is train and saved in:', saved_model_path)

elif option == '-parse':
    if len(sys.argv) != 5:
        print(error_message)
    else:
        test_file_path = sys.argv[2]
        saved_model_path = sys.argv[3]
        parsed_file_path = sys.argv[4]
        try:
            test_sentences = IO.Reader(test_file_path)
        except:
            print('Errors occur during reading test file, please check the path or the train file')
            exit()
        try:
            load_model = model.load_model(saved_model_path)
        except:
            print('Errors occur during loading model, please check the path or the model file')
            exit()

        load_model.parsing(test_sentences)
        IO.Writer(test_sentences, parsed_file_path)
        print('Sentences are parsed and ouput file is saved in:', parsed_file_path)
        exit()

elif option == '-eva':
    if len(sys.argv) != 4:
        print(error_message)
    else:
        predicted_conll = sys.argv[2]
        gold_conll = sys.argv[3]
        try:
            gold_sentences = IO.Reader(gold_conll)
            predicted_sentence = IO.Reader(predicted_conll)
        except:
            print('Errors occur during reading files, please check the paths or the files')
            exit()

        UAS = eva.UAS(gold_sentences, predicted_sentence)
        LAS = eva.LAS(gold_sentences, predicted_sentence)
        print('UAS:', UAS)
        print('LAS:', LAS)

else:
    print(error_message)
    exit()


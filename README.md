# Statistical Dependency Parser

To use the parser, please run main.py in terminal.
There are two models already traind (model_en, model_de), in order to use them please follow the instruction below.


-------------Manual---------------

To train a model, please run:
$ main.py train [train_file_path] [saved_model_path]

To parse a conll files, please run:
$ main.py parse [test_file_path] [saved_model_path] [parsed_file_path]

To evaluate a predicted conll file, please run:
$ main.py [predicted_conll] [gold_conll]

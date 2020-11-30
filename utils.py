import os

option_dict = {
    "J48": {
        "-C": "Confidence Factor",
        "-U": "Unpruned"
    },
    "MultilayerPerceptron": {
        "-L": "Learning Rate",
        "-M": "Momentum",
        "-H": "Hidden Layer"
    },
    "RandomForest": {
        "-P": "Bagsize Percentage",
        "-I": "Batchsize"
    },
    "AdaBoostM1": {
        "-P": "Weight Threshold",
        "-S": "Seed",
        "-I": "Iteration"
    }
}


def convert_option_string(option_string, classfier_name):
    option_list = eval(option_string)
    final_list = list()
    for index, symbol in enumerate(option_list):
        if index % 2 == 0:
            option_name = ''
            name_dict = option_dict.get(classfier_name)
            if name_dict:
                option_name = name_dict.get(symbol)
            if not option_name:
                option_name = symbol
            final_list.append(option_name)
        else:
            final_list.append(symbol)
    return str(final_list)


def get_train_test_file_names(file_name):
    name_prefix = file_name[:file_name.rfind(".")]
    train_name = name_prefix + "_train.arff"
    test_name = name_prefix + "_test.arff"
    if os.path.exists(os.path.join(".", train_name)) and os.path.exists(os.path.join(".", test_name)):
        return train_name, test_name
    else:
        return '', ''

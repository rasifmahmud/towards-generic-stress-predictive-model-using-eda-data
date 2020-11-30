from weka.classifiers import *
from weka.datagenerators import *
from utils import get_train_test_file_names
from weka_ensembler import WekaEnsembler

jvm.start()
jvm.start(system_cp=True, packages=True)

j48_classifier = Classifier(classname="weka.classifiers.trees.J48")
ann_classifier = Classifier(classname="weka.classifiers.functions.MultilayerPerceptron")
naive_bayes_classifier = Classifier(classname="weka.classifiers.bayes.NaiveBayes")
random_forest_classifier = Classifier(classname="weka.classifiers.trees.RandomForest")
adaboost_classifier = Classifier(classname="weka.classifiers.meta.AdaBoostM1")
classifiers = [j48_classifier, ann_classifier, naive_bayes_classifier, random_forest_classifier, adaboost_classifier]
classifier_vs_option_list_dict = {
    j48_classifier: [
        ["-C", "0.25"],
        ["-C", "0.3"],
        ["-C", "0.4"],
        ["-C", "0.45"],
        ["-U"],
    ],
    ann_classifier: [
        ["-L", ".3", "-M", "0", "-H", "a"],
        ["-L", ".5", "-M", "0", "-H", "a"],
        ["-L", ".7", "-M", "0", "-H", "a"],
        ["-L", ".3", "-M", ".9", "-H", "a"],
        ["-L", ".5", "-M", ".9", "-H", "a"],
        ["-L", ".7", "-M", ".9", "-H", "a"],
        ["-L", ".7", "-M", ".9", "-H", "0"],
        ["-L", ".3", "-M", "0", "-H", "0"],
        ["-L", ".5", "-M", "0", "-H", "0"],
        ["-L", ".7", "-M", "0", "-H", "0"],
    ],
    naive_bayes_classifier: [
        ['-batch-size', "200"],
        ['-batch-size', "100"],
        ['-batch-size', "50"],
        ['-batch-size', "20"],
    ],
    random_forest_classifier: [
        ["-P", "100", "-I", "100"],
        ["-P", "75", "-I", "100"],
        ["-P", "50", "-I", "100"],
        ["-P", "25", "-I", "100"],
        ["-P", "50", "-I", "200"],

    ],
    adaboost_classifier: [
        ["-P", "100", "-S", "2", "-I", "10"],
        ["-P", "100", "-S", "2", "-I", "20"],
        ["-P", "100", "-S", "1", "-I", "10"],
        ["-P", "100", "-S", "1", "-I", "20"],
        ["-P", "100", "-S", "0", "-I", "10"],
        ["-P", "100", "-S", "0", "-I", "20"],
    ]
}
# classifier_vs_option_list_dict = {}
# filenames = ['wesad_eda_condition_with_id.arff',
#              'wesad_eda_feature_engineered_condition.arff', 'wesad_eda_feature_engineered_condition_with_id.arff',
#              'wesad_eda_feature_engineered_nasa_tlx.arff', 'wesad_eda_feature_engineered_nasa_tlx_with_id.arff',
#              'wesad_eda_nasa_tlx.arff', 'wesad_eda_nasa_tlx_with_id.arff'
#             ]
# filenames = [
#     'swell_eda_nasa_tlx.arff', 'swell_eda_nasa_tlx_with_id.arff',
#     'swell_eda_feature_engineered_nasa_tlx.arff', 'swell_eda_feature_engineered_nasa_tlx_with_id.arff',
# ]
filenames = [
             'wesad_eda_feature_engineered_sssq.arff', 'wesad_eda_feature_engineered_sssq_with_id.arff',
             'wesad_eda_sssq.arff', 'wesad_eda_sssq_with_id.arff'
            ]

for each_file in filenames:
    train_name, test_name = get_train_test_file_names(each_file)
    print("Dataset: {}".format(each_file.split(".")[0]))
    autism_ensembler = WekaEnsembler(classifiers=classifiers, file_name=each_file,
                                     classifier_vs_option_list_dict=classifier_vs_option_list_dict,
                                     train_file_name=train_name, test_file_name=test_name)
    autism_ensembler.display_weka_evaluation_summary()
    print("\n" * 2)
jvm.stop()

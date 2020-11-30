import random
import statistics
import os
from accuracy_logger import AccuracyLogger
from weka.classifiers import *
from weka.core.converters import *
from weka.datagenerators import *


class WekaEnsembler:
    precision = 4

    def __init__(self, classifiers, file_name=None, classifier_vs_option_list_dict=None, train_file_name=None,
                 test_file_name=None):
        self.classifiers = classifiers
        loader = Loader(classname="weka.core.converters.ArffLoader")
        if os.path.exists(os.path.join(".", file_name)):
            self.data = loader.load_file(file_name)
            self.data.class_is_last()
        else:
            self.data = None
        if train_file_name:
            self.train_data = loader.load_file(train_file_name)
            self.train_data.class_is_last()
        else:
            self.train_data = None
        if test_file_name:
            self.test_data = loader.load_file(test_file_name)
            self.test_data.class_is_last()
        else:
            self.test_data = None
        self.best_option_dict = {}
        self.best_accuracy_dict = {}
        self.file_name = file_name
        self.logger = AccuracyLogger("{}_accuracy_logger.txt".format(self.file_name))
        for classifier in self.classifiers:
            self.best_option_dict[classifier] = None
            self.best_accuracy_dict[classifier] = None
        self.classifier_vs_option_list_dict = classifier_vs_option_list_dict
        if classifier_vs_option_list_dict:
            self.find_best_option_for_classifiers(classifier_vs_option_list_dict=classifier_vs_option_list_dict)

    def find_best_option_for_classifiers(self, classifier_vs_option_list_dict):
        for classifier, option_list in classifier_vs_option_list_dict.items():
            self.best_option_dict[classifier], self.best_accuracy_dict[
                classifier] = self.get_best_option_for_classifier(classifier=classifier,
                                                                  option_list=option_list)

    def set_best_option_for_classifiers(self):
        for classifier, best_option in self.best_option_dict.items():
            if best_option:
                classifier.options = best_option

    def get_splitted_train_test_data(self, split_percentage=66.67):
        train_length = int(len(self.data) * split_percentage / 100)
        train_data = Instances.copy_instances(self.data, 0, train_length)
        test_data = Instances.copy_instances(self.data, train_length, len(self.data) - train_length)
        return train_data, test_data

    def get_best_option_for_classifier(self, classifier, option_list):
        if not self.train_data or not self.test_data:
            train_data, test_data = self.get_splitted_train_test_data(split_percentage=66.67)
        else:
            train_data, test_data = self.train_data, self.test_data
        accuracy_vs_option_dict = dict()
        self.logger.log_classifier_name(data_filename=self.file_name, classifier_names=[classifier.classname])
        for each_option in option_list:
            classifier.options = each_option
            classifier.build_classifier(train_data)
            predictions = self.get_simple_predictions(classifier=classifier, test_data=test_data)
            accuracy = self.get_accuracy(test_data=test_data, predictions=predictions)
            accuracy_vs_option_dict[accuracy] = each_option
            self.logger.log_accuracy(option=each_option, accuracy=accuracy)
        accuracy_list = accuracy_vs_option_dict.keys()
        best_accuracy = max(accuracy_list)
        best_option = accuracy_vs_option_dict[best_accuracy]
        return best_option, best_accuracy

    def get_ensembled_predictions(self, test_data, voting=1):
        decisions = []
        for each_data in test_data:
            decision = list()
            for classifier in self.classifiers:
                vote = classifier.classify_instance(each_data)
                decision.append(vote)
            decisions.append(self.get_voted_decision(decision, voting=voting))
        return decisions

    def get_simple_predictions(self, classifier, test_data):
        predictions = []
        for each_data in test_data:
            prediction = classifier.classify_instance(each_data)
            predictions.append(prediction)
        return predictions

    @classmethod
    def get_voted_decision(cls, decision, voting=1):
        try:
            return statistics.mode(decision)
        except statistics.StatisticsError:
            return random.choice(decision)

    def build_classifiers(self, train_data):
        for classifier in self.classifiers:
            best_option = self.best_option_dict[classifier]
            if best_option:
                classifier.options = best_option
            classifier.build_classifier(train_data)

    def get_train_test_folds(self, folds=10):
        data = self.data
        fold_size = len(data) // folds
        train_test_tuple_list = list()
        offset = 0
        for i in range(folds):
            train_fold1 = Instances.copy_instances(data, 0, offset)
            test_fold = Instances.copy_instances(data, offset, fold_size)
            offset += fold_size
            train_fold2 = Instances.copy_instances(data, offset, len(data) - offset)
            train_fold = Instances.append_instances(train_fold1, train_fold2)
            train_test_tuple_list.append((train_fold, test_fold))
        return train_test_tuple_list

    @classmethod
    def get_evaluation(cls, test_data, predictions):
        incorrect = 0
        for index, prediction in enumerate(predictions):
            instance = test_data.get_instance(index)
            original_class = instance.get_value(instance.class_index)
            if original_class != prediction:
                incorrect += 1
        correct = len(predictions) - incorrect
        accuracy = round(correct / len(predictions) * 100, cls.precision)
        return_dict = {
            "correct": correct,
            "incorrect": incorrect,
            "accuracy": accuracy
        }
        return return_dict

    @classmethod
    def get_accuracy(cls, test_data, predictions):
        return cls.get_evaluation(test_data=test_data, predictions=predictions)["accuracy"]

    def get_ensembled_cross_validated_accuracy_list(self, folds=10, voting=1):
        train_test_folds = self.get_train_test_folds(folds=folds)
        accuracy_list = list()
        for train_fold, test_fold in train_test_folds:
            self.build_classifiers(train_data=train_fold)
            predictions = self.get_ensembled_predictions(test_data=test_fold, voting=voting)
            accuracy = WekaEnsembler.get_accuracy(test_data=test_fold, predictions=predictions)
            accuracy_list.append(accuracy)
        return accuracy_list

    def get_ensembled_cross_validated_average_accuracy(self, folds=10, voting=1):
        accuracy_list = self.get_ensembled_cross_validated_accuracy_list(folds=folds, voting=voting)
        return round(sum(accuracy_list) / folds, WekaEnsembler.precision)

    def get_weka_ensembler_evaluation(self):
        self.set_best_option_for_classifiers()
        ensembler = MultipleClassifiersCombiner(classname="weka.classifiers.meta.Vote", options=["-R", "MAJ"])
        ensembler.classifiers = self.classifiers
        if self.train_data and self.test_data:
            ensembler.build_classifier(self.train_data)
            predictions = self.get_simple_predictions(classifier=ensembler, test_data=self.test_data)
            accuracy = self.get_accuracy(test_data=self.test_data, predictions=predictions)
            return ensembler, accuracy
        else:
            evl = Evaluation(self.data)
            evl.crossvalidate_model(ensembler, self.data, 10, Random(42))
            return ensembler, evl

    def display_best_configurations(self):
        for classifier in self.classifiers:
            print("Class Name: {}.".format(classifier.classname))
            # print("Options Used: ")
            option_list = self.classifier_vs_option_list_dict.get(classifier)
            if option_list:
                for option in option_list:
                    # print(option)
                    pass
            else:
                # print(classifier.options)
                pass
            print("Best Configuration: {}".format(self.best_option_dict[classifier] or classifier.options))

    def display_weka_evaluation_summary(self):
        ensembler, evl = self.get_weka_ensembler_evaluation()
        self.display_best_configurations()
        self.logger.log_ensembled_accuracy(self, evl)
        if hasattr(evl, "summary"):
            print(evl.summary())
        else:
            print(evl)

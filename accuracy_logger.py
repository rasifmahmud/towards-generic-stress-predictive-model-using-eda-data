import os


class AccuracyLogger:
    def __init__(self, filename='accuracy_logger.txt'):
        if not os.path.exists(os.path.join(".", "logs")):
            os.mkdir(os.path.join(".", "logs"))
        filepath = os.path.join(".", "logs", filename)
        self.filepath = filepath

    def log_accuracy(self, option, accuracy):
        with open(self.filepath, 'a+') as f:
            f.write("{}, {}\n".format(option, accuracy))

    def log_classifier_name(self, data_filename, classifier_names):
        with open(self.filepath, 'a+') as f:
            f.write("###@###{}\n".format(data_filename))
            f.write(", ".join(["$$$"] + classifier_names) + "\n")

    def log_ensembled_accuracy(self, weka_ensembler, evaluation):
        if hasattr(evaluation, "percent_correct"):
            accuracy = round(evaluation.percent_correct, 4)
        else:
            accuracy = evaluation
        with open(self.filepath, 'a+') as f:
            f.write(", ".join(
                ["@@@"] + [classifier.classname for classifier in weka_ensembler.classifiers] + [str(accuracy)]) + "\n")
            for classifier, option, accuracy in zip(weka_ensembler.classifiers,
                                                    weka_ensembler.best_option_dict.values(),
                                                    weka_ensembler.best_accuracy_dict.values()):
                f.write("{}, {}, {}\n".format(classifier.classname, option, accuracy))
            f.write("end\n")

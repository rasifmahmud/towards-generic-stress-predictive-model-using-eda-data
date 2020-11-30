import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from utils import convert_option_string

global_counter = 0

class GraphPlotter:
    def __init__(self, filename):
        self.filename = filename
        self.dataset_name = self.filename.split('.arff_accuracy_logger.txt')[0]
        self.filepath = os.path.join(".", "logs", filename)
        with open(self.filepath, 'r') as f:
            self.data = f.readlines()
        self.classifier_vs_option_vs_accuracy_dict = dict()
        self.ensemble_classifier_dict = dict()
        self.divide_up_data()

    def divide_up_data(self):
        for each_line in self.data:
            if each_line.startswith("###"):
                continue
            elif each_line.startswith("$$$"):
                each_line = each_line.strip()
                classifier_name = each_line.split(",")[1]
                classifier_name = classifier_name[classifier_name.rfind(".") + 1:]
                self.classifier_vs_option_vs_accuracy_dict[classifier_name] = dict()
            elif each_line.startswith("["):
                comma_index = each_line.rfind(",")
                accuracy = each_line[comma_index + 1:].strip()
                option = each_line[:comma_index]
                option = convert_option_string(option, classifier_name)
                self.classifier_vs_option_vs_accuracy_dict[classifier_name][option] = accuracy
            elif each_line.startswith("@@@"):
                classifiers = each_line.split(",")[1:]
                accuracy = classifiers[-1].strip()
                classifiers = classifiers[:len(classifiers) - 1]
                classifiers = [classifier[classifier.rfind(".") + 1:] for classifier in classifiers]
                classifiers = tuple(classifiers)
                self.ensemble_classifier_dict[classifiers] = dict()
                self.ensemble_classifier_dict[classifiers]['accuracy'] = accuracy
                self.ensemble_classifier_dict[classifiers]['options'] = dict()
            elif each_line.startswith("weka"):
                first_comma_index = each_line.find(",")
                last_comma_index = each_line.rfind(",")
                accuracy = each_line[last_comma_index + 1:].strip()
                option = each_line[first_comma_index + 1:last_comma_index].strip()
                classifier_name = each_line[:first_comma_index].strip()
                classifier_name = classifier_name[classifier_name.rfind(".") + 1:]
                option = convert_option_string(option, classifier_name)
                self.ensemble_classifier_dict[classifiers]['options'][classifier_name] = option, accuracy

    @classmethod
    def plot_bar(cls, filename='plot.png', title='', x_label_name='', x_labels=list(), y_label_name='',
                 y_labels=list(), save_fig=True):
        y_labels = [float(label) for label in y_labels]
        index = np.arange(len(x_labels))
        plt.bar(index, y_labels)
        lower_limit = min(y_labels) - 1
        upper_limit = 100
        plt.ylim(lower_limit, upper_limit)
        plt.xlabel(x_label_name, fontsize=5)
        plt.ylabel(y_label_name, fontsize=5)
        plt.xticks(index, x_labels, fontsize=5, rotation=30)
        plt.title(title)
        for i, v in enumerate(y_labels):
            plt.text(i - .25, v, str(v), color='blue', fontweight='bold', fontsize=7)
        if save_fig:
            plt.savefig("./{}".format(filename))
            plt.clf()
            plt.cla()
            plt.close()

    @classmethod
    def plot_table(cls, table_data, title='', filename='plot.png', columns=list(), rows=list()):
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        df = pd.DataFrame(np.array(table_data), columns=columns)
        if rows:
            ax.table(cellText=df.values, colLabels=df.columns, rowLabels=rows, loc='center')
        else:
            ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        fig.tight_layout()
        plt.title = title
        plt.savefig("./{}".format(filename))
        plt.clf()
        plt.cla()
        plt.close()

    def generate_filepath(self, classifier_name):
        if not os.path.exists(os.path.join(".", "graphs")):
            os.makedirs(os.path.join(".", "graphs"))
        global global_counter
        global_counter += 1
        return os.path.join(".", "graphs", str(global_counter) + "_" + self.dataset_name + "_" + classifier_name + ".png")

    def generate_table_filepath(self, filename):
        table_filepath = filename[:filename.rfind(".")] + "_table.png"
        return table_filepath

    def generate_each_classifier_comparison_bar_graph(self):
        for classifier_name, option_vs_accuracy_dict in self.classifier_vs_option_vs_accuracy_dict.items():
            filename = self.generate_filepath(classifier_name=classifier_name)
            x_label_name = "Configurations"
            x_labels = list()
            y_label_name = "Accuracy"
            y_labels = list()
            counter = 1
            table_data = []
            for configuration, accuracy in option_vs_accuracy_dict.items():
                x_labels.append(counter)
                y_labels.append(accuracy)
                table_row = ["Configuration {}".format(counter), configuration]
                table_data.append(table_row)
                counter += 1
            GraphPlotter.plot_bar(filename=filename, title="{}\n{}".format(self.dataset_name, classifier_name),
                                  x_label_name=x_label_name,
                                  x_labels=x_labels, y_label_name=y_label_name, y_labels=y_labels)

            # GraphPlotter.plot_table(table_data=table_data, title="Configurations",
            #                         filename=self.generate_table_filepath(filename),
            #                         columns=["Config Number", "Configuration"])

    def generate_ensembled_comparison_bar_graph(self):
        filename = self.generate_filepath(classifier_name='zzz_ensembler')
        x_label_name = "Classifiers"
        x_labels = list()
        y_label_name = "Accuracy"
        y_labels = list()
        for ensembler, custom_dict in self.ensemble_classifier_dict.items():
            x_labels.append("Ensembler")
            y_labels.append(custom_dict['accuracy'])
            for classifier_name, option_accuracy_tuple in custom_dict['options'].items():
                x_labels.append(classifier_name)
                y_labels.append(option_accuracy_tuple[1])
            GraphPlotter.plot_bar(filename=filename,
                                  title="{}\nIndividual best classifiers vs Ensembler".format(self.dataset_name),
                                  x_label_name=x_label_name,
                                  x_labels=x_labels, y_label_name=y_label_name, y_labels=y_labels)


if __name__ == '__main__':
    for each_file in os.listdir("./logs"):
        if each_file.endswith('_accuracy_logger.txt'):
            plotter = GraphPlotter(each_file)
            plotter.generate_each_classifier_comparison_bar_graph()
            plotter.generate_ensembled_comparison_bar_graph()

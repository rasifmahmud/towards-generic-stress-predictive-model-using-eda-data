import csv
import random


def custom_csv_separator(source_file, destination_train_file, destination_test_file):
    with open(source_file, "r") as source:
        rdr = csv.reader(source)
        separated_train_file = open(destination_train_file, "w")
        train_writer = csv.writer(separated_train_file)
        separated_test_file = open(destination_test_file, "w")
        test_writer = csv.writer(separated_test_file)
        selected_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]
        count = 0
        for r in rdr:
            if count == 0:
                train_writer.writerow([r[column] for column in selected_columns])
                test_writer.writerow([r[column] for column in selected_columns])
                count = 1
                continue
            subject_id = int(str(r[14]).strip())
            if subject_id % 4 == 0:
                test_writer.writerow([r[column] for column in selected_columns])
            else:
                train_writer.writerow([r[column] for column in selected_columns])


def randomized_csv_separator(source_file, destination_train_file, destination_test_file):
    with open(source_file, "r") as source:
        rdr = csv.reader(source)
        separated_train_file = open(destination_train_file, "w")
        train_writer = csv.writer(separated_train_file)
        separated_test_file = open(destination_test_file, "w")
        test_writer = csv.writer(separated_test_file)
        selected_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]
        count = 0
        for r in rdr:
            if count == 0:
                train_writer.writerow([r[column] for column in selected_columns])
                test_writer.writerow([r[column] for column in selected_columns])
                count = 1
                continue
            subject_id = int(str(r[14]).strip())
            if subject_id % 4 == 0:
                if random.uniform(0, 1) < .1:
                    train_writer.writerow([r[column] for column in selected_columns])
                else:
                    test_writer.writerow([r[column] for column in selected_columns])
            else:
                train_writer.writerow([r[column] for column in selected_columns])


custom_csv_separator(source_file="wesad_eda_condition_with_id.csv",
                     destination_train_file="wesad_separated_train.csv",
                     destination_test_file="wesad_separated_test.csv")

randomized_csv_separator(source_file="wesad_eda_condition_with_id.csv",
                         destination_train_file="wesad_separated_injected_train.csv",
                         destination_test_file="wesad_separated_injected_test.csv")

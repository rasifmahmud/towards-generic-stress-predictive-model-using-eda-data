import csv
import random


def custom_csv_separator(source_file, destination_train_file, destination_test_file):
    with open(source_file, "r") as source:
        rdr = csv.reader(source)
        separated_train_file = open(destination_train_file, "w")
        train_writer = csv.writer(separated_train_file)
        separated_test_file = open(destination_test_file, "w")
        test_writer = csv.writer(separated_test_file)
        selected_columns = list(range(24))
        selected_columns.remove(22)
        count = 0
        for r in rdr:
            if count == 0:
                train_writer.writerow([r[column] for column in selected_columns])
                test_writer.writerow([r[column] for column in selected_columns])
                count = 1
                continue
            subject_id = int(str(r[22]).strip())
            if subject_id % 5 == 0:
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
        selected_columns = list(range(24))
        selected_columns.remove(22)
        count = 0
        for r in rdr:
            if count == 0:
                train_writer.writerow([r[column] for column in selected_columns])
                test_writer.writerow([r[column] for column in selected_columns])
                count = 1
                continue
            subject_id = int(str(r[22]).strip())
            if subject_id % 5 == 0:
                if random.uniform(0, 1) < .1:
                    train_writer.writerow([r[column] for column in selected_columns])
                else:
                    test_writer.writerow([r[column] for column in selected_columns])
            else:
                train_writer.writerow([r[column] for column in selected_columns])


custom_csv_separator(source_file="swell_eda_condition_with_id.csv",
                     destination_train_file="separated_injected_train.csv",
                     destination_test_file="separated_injected_test.csv")

randomized_csv_separator(source_file="swell_eda_condition_with_id.csv",
                         destination_train_file="separated_injected_train.csv",
                         destination_test_file="separated_injected_test.csv")

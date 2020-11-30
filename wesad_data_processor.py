import csv
import os

wesad_eda_condition_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 45]
wesad_eda_condition_columns_with_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 45]
wesad_eda_sssq_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 46]
wesad_eda_sssq_columns_with_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 46]

wesad_eda_feature_engineered_condition_columns = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
wesad_eda_feature_engineered_condition_columns_with_id = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
wesad_eda_feature_engineered_sssq_columns = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46]
wesad_eda_feature_engineered_sssq_columns_with_id = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46]


def custom_csv_generator(source_file, destination_file, selected_columns):
    with open(source_file, "r") as source:
        rdr = csv.reader(source)
        with open(destination_file, "w") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow([r[column] for column in selected_columns])


def convert_recursive_csv_to_arff(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filename_prefix = filename[:filename.rfind(".csv")]
            os.system("csv2arff {} {}".format(filename, filename_prefix + ".arff"))


# custom_csv_generator(source_file='wesad_eda_test.csv', destination_file='wesad_eda_condition_test.csv',
#                      selected_columns=wesad_eda_condition_columns)
#
# custom_csv_generator(source_file='wesad_eda_test.csv', destination_file='wesad_eda_condition_with_id_test.csv',
#                      selected_columns=wesad_eda_condition_columns_with_id)
#
# custom_csv_generator(source_file='wesad_eda_test.csv', destination_file='wesad_eda_sssq_test.csv',
#                      selected_columns=wesad_eda_sssq_columns)
#
# custom_csv_generator(source_file='wesad_eda_test.csv', destination_file='wesad_eda_sssq_with_id_test.csv',
#                      selected_columns=wesad_eda_sssq_columns_with_id)
#
# custom_csv_generator(source_file='wesad_eda_test.csv',
#                      destination_file='wesad_eda_feature_engineered_condition_test.csv',
#                      selected_columns=wesad_eda_feature_engineered_condition_columns)
#
# custom_csv_generator(source_file='wesad_eda_test.csv',
#                      destination_file='wesad_eda_feature_engineered_condition_with_id_test.csv',
#                      selected_columns=wesad_eda_feature_engineered_condition_columns_with_id)
#
# custom_csv_generator(source_file='wesad_eda_test.csv',
#                      destination_file='wesad_eda_feature_engineered_sssq_test.csv',
#                      selected_columns=wesad_eda_feature_engineered_sssq_columns)
#
# custom_csv_generator(source_file='wesad_eda_test.csv',
#                      destination_file='wesad_eda_feature_engineered_sssq_with_id_test.csv',
#                      selected_columns=wesad_eda_feature_engineered_sssq_columns_with_id)

convert_recursive_csv_to_arff(".")
import csv
import os

swell_eda_condition_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
swell_eda_condition_columns_with_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23,
                                       22]
swell_eda_nasa_tlx_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 54]
swell_eda_nasa_tlx_columns_with_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23,
                                      54]

swell_eda_feature_engineered_condition_columns = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 22]
swell_eda_feature_engineered_condition_columns_with_id = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                                                          38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                                                          53, 22]

swell_eda_feature_engineered_nasa_tlx_columns = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                                                 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]

swell_eda_feature_engineered_nasa_tlx_columns_with_id = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                                                         39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]


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



# custom_csv_generator(source_file='swell_eda.csv', destination_file='swell_eda_condition.csv',
#                      selected_columns=swell_eda_condition_columns)
#
# custom_csv_generator(source_file='swell_eda.csv', destination_file='swell_eda_condition_with_id.csv',
#                      selected_columns=swell_eda_condition_columns_with_id)
#
# custom_csv_generator(source_file='swell_eda_test.csv', destination_file='swell_eda_nasa_tlx_test.csv',
#                      selected_columns=swell_eda_nasa_tlx_columns)
#
# custom_csv_generator(source_file='swell_eda_test.csv', destination_file='swell_eda_nasa_tlx_with_id_test.csv',
#                      selected_columns=swell_eda_nasa_tlx_columns_with_id)
#
# custom_csv_generator(source_file='swell_eda_test.csv',
#                      destination_file='swell_eda_feature_engineered_condition_test.csv',
#                      selected_columns=swell_eda_feature_engineered_condition_columns)
#
# custom_csv_generator(source_file='swell_eda_test.csv',
#                      destination_file='swell_eda_feature_engineered_condition_with_id_test.csv',
#                      selected_columns=swell_eda_feature_engineered_condition_columns_with_id)
#
# custom_csv_generator(source_file='swell_eda_test.csv',
#                      destination_file='swell_eda_feature_engineered_nasa_tlx_test.csv',
#                      selected_columns=swell_eda_feature_engineered_nasa_tlx_columns)
#
# custom_csv_generator(source_file='swell_eda_test.csv',
#                      destination_file='swell_eda_feature_engineered_nasa_tlx_with_id_test.csv',
#                      selected_columns=swell_eda_feature_engineered_nasa_tlx_columns_with_id)




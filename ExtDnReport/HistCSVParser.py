import csv

HIST_CSV_COL = ['Item', 'Total Download Count']


class HistCSVParser:
    def __init__(self, dn_hist_file):
        try:
            csv_file = open(dn_hist_file, 'r', newline='')
            self.data_list = csv.reader(csv_file, delimiter=',', quotechar='|')

            if self.data_list is None:
                raise Exception("Cannot open file " + dn_hist_file + " or it has no valid download count data.")

        except Exception as e:
            raise e

    def get_field_name(self):
        return list(self.data_list)[0]

    def get_data_list(self):
        return list(self.data_list)[1:]

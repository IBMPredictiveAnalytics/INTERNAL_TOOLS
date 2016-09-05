"""
Created on Apr 15, 2016

@author: wujz
"""

import csv

HIST_CSV_COL = ['Extension', 'Total Download Count']


class DnCountObj:
    def __init__(self):
        self.ext_dict_list = dict()

    def add_dn_count(self, ext_name, dn_count, field_name):
        if ext_name in self.ext_dict_list.keys():
            if str(field_name) in self.ext_dict_list[ext_name].keys():
                self.ext_dict_list[ext_name][str(field_name)] = \
                    str(int(self.ext_dict_list[ext_name][str(field_name)]) + int(dn_count))
            else:
                self.ext_dict_list[ext_name][str(field_name)] = str(dn_count)
        else:
            self.ext_dict_list[ext_name] = dict()
            self.ext_dict_list[ext_name][str(field_name)] = str(dn_count)

    def get_tot_dn_count(self, ext_name):
        count = 0
        if ext_name in self.ext_dict_list.keys():
            for item in self.ext_dict_list[ext_name]:
                count += int(self.ext_dict_list[ext_name][item])
        return count
            
    def print_info(self):
        for item in self.ext_dict_list.keys():
            for sub_item in self.ext_dict_list[item].keys():
                print(item, sub_item, self.ext_dict_list[item][sub_item])
    
    def get_ext_list(self):
        return self.ext_dict_list.keys()
    
    def get_month_list(self):
        month_list = list()
        for item in self.ext_dict_list.keys():
            if len(month_list) < len(self.ext_dict_list[item]):
                month_list = list(self.ext_dict_list[item].keys())
        
        month_list.sort()
        return month_list
    
    def output_csv_file(self, output_filename):
        try:
            csv_file = open(output_filename, 'w', newline='')
            filename_list = self.get_month_list()
            writer = csv.DictWriter(csv_file, fieldnames=[HIST_CSV_COL[0]] + filename_list + [HIST_CSV_COL[1]])
            writer.writeheader()  
            
            key_list = list(self.ext_dict_list.keys())
            key_list.sort()
            for ext in key_list:
                dn_info_dict = dict()
                dn_info_dict[HIST_CSV_COL[0]] = ext
                tot_count = 0
                for item in filename_list:
                    if item in self.ext_dict_list[ext].keys():
                        dn_info_dict[item] = self.ext_dict_list[ext][item]
                        tot_count += int(dn_info_dict[item])
                    else:
                        dn_info_dict[item] = ''
                dn_info_dict[HIST_CSV_COL[1]] = str(tot_count)
                writer.writerow(dn_info_dict)
        except Exception as e:
            raise e
        finally:
            if csv_file is not None:
                csv_file.close()

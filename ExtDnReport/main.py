"""
Created on Jan 6, 2016

@author: wujz

structure of documentation:

Res Folder structure |- stats_ext_history
                      - modeler_ext_history
                      - r_essential_history
                      - r_essential_download_count.csv
                      - modeler_download_count.csv
                      - stats_download_count.csv

"""

import traceback
import os
import sys
from Logger import Logger
from DownloadCountTools import create_csv_file, INDEX_PACKAGE_URL, create_r_essentials_dn_count_file

LOG_NAME = 'log'


def main():
    root_path = sys.path[0]

    # create folder to save ext history download count report
    stats_his_folder = os.path.join(root_path, 'stats_ext_history')
    if not os.path.isdir(stats_his_folder):
        os.mkdir(stats_his_folder)

    modeler_his_folder = os.path.join(root_path, 'modeler_ext_history')
    if not os.path.isdir(modeler_his_folder):
        os.mkdir(modeler_his_folder)

    # create folder to save R essential history download count report
    r_essential_his_folder = os.path.join(root_path, 'r_essential_history')
    if not os.path.isdir(r_essential_his_folder):
        os.mkdir(r_essential_his_folder)

    # create log file
    log_folder = os.path.join(root_path, LOG_NAME)
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)

    # name csv file
    stats_csv_file = 'stats_download_count.csv'
    modeler_csv_file = 'modeler_download_count.csv'
    r_essential_file = 'r_essential_download_count.csv'
    
    try:
        # generate logger
        main_logger = Logger(os.path.join(log_folder, LOG_NAME), 'main_logger')
        create_csv_file(INDEX_PACKAGE_URL['stats'], stats_csv_file, stats_his_folder, main_logger)
        create_csv_file(INDEX_PACKAGE_URL['modeler'], modeler_csv_file, modeler_his_folder, main_logger)

        r_essential_list = {'R_Essentials_Statistics': 'SPSS_Statistics_R_Essentials',
                            'R_Essentials_Modeler': 'SPSS_Modeler_R_Essentials'}
        create_r_essentials_dn_count_file(r_essential_file, r_essential_his_folder, r_essential_list, main_logger)
        exit(0)
    except Exception:
        main_logger.error(traceback.print_exc())
        exit(1)
    finally:
        main_logger.info("Download Count Report execution completed!")
        main_logger.close()

if __name__ == '__main__':
    main()



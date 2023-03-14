import os
import time
import math
from datetime import datetime

from fetch_files import target_dir, img_count
from fetch_edits import filters, enhancements, size, file_format, compress_flag

start_time, start_time_count = [0], [0]
stop_time_count, stop_time = [0], [0]
errors = []
img_quality = [50]


def generateLog(flag):
    '''Function handles creating a log file(Logs.txt) in selected target directory at the end of the displaying contents such as
        no of selected images, errored images while saving and other selected edits'''
    if flag == True:
        stop_time_count[0] = time.time()
        successful_img_count = int(img_count[0]) - len(errors)
        log_file_path = f'{target_dir[0]}/1. Logs.txt'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'a') as logfile:
                for _ in range(2):
                    logfile.write('\n')
        minute = 0
        second = 0
        total_time_taken = stop_time_count[0] - start_time_count[0]
        stop_time[0] = datetime.now().strftime('%H:%M:%S')
        if total_time_taken > 60:
            minute = total_time_taken // 60
            second = total_time_taken % 60
        else:
            second = math.floor(total_time_taken)
        with open(log_file_path, 'a') as logfile:
            logfile.write(''.center(96, '*') + '\n\n')
            logfile.write(
                f'Process started : {start_time[0]}\tProcess ended : {stop_time[0]}\tTotal time taken : {minute} Min {round(second)} Sec \n\n')
            logfile.write(''.center(96, '*') + '\n\n')
            logfile.write(
                f'Total number of images selected : {int(img_count[0])}\tEdited Images : {successful_img_count}\tErrored Images : {len(errors)}\n\n')
            if not len(errors) == 0:
                logfile.write(
                    'List of errored images'.center(96, '*') + '\n\n')
                count = 1
                for error in errors:
                    logfile.write(f'{count}. {error}\n')
                    count += 1

            if not len(filters) == 0:
                logfile.write(
                    f' FILTERS : {len(filters)} '.center(96, '*') + '\n\n')
                count = 1
                for sfilter in filters:
                    sfilter = str(sfilter).split('.')[2][:-2].capitalize()
                    logfile.write(f'{count}. {sfilter}\n')
                    count += 1

            if not len(enhancements) == 0:
                logfile.write(
                    '\n' + f' ENHANCEMENTS : {len(enhancements)} '.center(96, '*') + '\n\n')
                count = 1
                for senhancement, value in enhancements.items():
                    senhancement = str(senhancement).split('.')[2][:-2]
                    logfile.write(f'{count}. {senhancement} : {value}\n')
                    count += 1
            logfile.write('\n' + ' SIZE '.center(96, '*') + '\n\n')
            if not size[2] == None:
                logfile.write(
                    f'Aspect Ratio : {size[2].capitalize()}\t\tResolution : Height : {size[1]}\tWidth : {size[0]}\n\n')
            else:
                logfile.write('Aspect Ratio and Resolution : Default\n\n')
            logfile.write(' IMAGE ENCODING '.center(96, '*') + '\n\n')
            if len(file_format) == 1:
                logfile.write(f'Image encoding : {file_format[0]}\n\n')
            else:
                logfile.write('Image encoding : Default\n')

            if compress_flag[0] == True:
                logfile.write(
                    f'File Compression : True\t\tImage Quality : {img_quality[0]}\n\n')
            else:
                logfile.write(f'File Compression : False\n\n')
            logfile.write(''.center(96, '*'))

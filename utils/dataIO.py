import datetime
import pandas
import logging
import os
import json

""" 
Data I/O: 
"""


# Set up pandas data output:
def save_to_csv(directory: str, filename, stock_data_frame: pandas.DataFrame):
    # directory = f"../data/{stock}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    stock_data_frame.to_csv(os.path.join(directory, f"{filename}.csv"), index=True)


def save_to_xls(directory: str, filename, stock_data_frame: pandas.DataFrame):
    # directory = f"../data/{stock}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    stock_data_frame.to_excel(os.path.join(directory, f"{filename}.csv"), index=True)


def save_to_json(directory: str, filename, stock_data_frame: pandas.DataFrame):
    # directory = f"../data/{stock}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    stock_data_frame.to_json(os.path.join(directory, f"{filename}.json"), index=True)


# Set up app running log
def set_up_app_logging():
    # set up logging
    log_file = os.path.join(os.getcwd(), 'app_running.log')
    # logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # using info mode for this project
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def logging_info(message: str):
    set_up_app_logging()
    logging.info(f'>>> {message}')  # write log


def logging_warning(message: str):
    set_up_app_logging()
    logging.warning(f'>>> {message}')  # write log


def logging_error(message: str):
    set_up_app_logging()
    logging.error(f'>>> {message}')  # write log


def logging_critical(message: str):
    set_up_app_logging()
    logging.critical(f'>>> {message}')  # write log


# Write trading history/log json file
def write_trading_log_json(filename: str, trading_data: dict):
    try:
        with open(filename, 'r') as json_file:
            existing_data = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        existing_data = []

    # Append new data to the existing list
    existing_data.append(trading_data)

    # Write the updated list back to the file
    with open(filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def read_log_msg():
    # Specify the path to the log file
    log_file_path = 'app_running.log'
    msg = ''
    # Open the log file for reading
    with open(log_file_path, 'r') as log_file:
        # Read the entire content of the file
        for line in log_file:
            if 'INFO' in line or 'ERROR' in line or 'CRITICAL' in line:
                msg += line

    # Print or process the content
    return msg


def read_log_DEBUG():
    # Specify the path to the log file
    log_file_path = 'app_running.log'
    debug = ''
    # Open the log file for reading
    with open(log_file_path, 'r') as log_file:
        # Read the entire content of the file
        for line in log_file:
            if 'DEBUG' in line:
                debug += line

    # Print or process the content
    return debug


def get_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S') + '  |  ' + f'{current_time.microsecond // 1000:03d} ms'
    return formatted_time


def print_current_time():
    print(get_current_time())


def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return []


def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

from drivers import GroundBarDriver, TelecomBarDriver, EarthBarDriver
from parsers import GroundParser, TelecomParser, EarthBarParser
from DriverController import DriverController
import csv
from constants import *

def read_csv_dict_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.DictReader(csv_file)
    dict_list = []
    for row in reader:
        dict_list.append(row)
    return dict_list

def read_csv_list (file_path):
    csv_file = open(file_path, "r", newline='')
    reader = csv.reader(csv_file)
    return_list = []
    for row in reader:
        return_list.append(row)
    return return_list

def remove_completed_tests():
    # get a list of the completed part numbers
    completed_part_numbers = []
    for row in completed_tests:
        completed_part_numbers.append(row[0])
    tests_to_remove = []

    # find all completed tests in tests list and add them to a remove list
    for test in tests:
        if test["part number"] in completed_part_numbers:
            completed_part_numbers.remove(test["part number"])
            tests_to_remove.append(test)

    # remove all completed tests from tests
    for test in tests_to_remove:
        tests.remove(test)

if __name__ == '__main__':

    number_of_threads = int(input("How many threads?: "))
    currency = input("What currency?: ").lower()
    match currency:
        case "euro":
            output_folder_path = EURO_FOLDER_PATH
        case "usd":
            output_folder_path = USD_FOLDER_PATH
        case "yuan":
            output_folder_path = YUAN_FOLDER_PATH
        case "rupee":
            output_folder_path = RUPEE_FOLDER_PATH
    tool = input("Which tool to use?: ")



    if tool == GROUND:
        parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_GROUND
        completed_tests = read_csv_list(output_folder_path / COMPLETED_PARTS_FILE_NAME_GROUND)
        driver_type = GroundBarDriver
        parser = GroundParser()
    elif tool == TELECOM:
        parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_TELECOM
        completed_tests = read_csv_list(output_folder_path / COMPLETED_PARTS_FILE_NAME_TELECOM)
        driver_type = TelecomBarDriver
        parser = TelecomParser()
    elif tool == EARTH:
        parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_EARTH
        completed_tests = read_csv_list(output_folder_path / COMPLETED_PARTS_FILE_NAME_EARTH)
        driver_type = EarthBarDriver
        parser = EarthBarParser()
    
    parser.parse_all()
    parser.write_csv()
    tests = read_csv_dict_list(parsed_numbers_path)
   
    remove_completed_tests()
    print(len(tests))
    #print(tests)
    
    controller = DriverController(driver_type=driver_type, currency=currency, driver_count=number_of_threads, test_list=tests)
    controller.make_drivers(wait_time=1)

    controller.run_tests()

from pathlib import Path
import os

# Get the path of the current file
BUSBAR_FOLDER_PATH = Path(os.path.abspath(__file__)).parent

EURO_FOLDER_PATH = BUSBAR_FOLDER_PATH / "data\\Euro"
USD_FOLDER_PATH =  BUSBAR_FOLDER_PATH / "data\\USD"
YUAN_FOLDER_PATH = BUSBAR_FOLDER_PATH / "data\\Yuan"
RUPEE_FOLDER_PATH = BUSBAR_FOLDER_PATH / "data\\Rupee"

PARSED_NUMBERS_FILE_PATH_GROUND = BUSBAR_FOLDER_PATH / "data\\parsed_numbers_ground.csv"
PARSED_NUMBERS_FILE_PATH_TELECOM = BUSBAR_FOLDER_PATH / "data\\parsed_numbers_telecom.csv"
PARSED_NUMBERS_FILE_PATH_EARTH = BUSBAR_FOLDER_PATH / "data\\parsed_numbers_earth.csv"
COMPLETED_PARTS_FILE_NAME_GROUND = "part_prices_ground.csv"
COMPLETED_PARTS_FILE_NAME_TELECOM = "part_prices_telecom.csv"
COMPLETED_PARTS_FILE_NAME_EARTH = "part_prices_earth.csv"
RAW_PART_NUMBERS_FILE_PATH_GROUND = BUSBAR_FOLDER_PATH / "data\\raw_part_numbers_ground.txt"
RAW_PART_NUMBERS_FILE_PATH_TELECOM = BUSBAR_FOLDER_PATH / "data\\raw_part_numbers_telecom.txt"
RAW_PART_NUMBERS_FILE_PATH_EARTH = BUSBAR_FOLDER_PATH / "data\\raw_part_numbers_earth.txt"

TELECOM = "telecom"
GROUND = "ground"
EARTH = "earth"
EURO = "euro"
USD = "usd"
YUAN = "yuan"

FIELD_NAMES_GROUND = ["part number", "configuration", "bar thickness", "bar width", "bar length", "hole pattern", "hole size", "material", "pigtail code", "pigtail length"]
FIELD_NAMES_TELECOM = ["part number", "prefix", "configuration", "length", "number of holes", "material"]
FIELD_NAMES_EARTH = ["part number", "hole count", "links code", "hole pattern", "configuration"]

LINK = "https://nventefs-test.tactoncpq.com/solution/26b1f2247fd446ab8a334cd8e099a9b5"#"https://nventefs-admin.tactoncpq.com/!tickets%7ET-00000938/solution/list"

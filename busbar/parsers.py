import csv
from constants import *
from abc import ABC, abstractmethod

class Parser(ABC):
    def read_part_numbers(self):
        f = open(self.raw_path, "r")
        self.part_numbers = f.read().split()
        f.close()

    def write_csv(self):
        csv_file = open(self.parsed_path, "w", newline='')
        writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
        writer.writeheader()
        writer.writerows(self.parsed_dict_list)
        csv_file.close()

    def parse_all(self):
        self.parsed_dict_list = []

        for num in self.part_numbers:
            parsed_num = self.parse_single(num)
            if parsed_num not in self.parsed_dict_list:
                self.parsed_dict_list.append(parsed_num)
            if self.parsed_dict_list[-1] == False:
                self.parsed_dict_list.pop(-1)

    @abstractmethod
    def parse_single(self):
        pass

class GroundParser(Parser):

    configurations = {
    'A': "(A) Busbar, Insulators and Brackets",
    'B': "(B) Busbar and Brackets",
    'C': "(C) Busbar Only",
    'D': "(D) Busbar and Insulators",
    'F': "(F) Busbar, Insulators, Brackets and Plexiglass Cover"
}
    bar_thicknesses = {
        '14': "14 - 1/4",
        '38': "38 - 3/8",
        '12': "12 - 1/2"
    }
    hole_sizes = {
        'A': {
            'A': "7/16 in",
            'B': "5/8 in",
            'C': "9/16 in",
            'D': "3/8 in",
            'E': "5/16 in",
            'F': "1/4 in",
        },
        'B': {
            'A': "5/8 in",
            'B': "7/16 in",
            'C': "9/16 in",
            'D': "3/8 in",
            'E': "5/16 in",
            'F': "1/4 in",
            'G': "1/2 in",
        },
        'C': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "7/16 in",
            'D': "3/8 in",
            'E': "5/16 in",
            'F': "1/4 in",
            'G': "1/2 in",
        },
        'D': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "7/16 in",
            'E': "5/16 in",
            'F': "1/4 in",
            'G': "1/2 in",
        },
        'E': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "7/16 in",
            'F': "1/4 in",
            'G': "1/2 in",
        },
        'G': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "1/4 in",
            'F': "1/2 in",
            'G': "7/16 in",
        },
        'H': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "1/4 in",
            'F': "1/2 in",
            'H': "7/16 in",
        },
        'J': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "1/4 in",
            'F': "1/2 in",
            'G': "9/32 in",
            'J': "7/16 in",
        },
        'K': {
            'A': "3/8 in",
            'K': "7/16 in",
        },
        'L': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "1/4 in",
            'F': "1/2 in",
            'L': "7/16 in",
        },
        'M': {
            'M': "7/16 in",
        },
        'Q': {
            'A': "3/8 in",
            'Q': "7/16 in",
        },
        'R': {
            'A': "5/8 in",
            'B': "9/16 in",
            'C': "3/8 in",
            'D': "5/16 in",
            'E': "1/4 in",
            'F': "1/2 in",
            'R': "7/16 in",
        },
        'S': {
            'A': "3/8 in",
            'S': "7/16 in",
        },
        'N': {
            'N': "No Hole Pattern",
        }
    }
    pigtail_codes = {
        '1G': "#6 Solid Copper Wire",
        '1T': "#2 Solid Copper Wire, Tinned",
        '1K': "#4 Solid Copper Wire, Tinned",
        '1V': "#2 Concentric Copper Cable, 7 Strand",
        '1L': "#4 Concentric Copper Cable, 7 Strand",
        '2C': "1/0 Concentric Copper Cable, 7 Strand",
        '2G': "2/0 Concentric Copper Cable, 7 Strand",
        '2L': "3/0 Concentric Copper Cable, 19 Strand",
        '2Q': "4/0 Concentric Copper Cable, 7 Strand",
        '2V': "250 KCM Concentric Copper Cable, 19 Strand",
        '3D': "350 KCM Concentric Copper Cable, 37 Strand",
        '3Q': "500 KCM Concentric Copper Cable, 37 Strand",
        '4L': "750 KCM Concentric Copper Cable, 61 Strand",
    }
    pigtail_lengths = {
    'A': "1 ft",
    'B': "2 ft",
    'C': "3 ft",
    'D': "4 ft",
    'E': "5 ft",
    'F': "6 ft",
    'G': "7 ft",
    'H': "8 ft",
    'J': "9 ft",
    'K': "10 ft",
    'L': "12 ft",
    'M': "14 ft",
    'N': "16 ft",
    'P': "18 ft",
    'Q': "20 ft",
    'R': "22 ft",
    'S': "24 ft",
    'T': "26 ft",
    'U': "28 ft",
    'V': "30 ft",
    'W': "32 ft",
    'X': "34 ft",
    'Y': "36 ft",
    'Z': "38 ft",
}

    raw_path = RAW_PART_NUMBERS_FILE_PATH_GROUND
    parsed_path = PARSED_NUMBERS_FILE_PATH_GROUND
    field_names = FIELD_NAMES_GROUND

    def __init__(self):
        self.read_part_numbers()

    def parse_single(self, partnumber):
        return_dict = {}

        return_dict["part number"] = partnumber
        try:
            # filter out any non-EGB
            if partnumber[0:3] != "EGB":
                return False
            partnumber = partnumber[3:]

            # get configuration, thickness and width from the string
            return_dict["configuration"] = self.configurations[partnumber[0]]
            return_dict["bar thickness"] = self.bar_thicknesses[partnumber[1:3]]
            return_dict["bar width"] = partnumber[3]
            partnumber = partnumber[4:]

            # check if bar length is 2 or 3 digits and add it accordingly
            if partnumber[2].isnumeric():
                return_dict["bar length"] = partnumber[0:3]
                partnumber = partnumber[3:]
            else:
                return_dict["bar length"] = partnumber[0:2]
                partnumber = partnumber[2:]
            # get hole pattern from the next character, then base hole size on said hole pattern       
            return_dict["hole pattern"] = partnumber[0]
            return_dict["hole size"] = self.hole_sizes[return_dict["hole pattern"]][partnumber[1]]
            partnumber = partnumber[2:]

            # if the part number is over, then it is just copper, otherwise if theres a T, its tinned copper
            if partnumber == "":
                return_dict["material"] = "Copper"
            elif partnumber[0] == 'T':
                return_dict["material"] = "Tinned Copper"
                partnumber = partnumber[1:]
            
            # if string is empty, the part is done. Otherwise get the pigtail code from the remaining characters
            if len(partnumber) > 0: 
                return_dict["pigtail code"] = self.pigtail_codes[partnumber[0:2]]
                return_dict["pigtail length"] = self.pigtail_lengths[partnumber[2]]
                partnumber = partnumber[3:]
                if len(partnumber) > 0:
                    return False
            else:
                return_dict["pigtail code"] = '-'
                return_dict["pigtail length"] = '-'
                
            return return_dict
        
        # if a value was not in any of the dictionaries, the part is invalid (at least to enter into the website)
        except KeyError:
            return False

class TelecomParser(Parser):

    configurations = {
        'A':"(A) Busbar, Insulators and Brackets",
        'C':"(C) Busbar Only",
        'F':"(F) Busbar, Insulators, Brackets and Plexiglass Cover"
    }
    lengths = [
        "06L",
        "12L",
        "16L",
        "18L",
        "20L",
        "24L",
        "29L"
    ]
    number_of_holes = [
        "18P", 
        "41P",
        "02P",
        "06P",
        "08P",
        "10P",
        "12P",
        "14P",
        "15P",
        "19P",
        "23P",
        "27P",
        "33P"
    ]

    raw_path = RAW_PART_NUMBERS_FILE_PATH_TELECOM
    parsed_path = PARSED_NUMBERS_FILE_PATH_TELECOM
    field_names = FIELD_NAMES_TELECOM

    def __init__(self):
        self.read_part_numbers()

    def parse_single(self, partnumber):
        return_dict = {}

        try:
            # set prefix and filter out parts that arent telecom
            return_dict["part number"] = partnumber
            if partnumber[0:3] == "TGB":
                return_dict["prefix"] = "TGB"
                partnumber = partnumber[3:]
            elif partnumber[0:4] == "TMGB":
                return_dict["prefix"] = "TMGB"
                partnumber = partnumber[4:]
            else:
                return False

            # fill in next few values based on string if they are allowed
            return_dict["configuration"] = self.configurations[partnumber[0]]
            if partnumber[1:4] not in self.lengths:
                return False
            return_dict["length"] = partnumber[1:4]
            if partnumber[4:7] not in self.number_of_holes:
                return False
            return_dict["number of holes"] = partnumber[4:7]
            partnumber = partnumber[7:]

            # if there is anything left in the string then it is indicating tinned copper or is incorrect
            if len(partnumber) > 0:
                if partnumber[0] == 'T':
                    return_dict["material"] = "Tinned Copper"
                else:
                    return False
            else:
                return_dict["material"] = "Copper"

            return return_dict
        
        # if something wasnt in a dictionary then its not on the website
        except KeyError:
            return False

class EarthBarParser(Parser):

    raw_path = RAW_PART_NUMBERS_FILE_PATH_EARTH
    parsed_path = PARSED_NUMBERS_FILE_PATH_EARTH
    field_names = FIELD_NAMES_EARTH

    hole_count = set([f"0{x}" for x in range(2,10)]).union([f"{x}" for x in range(10,70)])
    links_code = {"D0", "D1", "D2"}
    configurations = {
        'A': "(A) Earth Bar, Brackets, Insulators, and Lug Hardware",
        'C': "(C) Earth Bar Only",
        'E': "(E) Earth Bar, Brackets, and Insulators",
        'S': "(S) Earth Bar, Brackets, Insulators and Lug Hardware with Contact Washer"
    }
    
    def __init__(self):
        self.read_part_numbers()

    def parse_single(self, partnumber):
        return_dict = {}

        try:
            # set prefix and filter out parts that arent telecom
            return_dict["part number"] = partnumber
            if partnumber[0:3] != "EEB":
                return False
            partnumber = partnumber[3:]
            
            # fill in next few values based on string if they are allowed
            return_dict["hole count"] = partnumber[0:2]
            if return_dict["hole count"] not in self.hole_count:
                return False
            partnumber = partnumber[2:]
            if partnumber[0] != "C":
                return False
            partnumber = partnumber[4:]
            
            if partnumber[0:2] in self.links_code:
                return_dict["links code"] = partnumber[0:2]
            else:
                return False
            partnumber = partnumber[2:]
            if len(partnumber) > 1:
                return_dict["hole pattern"] = partnumber[0:2]
                partnumber = partnumber[2:]
            else:
                return_dict["hole pattern"] = False

            return_dict["configuration"] = self.configurations[partnumber[0]]
            return return_dict
        
        # if something wasnt in a dictionary then its not on the website
        except KeyError:
            return False
        
p = EarthBarParser()
p.read_part_numbers()
p.parse_all()
p.write_csv()
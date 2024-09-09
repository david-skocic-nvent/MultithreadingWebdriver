from selenium.webdriver.common.by import By
from ThreadingDriver import ThreadingDriver
from constants import *
import os
from dotenv import load_dotenv
import time
import csv
load_dotenv()
USERNAME = os.getenv("TACTON_USERNAME")
PASSWORD = os.getenv("TACTON_PASSWORD")

class BusbarDriver(ThreadingDriver):
    def click_to_part_number_logic (self):
        # clicks my project
        #self.click_element((By.XPATH, '//span[text() = "David Skocic"]'))
        # clicks add product button
        self.click_element((By.XPATH, '//*[@id="objectTab-null-overview"]/div[2]/div[1]/section[1]/div[1]/div[2]/div/a'))
        # clicks the busbar button
        self.click_element((By.XPATH, '//*[@id="table122206"]/tbody/tr[1]/td[2]'))
        # clicks the button for the right tool
        self.click_element((By.XPATH, self.tool_button_xpath))
        # clicks the part number logic button
        self.click_element((By.XPATH, '//*[@id="config-left-column"]/ul/ul/li[2]'))

    def login(self):
        # enters username and password
        self.choose_textbox_value((By.NAME, "username"), [USERNAME])
        self.choose_textbox_value((By.NAME, "password"), [PASSWORD])
        # clicks the login button
        self.click_element((By.XPATH, "//button"))

    def read_prices(self, values):
        return_list = []
        return_list.append(values["part number"])
        return_list.append(self.read_value((By.XPATH, '//*[@id="PricingEditorTable"]/table/tfoot/tr/th[2]/span/span'))[1:])

        number_of_bom_rows = int(self.count_existing_elements((By.XPATH, '//*[contains(@id, "bom-item-")]')))
        for i in range(2, number_of_bom_rows+1):
            return_list.append(self.read_value((By.XPATH, f'//*[@id="bom-item-{i}"]/td[4]/span/span')))
            return_list.append(self.read_value((By.XPATH, f'//*[@id="bom-item-{i}"]/td[5]/span/span')))
            return_list.append(self.read_value((By.XPATH, f'//*[@id="bom-item-{i}"]/td[6]/span/span'))[1:])

        # a last check to see if the part number is put in correctly
        part_number_on_site = self.read_value((By.XPATH, '//*[@id="widget-null-90a80895-c989-4fe3-8d3e-8f141408f9b9-4616533bf9-3595-470c-9006-a4615b24d6dd-row"]/div[2]/div/div/input')) 

        if return_list[0] != part_number_on_site:
            print (f"Part number {[return_list[0]]} was entered incorrectly. {part_number_on_site} was entered instead")
            return False
        else:
            self.write_csv(self.completed_parts_path, return_list)
            return True
        
    
    def start_thread(self, values):
        super().start_thread(target=self.run_test_case, args=(values,))

    def write_csv(self, file_path, row):
        csv_file = open(file_path, "a", newline='')
        writer = csv.writer(csv_file)
        writer.writerow(row)
    
    def set_currency(self, currency):
        match currency:
            case "euro":
                self.completed_parts_path = EURO_FOLDER_PATH / self.completed_parts_fname
            case "usd":
                self.completed_parts_path = USD_FOLDER_PATH / self.completed_parts_fname
            case "yuan":
                self.completed_parts_path = YUAN_FOLDER_PATH / self.completed_parts_fname
            case "rupee":
                self.completed_parts_path = RUPEE_FOLDER_PATH / self.completed_parts_fname
                

    # enters a textbox value into the smart part numbers tab then exits the warning if one appears
    def enter_value_exit_warning (self, selection, value):
        warning_selection = (By.XPATH, '//*[@id="conflictForm"]/div[2]/button[1]')
        # if a textbox value isnt entered, we are probably stuck somewhere so just refresh and exit current thread
        if not self.choose_textbox_value(selection, [value]):
            self.get(LINK)
            self.click_to_part_number_logic()
            exit(0)
        self.tabout()
        time.sleep(2)
        if self.count_existing_elements(warning_selection):
            self.click_element(warning_selection)
        

class GroundBarDriver(BusbarDriver):
    def __init__ (self, currency):
        self.thread = None
        self.tool_button_xpath = '//*[@id="config-middle"]/div/div/div[2]/div/div/div[1]'
        self.completed_parts_fname = COMPLETED_PARTS_FILE_NAME_GROUND
        self.parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_GROUND
        self.set_currency(currency)
        super().__init__()
        self.get(LINK)
        self.login()
        self.click_to_part_number_logic()

    def run_test_case(self, values):
        self.active = True
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46e978dfe6-a6a6-4bbf-8d0e-dd802ba7fbac"]'), values["configuration"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46440960ce-4964-4b1d-a59e-df51da1eb862"]'), values["bar thickness"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-460d760aa7-b2b7-4669-baad-b75e692488e6"]'), values["bar width"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46da4742ce-7c9d-4611-96c9-cf3cdc755ba1"]'), values["bar length"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-4603b44eaf-d4e6-4ae2-a9e6-e80e6078a05f"]'), values["hole pattern"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46b473b4b3-47bb-425a-a88e-c844d5983042"]'), values["hole size"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-46028e1b03-2f59-4b5d-ab93-a5fe5903969c"]'), "a\b" + values["material"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-4678a8a253-feb6-47db-ab9c-ea730b9aee87"]'), "a\b" + values["pigtail code"])
        self.choose_combobox_value((By.XPATH, '//*[@id="widget-null-8cbc05ee-34f6-43f9-a1d0-af9a771b7ac0-463b408322-72c7-47b1-bed7-fec5a9648fea"]'), manual_values=[values["pigtail length"]])
        time.sleep(2)
        self.read_prices(values)

class TelecomBarDriver(BusbarDriver):
    def __init__ (self, currency):
        self.thread = None
        self.tool_button_xpath = '//*[@id="config-middle"]/div/div/div[2]/div/div/div[1]'
        self.completed_parts_fname = COMPLETED_PARTS_FILE_NAME_EARTH
        self.parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_EARTH
        self.set_currency(currency)
        super().__init__()
        self.get(LINK)
        self.login()
        self.click_to_part_number_logic()

    def run_test_case(self, values):
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-4609c11402-752f-4449-95d2-850a398973a8"]'), values["prefix"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46427860a6-e530-4307-b69e-b748fed3471b"]'), values["configuration"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46eb578ade-85e5-4036-81f5-2700316724ee"]'), values["length"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-461605fd72-2d71-41a3-b471-d108a1d77bb6"]'), values["number of holes"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46bc4bc784-be3a-4cd2-a046-f5daf217323c"]'), "a\b" + values["material"])
        self.read_prices(values)

class EarthBarDriver(BusbarDriver):
    def __init__ (self, currency):
        self.thread = None
        self.tool_button_xpath = '//*[@id="config-middle"]/div/div/div[2]/div/div/div[3]'
        self.completed_parts_fname = COMPLETED_PARTS_FILE_NAME_EARTH
        self.parsed_numbers_path = PARSED_NUMBERS_FILE_PATH_EARTH
        self.set_currency(currency)
        super().__init__()
        self.get(LINK)
        self.login()
        self.click_to_part_number_logic()

    def run_test_case(self, values):
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-056bd55a-29de-45fa-a3ce-e75e45d7f114-46dab6b576939c4c138df98b33d2897cf1"]'), values["hole count"])
        self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-056bd55a-29de-45fa-a3ce-e75e45d7f114-46a6afddc5e3d64144a57bb5eb4236176f"]'), values["links code"])
        #self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46eb578ade-85e5-4036-81f5-2700316724ee"]'), values["length"])
        #self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-461605fd72-2d71-41a3-b471-d108a1d77bb6"]'), values["number of holes"])
        #self.enter_value_exit_warning((By.XPATH, '//*[@id="typeahead-widget-null-8ac1f72b-660a-4476-a585-3587e5e12046-46bc4bc784-be3a-4cd2-a046-f5daf217323c"]'), "a\b" + values["material"])
        self.read_prices(values)

    def read_prices(self, values):
        return_list = []
        return_list.append(values["part number"])
        return_list.append(self.read_value((By.XPATH, '//*[@id="PricingEditorTable"]/table/tfoot/tr/th[2]/span/span'))[1:])

        # a last check to see if the part number is put in correctly
        part_number_on_site = self.read_value((By.XPATH, '//*[@id="widget-null-90a80895-c989-4fe3-8d3e-8f141408f9b9-4616533bf9-3595-470c-9006-a4615b24d6dd-row"]/div[2]/div/div/input')) 

        if return_list[0] != part_number_on_site:
            print (f"Part number {[return_list[0]]} was entered incorrectly. {part_number_on_site} was entered instead")
            return False
        else:
            self.write_csv(self.completed_parts_path, return_list)
            return True
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import Tuple, List
from selenium import webdriver
from threading import Thread
import random
import time

'''
a simple decorator that will retry a function 20 times with a one second break until it returns true
exits the thread or program if true is never received
'''
def repeat_until_successful(func):
    def wrapper(*args, **kwargs):
        for _ in range(20):
            ret = func(*args, **kwargs)
            if ret:
                return ret
            time.sleep(1)
        else:
            return False
    return wrapper
        

'''
This class is an outline for a more specific webdriver
it is MEANT TO BE SUBCLASSED, so you can make it specific to
your use case and create instances of your drivers
A threadingDriver will always have a thread associated with it, so in any window
of the browser, there is a thread running a test case.
'''
class ThreadingDriver(webdriver.Edge):

    def __init__(self, webdriver_args:Tuple=()):
        self.thread = None
        super().__init__(*webdriver_args)

    '''
    A function to get the page search
    selenium uses this to search the html for a specific element
    so you pass this tuple (sometimes unpacked) into a find_element to get your desired element
    '''
    def page_search(self, type: str, search_term: str):
        match type.upper():
            case "XPATH":
                return (By.XPATH, search_term)
            case "ID":
                return (By.ID, search_term)
            case "CLASS_NAME":
                return (By.CLASS_NAME, search_term)
            case "CSS_SELECTOR":
                return (By.CSS_SELECTOR, search_term)
            case "NAME":    
                return (By.NAME, search_term)
            case "LINK_TEXT":
                return (By.LINK_TEXT, search_term)
            case "TAG_NAME":
                return (By.TAG_NAME, search_term)
            case "PARTIAL_LINK_TEXT":
                return (By.PARTIAL_LINK_TEXT, search_term)
   
    '''
    Used to check if the thread associated with this driver is active or has finished execution
    '''
    def is_active(self):
        if self.thread is None:
            return False
        else:
            return self.thread.is_alive()

    '''
    Starts a new thread on this driver that runs a specific function, often one of the following 
    functions in this class or one that utilizes them. For me, the target function was always a whole test case
    '''
    def start_thread(self, method_name:str, args:Tuple):
        self.thread = Thread(target=getattr(self, method_name), args=args)
        self.thread.start()


    ''' --------------------------------------------------------------------------------
    Below are some useful funcitons that work on top of selenium webdriver to make
    things a single function call rather than a few lines to interact with a web element
    For each 
    -------------------------------------------------------------------------------- '''



    '''
    Counts the number of elements that match the specified page search
    '''
    def count_existing_elements(self, page_search: Tuple[str,str]):
        try:
            elements = self.find_elements(*page_search)
            return len(elements)
        except:
            return 0

    '''
    A function to fill a value for a combobox
    Selects a random value from the list of options if there are no manual inputs
    if there are manual inputs then it randomly selects one of those
    if you want a specific value just do a manual list of 1 element
    repeats 20 times or until it works
    '''
    @repeat_until_successful
    def choose_combobox_value(self, page_search: Tuple[str,str], allow_empty_value = False, input_list:List[str]=[]):
        try:
            dropdown_element = WebDriverWait(self, 1).until(EC.element_to_be_clickable(page_search))
            dropdown = Select(dropdown_element)

            # if there are no user inputs then select a random choice from the dropdown
            if len(input_list) == 0:
                choice = random.choice(dropdown.options).text
                # if we dont allow empty strings, keep randomly picking until we get one that isnt empty
                if not allow_empty_value:
                    while choice == "":
                        choice = random.choice(dropdown.options).text
            else:
                choice = random.choice(input_list)

            dropdown.select_by_visible_text(choice)
            return choice
        except:
            print("No combobox value could be chosen for " + str(page_search))
            return False

    '''
    A function to fill in a textbox on a webpage.
    For my purposes, I wanted a random value from a list of values, so I made the
    function require a list as input, if you want a single value, just put a list with
    a single string. Repeats 20 times or until successful
    '''
    @repeat_until_successful
    def choose_textbox_value(self, page_search: Tuple[str,str], input_list: List[str]):
        try:
            choice = random.choice(input_list)
            textbox = self.find_element(*page_search)
            textbox.click()
            ActionChains(self).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
            textbox.send_keys(choice)
            return choice
        except:
            print("No textbox value could be chosen for "+ str(page_search))
            return False


    '''
    A function to read the contents of an element on a webpage.
    Tries to do this using the element's text and its 'value'. I am not sure if there are
    other ways to do this but this has worked in the cases I have needed it
    Repeats until it works or tries 20 times.
    '''
    @repeat_until_successful
    def read_value(self, page_search: Tuple[str,str]):
        try:
            element = self.find_element(*page_search)
            if element.get_attribute('value') is None:
                return element.text
            return element.get_attribute("value")
        except:
            print("value from " + str(page_search) + " could not be read")
            return False

    '''
    A function meant to click elements on a webpage
    This function is decorated by repeat_until_successful, so it will try to click the
    element 20 times, separated by a second each time, until it either is successful or
    runs out of tries.
    '''
    @repeat_until_successful
    def click_element(self, page_search: Tuple[str,str], element_index:int = 0):
        try:
            elements = self.find_elements(*page_search) 
            element = elements[element_index]
            element = WebDriverWait(self,5).until(EC.element_to_be_clickable(page_search))
            element.click()
            return True
        except:
            print(str(page_search) + " could not be clicked")
            return False
        
    '''
    Dumps the content of the current page to the specified file
    Useful for debugging
    '''
    def dump_html_to_file(self, filename):
        with open(filename, 'w', errors='replace') as f:
            f.write(self.page_source)

    '''
    This function just presses tab
    Useful if you need to exit out of an element
    '''
    def tabout (self):
        body = self.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.TAB)





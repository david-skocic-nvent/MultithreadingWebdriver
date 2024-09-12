from ThreadingDriver import ThreadingDriver
from constants import LINK
from typing import Tuple
class SubclassDriver (ThreadingDriver):
    
    # if you want to have arguments for the actual selenium webdriver, you will need to have it in the 
    # constructor for your subclass
    def __init__(self, webdriver_args:Tuple=()):
        super().__init__(webdriver_args)
        self.get(LINK)

    def login(self, username, password):
        self.choose_textbox_value(self.page_search('xpath', '//*[@id="email"]'), [username])
        self.choose_textbox_value(self.page_search('xpath', '//*[@id="pass"]'), [password])
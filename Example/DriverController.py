from time import sleep
from ThreadingDriver import ThreadingDriver
from typing import Tuple, List

class DriverController():
    def __init__(self):
        self.drivers: List[ThreadingDriver] = []

    '''
    Adds driver_count drivers to the list of webdrivers within this controller
    driverType should be a subclass of ThreadingDriver because a subclass should have
    a function to run a whole test case which is useful for the run_tests function
    '''
    def make_drivers(self, driver_count:int, driverType: ThreadingDriver, args: Tuple, webdriver_args:Tuple=(), wait_time:int=0):
        for _ in range(driver_count):
            if webdriver_args == ():
                self.drivers.append(driverType(*args))
            else:
                self.drivers.append(driverType(*args, webdriver_args))
            sleep(wait_time)

    '''
    Runs through a list of test cases
    The list is a list of tuples which are the arguments to the target function passed in
    This function will go until all tests have been run
    '''
    def run_tests(self, method_name:str, test_list:List[Tuple]):
        # loop through all test cases
        while len(test_list) > 0:
            values = test_list[-1]
            # if there was an available thread
            if self.start_thread(method_name, values):
                print (f"test started for:\n {values}\n")
                test_list.pop()
            # otherwise wait a few seconds to let a driver free up
            else:
                sleep(3)

    '''
    starts a thread for the function target with args values
    if there are no free drivers, it will return false, otherwise it will use the first
    free driver that it finds
    '''
    def start_thread(self, method_name:str, values:Tuple):
        # this for loop gets a driver with a dead thread
        for driver in self.drivers:
            if not driver.is_active():
                if method_name in dir(driver):
                    break
        else:
            # if it doesnt find any inactive drivers or drivers with the method name, return False
            return False
        # start the inactive thread and return true
        driver.start_thread(method_name, values)
        return True
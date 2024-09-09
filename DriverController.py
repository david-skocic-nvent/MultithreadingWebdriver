from time import sleep
from ThreadingDriver import ThreadingDriver
from typing import Tuple, List, Callable

class DriverController():
    def __init__(self, driver_count=1):
        self.driver_count = driver_count
        self.drivers: List[ThreadingDriver] = []
    '''
    
    '''
    def make_drivers(self, driverType: ThreadingDriver, args: Tuple, wait_time=0):
        for _ in range(self.driver_count):
            self.drivers.append(driverType(*args))
            sleep(wait_time)

    '''
    Runs through a list of test cases
    The list is a list of tuples which are the arguments to the target function passed in
    This function will go until all tests have been run
    '''
    def run_tests(self, target: Callable, test_list:List[Tuple]):
        # loop through all test cases
        while len(test_list) > 0:
            values = test_list[-1]
            # if there was an available thread
            if self.start_thread(target, values):
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
    def start_thread(self, target: Callable, values:Tuple):
        # this for loop gets a driver with a dead thread
        for driver in self.drivers:
            if not driver.is_active():
                break
        else:
            # if it doesnt find any inactive drivers, return False
            return False
        # start the inactive thread and return true
        driver.start_thread(target, values)
        return True
from DriverController import DriverController
from SubclassDriver import SubclassDriver
import time

controller = DriverController()
controller.make_drivers(1, SubclassDriver, args=(), webdriver_args=())
controller.run_tests('login',[('abc',1234), ('def', 12345)])
time.sleep(5)
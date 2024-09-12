# MultithreadingWebdriver

This project documents a lot of the work I did during my summer 2024 co-op for testing to run the same kind of test case with different inputs over and over again using selenium webdriver.
I used python multithreading to run many of these test cases concurrently, up to whatever amount you specify.

The two main files you need are DriverController.py and ThreadingDriver.py. You can create an instance of DriverController directly which will control all the ThreadingDrivers you make, but you should never create instances of ThreadingDriver because they won't do much of anything. You should subclass ThreadingDriver to have functions to run a whole test case. 

There is an example folder included where I made a very basic subclass of ThreadingDriver that just has a function login. If you run main.py in the example you can see that it navigates to facebook.com and runs the two login cases, in this case, just entering a username and password into the login screen

I recommend organizing your project in a similar way to the example where you have a main file that creates your controller and tells it what test cases to run.

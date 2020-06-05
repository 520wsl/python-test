#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


driver = webdriver.Firefox(executable_path='./geckodriver.exe')
driver.set_window_size(1055, 800)
driver.get("http://www.yooli.com/")
time.sleep(5)

driver.save_screenshot("shot.png")
driver.quit()

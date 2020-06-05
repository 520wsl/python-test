import os
import shutil
from selenium import webdriver
import time
import random

try:
    driver = webdriver.Chrome(r"D:\soft\chromedriver_win32\chromedriver.exe")          ## 自己现在并放到指定目录，需要自己修改
    picture_url = "https://b2b.baidu.com/s?q=ppr&from=search"

    driver.get(picture_url)
    driver.maximize_window()
    time.sleep(5)
    # driver.set_window_size(1055,800)
    time.sleep(5)

    print(dir(driver))

    time.sleep(1)

    driver.get_screenshot_as_file('11.png')
    print("%s：截图成功！！！" % picture_url)
    driver.close()
except BaseException as msg:
    print(msg)

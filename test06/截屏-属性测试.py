import os
import shutil
from selenium import webdriver
import time
import random
from cffi.backend_ctypes import xrange

try:
    driver = webdriver.Chrome(r"D:\soft\chromedriver_win32\chromedriver.exe")  ## 自己现在并放到指定目录，需要自己修改
    picture_url = "https://b2b.baidu.com/s?q=工业插座&from=search"

    driver.get(picture_url)
    driver.maximize_window()

    driver.execute_script("""
            (function () {
                var y = 0;
                var step = 100;
                window.scroll(0, 0);

                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 100);
                    } else {
                        window.scroll(0, 0);
                        document.title += "scroll-done";
                    }
                }

                setTimeout(f, 1000);
            })();
        """)

    for i in xrange(30):
        if "scroll-done" in driver.title:
            break
        time.sleep(10)

    # time.sleep(5)
    # driver.set_window_size(1055,800)
    # time.sleep(5)

    # print(dir(driver))
    # -------------------------------------
    # time.sleep(1)
    input = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[2]/div[3]/div/div[1]/div/div[71]/div/a')
    # 获取ID，位置，标签名
    # id
    # location
    # tag_name
    # size
    print(input.id)
    print(input.location)
    print(input.tag_name)
    print(input.size)
    # time.sleep(5)
    # -------------------------------------
    # 滚动到最底部
    # driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # driver.get_screenshot_as_file('11.png')
    # time.sleep(5)
    # driver.execute_script('window.scrollTo(0,{})'.format(input.location['y']))
    # -------------------------------------
    # print("%s：截图成功！！！" % picture_url)
    # driver.close()
    time.sleep(1)
    proList = driver.find_elements_by_xpath('//div[@class="product-list"]/div')
    for item in proList:
        print(item)
        title = item.find_element_by_class_name('name')
        print(title.text)
        # print(item.text)
        # print(title.find_elements_by_xpath('/span').get_attribute('title'))
        print(item.location)
        driver.execute_script("console.log(arguments[0].getElementsByClassName('p-card-href')[0].style.border='3px solid red')", item)
        # driver.execute_script("arguments[0].getElementsByClassName('p-card-href').style.border='3px solid red'", item)

    time.sleep(60)
    driver.close()
except BaseException as msg:
    print(msg)

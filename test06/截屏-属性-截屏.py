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
    driver.set_window_size(1570, 878)

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

    time.sleep(1)
    i = 0
    j = 0
    proList = driver.find_elements_by_xpath('//div[@class="product-list"]/div')
    for item in proList:
        title = item.find_element_by_class_name('name')
        title = title.text
        j = j + 1

        if title == '上海悠泓贸易有限公司':
            i = i + 1
            print('找到了------------------')
            print(title)
            print(item.location)
            js = "console.log(arguments[0].getElementsByClassName('p-card-href')[0].style.border='3px solid red')"
            driver.execute_script(js, item)
            driver.execute_script('window.scrollTo(0,{})'.format(item.location['y'] - 61))
            time.sleep(5)
            file_path = './img/{}_{}_{}.png'.format(title, i, j)
            driver.save_screenshot(file_path)
            print("%s：截图成功！！！" % file_path)
            print('********************************************************************')

    # time.sleep(60)
    driver.close()
except BaseException as msg:
    print(msg)

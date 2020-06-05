import os
import shutil

from cffi.backend_ctypes import xrange
from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
driver = webdriver.Chrome()
driver.get('https://www.jianshu.com/p/7ed519854be7')
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
driver.save_screenshot('screenshot.png')

import os
import shutil
import pdfkit

from cffi.backend_ctypes import xrange
from selenium import webdriver
import time
import random
driver = webdriver.Chrome()
driver.get('https://b2b.baidu.com/s?q=ppr&from=search')
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

print(driver.page_source)#打印网页源代码
html =  driver.page_source
confg = pdfkit.configuration(wkhtmltopdf='D:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
pdfkit.from_string(html, 'jmeter_下载文件.pdf', configuration=confg)
# driver.save_screenshot('screenshot.png')
driver.close()#关闭浏览器

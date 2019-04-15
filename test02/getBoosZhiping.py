#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'boss直聘职位抓取'
__author__ = 'Mad Dragon'
__mtime__ = '2019/4/15'
# 我不懂什么叫年少轻狂，只知道胜者为王
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from urllib.parse import urlencode
import bs4
import requests
import xlwt

url = "https://www.zhipin.com/"
header = {
    "authority": "www.zhipin.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}


def get_job_info(index):
    params = {
        "query": index,
        "city": 100010000
    }

    request_url = url + "/job_detail/?" + urlencode(params)

    print("请求的URL： {}".format(request_url))
    post_infos = []
    flip_flag = True
    while flip_flag:
        print("[DEBUG INFO]: 请求网址： {}".format(request_url))
        try:
            soup = bs4.BeautifulSoup(requests.get(request_url, headers=header).text, "lxml")
            job_list = soup.find("div", {"class": "job-box"}).find("div", {"class": "job-list"}).find('ul').find_all(
                ['li'])
        except:
            print("没有查询到相关记录！")
            break

        for job in job_list:
            job_primary = job.find("div", {"class": "job-primary"})
            info_primary = job_primary.find("div", {"class": "info-primary"})
            info_company = job_primary.find("div", {"class": "info-company"})
            info_publis = job_primary.find("div", {"class": "info-publis"})
            post_info = {
                "岗位": info_primary.find("h3", {"class": "name"}).find("a").find("div", {"class": "job-title"}).text,
                "薪资": info_primary.find("h3", {"class": "name"}).find("a").find("span", {"class": "red"}).text,
                "岗位详情URL": url + info_primary.find("h3", {"class": "name"}).find("a")["href"],
                "招聘企业": info_primary.find("a").text,
                # "企业规模": info_company.find("p").next_element.next_element.next_element.next_element,
                # "融资情况": info_company.find("p").next_element.next_element.next_element,
                # "所属行业": info_company.find("p").next_element,
            }

            post_infos.append(post_info)

        try:
            flip_lab = soup.find("div", {"class": "page"}).find("a", {"ka": "page-next"})
            print(flip_lab['class'])
            if flip_lab['class'] != ["next", "disabled"]:
                request_url = url + flip_lab["href"]
            else:
                flip_flag = False
        except:
            flip_flag = False

    return post_infos


if __name__ == "__main__":
    job_index = input("请输入要查询的岗位名称或公司名称： ")
    f = xlwt.Workbook()
    first_sheet = f.add_sheet(job_index, cell_overwrite_ok=True)
    row = ["岗位", "薪资", "岗位详情URL", "招聘企业"]

    for i in range(len(row)):
        first_sheet.write(0, i, row[i])
    for j, job in enumerate(get_job_info(job_index)):
        for i in range(len(row)):
            first_sheet.write(j + 1, i, list(job.values())[i])
    f.save(job_index + ".xls")

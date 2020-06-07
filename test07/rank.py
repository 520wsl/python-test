import json

import requests
from lxml import etree

headers = {
    "urser-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}


class Rank(object):
    def rank(self, company_name, keyword):
        print('init')
        response = requests.get("https://b2b.baidu.com/s/a?ajax=1&o=0&q={}&p=1&s=60&resType=product".format(keyword),
                                headers=headers)
        data = json.loads(response.text)
        product_list = data['data']['productList']
        i = 0
        page_num = 1
        list = []
        for item in product_list:
            i = i + 1
            company = item['fullProviderName']
            if company == company_name:
                pro_name = item['fullName']
                from_service = item['from']
                list.append({
                    'id': i,
                    'company': company,
                    'keyword': keyword,
                    'page_num': page_num,
                    'ranking': i,
                    'pro_name': pro_name,
                    'page_url': '',
                    'from_service': from_service
                })
        return list


if __name__ == "__main__":
    R = Rank()
    res = R.rank('沈阳星烁电子科技有限公司', '显示屏')
    print(res)

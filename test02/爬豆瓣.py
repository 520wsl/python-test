import requests
import json

for i in range(0,40,20):
    url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={0}&limit=20".format(i)
    print(url)
    response = requests.get(url)
    if response.text == []:
        print("=========爬取结束++++++++++")
    py_data = json.loads(response.text)

    for i in py_data:
        # print(i)
        items = {
            "电影名称": i['title'],
            "电影评分": i['score'],
            "上映地区": i['regions'],
            "上映时间": i['release_date'],
            "评价数": i['vote_count'],
            "电影剧情": i['title']
        }
        print(items)
        content = json.dumps(items,ensure_ascii=False) + ",\n"

        with open("douban.json",'a',encoding="utf-8") as f:
            f.write(content)

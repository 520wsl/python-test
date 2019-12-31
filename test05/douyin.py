from flask import Flask, request, send_file
import requests
import json
import re

app = Flask(__name__)


# 只接受get方法访问
@app.route("/douyin/", methods=["GET"])
def check():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
    }
    # 默认返回内容
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_data = request.args.to_dict()
    url = get_data.get('url')

    # 获取接口参数
    html = requests.get(url=url, headers=headers)
    title = re.findall('itemId: "(.*?)",', html.text)[0]
    dytk = re.findall('dytk: "(.*?)" }', html.text)[0]

    # 拼接接口
    url_item = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + title + '&dytk=' + dytk

    # 获取抖音无水印视频链接
    html_item = requests.get(url=url_item, headers=headers)
    # 字符串转字典
    content = json.loads(html_item.text)

    # 获取视频相关的信息
    data = {}
    # 视频的描述
    data['videoDesc'] = content['item_list'][0]['desc']
    # 视频的封面图,小图
    data['dynamiCoverUrl'] = content['item_list'][0]['video']['dynamic_cover']['url_list'][0]
    # 视频的封面图,大图
    data['staticCoverUrl'] = content['item_list'][0]['video']['origin_cover']['url_list'][0]
    # 视频的评论数
    data['comments'] = content['item_list'][0]['statistics']['comment_count']
    # 视频的点赞数
    data['prise'] = content['item_list'][0]['statistics']['digg_count']

    print(data)
    print(content)

    # 视频接口
    url_video = content['item_list'][0]['video']['play_addr']['url_list'][1]
    response = requests.get(url_video, headers=headers, allow_redirects=True)

    # 获取重定向后的链接,这个也是无水印视频的下载链接,不过本次没用
    redirect = response.url
    # print(redirect)
    # 视频的下载链接
    # data['videoPlayAddr'] = redirect
    # 返回视频的信息
    # return_dict['result'] = data
    # 返回结果
    # return json.dumps(return_dict, ensure_ascii=False)

    video = requests.get(url=redirect, headers=headers).content
    video_name = "douyin.mp4"
    with open(video_name, 'wb') as f:
        f.write(video)
        f.flush()
    return send_file('douyin.mp4')


if __name__ == "__main__":
    # 本地调试
    # app.run(debug=True)
    # 部署上线
    app.run(host='127.0.0.1', port=443)
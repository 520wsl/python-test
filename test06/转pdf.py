import pdfkit

url = 'https://b2b.baidu.com/s?q=ppr&from=search'  # 一篇博客的url
confg = pdfkit.configuration(wkhtmltopdf='D:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
# 这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
# pdfkit.from_url(url, 'jmeter_下载文件.pdf', configuration=confg)
# from_url这个函数是从url里面获取内容
# 这有3个参数，第一个是url，第二个是文件名，第三个就是khtmltopdf的路径

pdfkit.from_file('C:/Users/39554/Desktop/【ppr】ppr价格_ppr批发_ppr厂家-百度爱采购.html', 'jmeter_下载文件2.pdf',configuration=confg)
# from_file这个函数是从文件里面获取内容
# 这有3个参数，第一个是一个html文件，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径

# html = '''
# <div>
# <h1>title</h1>
# <p>content</p>
# </div>
# '''  # 这个html是我从一个页面上拷下来的一段，也可以

# pdfkit.from_string(html, 'jmeter_下载文件3.pdf',configuration=confg)
# from_file这个函数是从一个字符串里面获取内容
# 这有3个参数，第一个是一个字符串，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径

one, two, three, four = 6, 5, 8, 10
print('  '*3+'狂龙钓鱼记录表')
print('|序号|'+'日期             |'+'鱼名 |'+'数量（条）|')
print('|1   |'+'2018年12月26日   |'+'鲫鱼 |'+'%d         |' % one)
print('|2   |'+'2018年12月28日   |'+'草鱼 |'+'%d         |' % two)
print('|3   |'+'2018年12月29日   |'+'章鱼 |'+'%d         |' % three)
print('|4   |'+'2018年12月30日   |'+'鲤鱼 |'+'%d        |' % four)
print('|合计：           %d + %d + %d + %d = %d 条|' %( one, two, three, four, one + two + three + four))

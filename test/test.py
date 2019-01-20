# _*_ coding:utf-8 _*_
#
#                              _ooOoo_
#                             o8888888o
#                             88" . "88
#                             (| -_- |)
#                             O\  =  /O
#                          ____/`---'\____
#                        .'  \\|     |//  `.
#                       /  \\|||  :  |||//  \
#                      /  _||||| -:- |||||-  \
#                      |   | \\\  -  /// |   |
#                      | \_|  ''\---/''  |   |
#                      \  .-\__  `-`  ___/-. /
#                    ___`. .'  /--.--\  `. . __
#                 ."" '<  `.___\_<|>_/___.'  >'"".
#                | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#                \  \ `-.   \_ __\ /__ _/   .-` /  /
#           ======`-.____`-.___\_____/___.-`____.-'======
#                              `=---='
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      佛祖保佑        永无BUG
#             佛曰:
#                    写字楼里写字间，写字间里程序员；
#                    程序人员写程序，又拿程序换酒钱。
#                    酒醒只在网上坐，酒醉还来网下眠；
#                    酒醉酒醒日复日，网上网下年复年。
#                    但愿老死电脑间，不愿鞠躬老板前；
#                    奔驰宝马贵者趣，公交自行程序员。
#                    别人笑我忒疯癫，我笑自己命太贱；
#                    不见满街漂亮妹，哪个归得程序员？
#
print("你好世界")
print("测试")
print("太酷了！^_^")
a = 1
n = 2
print(a)
name, name1, name2 = 'Tome', 'Jerry', "Search"
strA = "abcdefghijklmnopqrstuvwxyz"
print(name, name1, name2)
print(name[0])
print(name[1])
print(name[1:4])
print(name[:2])
print(name[1:])
print(name[:])
print(strA[::2])
print(strA[-1])
print(strA[-4:-1])
# print(name[13]) #string index out of range

# -------------------------

record = name + ',' + name2
print(record)

new_name = name[:2] + ' doge'
print(new_name)

del new_name
# print(new_name)

print(len(strA))

print('C:\back\name')
print(r'C:\back\name')

print('Cat' * 2)
age = 10
print("Tome's name is %d" % age)

print(5 / 3)
print(5 // 3)

print(10.0 / 3)

print(4.0 / 2.0)

print(True and True)
print(True or False)
print(not False)

print(0b1110)
print(bin(5))
print(bin(6))
print(bin(7))
print(bin(8))
print(bin(9))
print(bin(10))
print(bin(11))
print(bin(12))
print(bin(13))
print(bin(14))
print(bin(15))
print(bin(16))

print(int(3.2))
print(float(10))
print(type(10.0))
print(complex(2, 2))
print(hex(16))
print(ord('a'))
strB = 'abcde'
print(strB[2:])

print(bin(97))

print(0b11 ^ 0b00)

if True:
    print('OK')

if False:
    print("OK")
else:
    print("No")

i = 0

while i < 10:
    i += 1
    print(i)

fish_record = '鲫鱼5条、鲤鱼8条、鲢鱼7条、草鱼2条、黑鱼6条、乌龟1只'
a = 0
for var in fish_record:
    if var == '条':
        a = a + 1
        print(a)

for b in range(9):
    if b != 0:
        if b % 2 == 0:
            print('%d是偶数' % b)

for c in range(1, 5, 2):
    print(c)

if '乌龟' in fish_record:
    print('乌龟在字符串里')
else:
    print('乌龟没有在字符串里')

print(id(fish_record))

list1 = ['Tom', 1, 2.3, 1]
print(list1.index(1))
print(list1.index(1, 2))
# print(list1.index('a'))
print('a' in list1)
print(list1[2])

list1.clear()
print(len(list1))

team1 = ['张三', '李四', '王五']
team2 = ['Tom', 'Jack', 'John', '李四']

team1.extend(team2)

print(team1)

team1.sort()
print(team1)

new_team1 = team1.copy()
print(new_team1)
print(id(team1))
print(id(new_team1))

vegetable = ['白菜', '萝卜', '青菜', '芹菜', '花菜', '白菜']
print(vegetable.count('白菜'))

print(vegetable)
vegetable.reverse()
print(vegetable)

Nums = [i ** 2 for i in range(11) if i > 0]
print(Nums)

print((name, name1, name2))
print(name, name1, name2)

l_to_t = tuple(vegetable)
print((l_to_t))
print(type(l_to_t))

t_to_l = list(l_to_t)
print(t_to_l)
print(type(t_to_l))

dl = {
    'Tome': 10,
    'Jim': 5,
    'Mike': 11,
    'Jack': 12
}

for gets in dl:
    print(gets)

for gets in dl.keys():
    print(gets)

for keys in dl:
    print(dl[keys])

for get_v in dl.values():
    print(get_v)

if 'Tome' in dl.keys():
    print('Tome 在键集合内')
else:
    print('Tome 不在键集合内')

if 11 in dl.values():
    print('11 在键集合内')
else:
    print('11 不在键集合内')

print(dl.items())
if ("Mike", 11) in dl.items():
    print('("Mike", 11) 在键集合内')
else:
    print('("Mike", 11) 不在键集合内')

no1 = {'张三': 35.5, '李四': 200, '王五': 800}
no2 = {'Tom': 99.8, 'John': 183, 'Jim': 429}
no3 = {'阿毛': 12, '阿狗': 33}

rest = {'1 号': no1, '2 号': no2, '3 号': no3}
print(rest)

total = 0
for get_v in rest.values():
    total = total + sum(get_v.values())

print('餐厅今天营业额为：%.2f'%(total))
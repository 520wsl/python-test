#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Mad Dragon'
__mtime__ = '2019/1/20'
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
import time

import redis
import threading

# 工具类简单，如果是字节，转成str
from redis import StrictRedis


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if isinstance(s, bytes):
        return s.decode(encoding)
    return s


class RedisToo():
    def __init__(self):
        self.links = []
        self.pool = redis.ConnectionPool(host='192.168.2.202', port=6379, db=8)

    def target(self, numb):
        for i in range(int(numb)):
            link = r.lpop("list_name1")
            if link != None:
                link = str(link, 'utf-8')
                self.links.append(link)

    def getData(self):
        nloops = range(3)
        # self.logger.debug('threads:==>\n\t %s \n\t %s' % (nloops, taskList))

        threads = []
        for i in nloops:
            t = threading.Thread(target=self.target, args=('5'))
            threads.append(t)

        for i in nloops:
            threads[i].start()

        for i in nloops:
            threads[i].join()

    def setData(self):
        linkStr = ''
        links = ['http://www.xs8.cn/chapter/10419666104050403/27970454875239101',
                 'http://www.xs8.cn/chapter/10419666104050403/27971046525066095',
                 'http://www.xs8.cn/chapter/10419666104050403/27974185613957043',
                 'http://www.xs8.cn/chapter/10419667504050703/27970161765144378',
                 'http://www.xs8.cn/chapter/10419667504050703/27970887865902049',
                 'http://www.xs8.cn/chapter/10419667504050703/28017711619628243',
                 'http://www.xs8.cn/chapter/10419667504050703/28049403636729897',
                 'http://www.xs8.cn/chapter/10419667504050703/28049464558322799',
                 'http://www.xs8.cn/chapter/10419667504050703/28061038697967875',
                 'http://www.xs8.cn/chapter/10419667504050703/28061038703334037',
                 'http://www.xs8.cn/chapter/10419667504050703/28061038971802330',
                 'http://www.xs8.cn/chapter/10419667504050703/28061039794045571',
                 'http://www.xs8.cn/chapter/10419667504050703/28061040045720868',
                 'http://www.xs8.cn/chapter/10419667504050703/28126208670369736',
                 'http://www.xs8.cn/chapter/10419667504050703/28132572722689601',
                 'http://www.xs8.cn/chapter/10419667504050703/28132576493508279',
                 'http://www.xs8.cn/chapter/10419667504050703/28178935813415553',
                 'http://www.xs8.cn/chapter/10419667504050703/28178941199589098',
                 'http://www.xs8.cn/chapter/10419667504050703/28178944428951467',
                 'http://www.xs8.cn/chapter/10419667504050703/28178948439172923',
                 'http://www.xs8.cn/chapter/10419667504050703/28178952475379359',
                 'http://www.xs8.cn/chapter/10419667504050703/28178955948871187',
                 'http://www.xs8.cn/chapter/10419667504050703/28178959170491331',
                 'http://www.xs8.cn/chapter/10419667504050703/28336505297470113',
                 'http://www.xs8.cn/chapter/10419667504050703/28336507982048901',
                 'http://www.xs8.cn/chapter/10419667504050703/28336512798156345',
                 'http://www.xs8.cn/chapter/10419667504050703/28336516305185933',
                 'http://www.xs8.cn/chapter/10419667504050703/28336519241549044',
                 'http://www.xs8.cn/chapter/10419667504050703/28336523268577104',
                 'http://www.xs8.cn/chapter/10419667504050703/28336526222213856',
                 'http://www.xs8.cn/chapter/10419667504050703/28336529175309568',
                 'http://www.xs8.cn/chapter/10419667504050703/28336534812406453',
                 'http://www.xs8.cn/chapter/10419667504050703/28336540468075449',
                 'http://www.xs8.cn/chapter/10419667504050703/28336546104706713',
                 'http://www.xs8.cn/chapter/10419667504050703/28584762457234234',
                 'http://www.xs8.cn/chapter/10419667504050703/28608226121734528',
                 'http://www.xs8.cn/chapter/10419667504050703/28608227215240135',
                 'http://www.xs8.cn/chapter/10419667504050703/28608227735365271',
                 'http://www.xs8.cn/chapter/10419667504050703/28608228289061626',
                 'http://www.xs8.cn/chapter/10419667504050703/28608231759186329',
                 'http://www.xs8.cn/chapter/10419667504050703/28608233104492360',
                 'http://www.xs8.cn/chapter/10419667504050703/28608240618116800',
                 'http://www.xs8.cn/chapter/10419667504050703/28608244644952811',
                 'http://www.xs8.cn/chapter/10419667504050703/28608244930212767',
                 'http://www.xs8.cn/chapter/10419667504050703/28736523254895112',
                 'http://www.xs8.cn/chapter/10419667504050703/28736526724124921',
                 'http://www.xs8.cn/chapter/10419667504050703/28736530767545097',
                 'http://www.xs8.cn/chapter/10419667504050703/28736534794348254',
                 'http://www.xs8.cn/chapter/10419667504050703/28736538552665604',
                 'http://www.xs8.cn/chapter/10419667504050703/28815599234127834',
                 'http://www.xs8.cn/chapter/10419667504050703/28815603529473464',
                 'http://www.xs8.cn/chapter/10419667504050703/28815607825339711',
                 'http://www.xs8.cn/chapter/10419667504050703/28815611031580800',
                 'http://www.xs8.cn/chapter/10419667504050703/29081360543130257',
                 'http://www.xs8.cn/chapter/10419667504050703/29081371550113417',
                 'http://www.xs8.cn/chapter/10419667504050703/29081376114448234',
                 'http://www.xs8.cn/chapter/10419667504050703/29081627370146918',
                 'http://www.xs8.cn/chapter/10419667504050703/29200083890733806',
                 'http://www.xs8.cn/chapter/10419667504050703/29200084167504865',
                 'http://www.xs8.cn/chapter/10419667504050703/29200084444475458',
                 'http://www.xs8.cn/chapter/10419667504050703/29200084687655618',
                 'http://www.xs8.cn/chapter/10419667504050703/29200085224645680',
                 'http://www.xs8.cn/chapter/10419667504050703/29200085501650738',
                 'http://www.xs8.cn/chapter/10419667504050703/30381712350761888',
                 'http://www.xs8.cn/chapter/10419667504050703/30381839047671949',
                 'http://www.xs8.cn/chapter/10419667504050703/32029168929022106',
                 'http://www.xs8.cn/chapter/10419769603977603/27970374349187890',
                 'http://www.xs8.cn/chapter/10419823504071203/27971670914801857',
                 'http://www.xs8.cn/chapter/10419823504071203/27971779342544172',
                 'http://www.xs8.cn/chapter/10419823504071203/27988207881364764',
                 'http://www.xs8.cn/chapter/10419823504071203/28005173783707501',
                 'http://www.xs8.cn/chapter/10419823504071203/28029994666955119',
                 'http://www.xs8.cn/chapter/10419823504071203/28063232100265284',
                 'http://www.xs8.cn/chapter/10419823504071203/28073864286822034',
                 'http://www.xs8.cn/chapter/10419823504071203/28086333659498668',
                 'http://www.xs8.cn/chapter/10419823504071203/28155173105537716',
                 'http://www.xs8.cn/chapter/10419823504071203/28156009019898656',
                 'http://www.xs8.cn/chapter/10419823504071203/28193337108265037',
                 'http://www.xs8.cn/chapter/10419823504071203/28200976785213572',
                 'http://www.xs8.cn/chapter/10419823504071203/28236338602769603',
                 'http://www.xs8.cn/chapter/10419823504071203/28248431625061001',
                 'http://www.xs8.cn/chapter/10419823504071203/28268801568276322',
                 'http://www.xs8.cn/chapter/10419823504071203/28270632838050392',
                 'http://www.xs8.cn/chapter/10419823504071203/28282214204948257',
                 'http://www.xs8.cn/chapter/10419823504071203/28291568921885745',
                 'http://www.xs8.cn/chapter/10419823504071203/28294732440177290',
                 'http://www.xs8.cn/chapter/10419823504071203/28311070767135729',
                 'http://www.xs8.cn/chapter/10419823504071203/28316709785312726',
                 'http://www.xs8.cn/chapter/10419823504071203/28316763754623443',
                 'http://www.xs8.cn/chapter/10419823504071203/28335757445199557',
                 'http://www.xs8.cn/chapter/10419823504071203/28361346051723471',
                 'http://www.xs8.cn/chapter/10419823504071203/28383147819974842',
                 'http://www.xs8.cn/chapter/10419823504071203/28401373803090547',
                 'http://www.xs8.cn/chapter/10419823504071203/28406248027526326',
                 'http://www.xs8.cn/chapter/10419823504071203/28406251547204172',
                 'http://www.xs8.cn/chapter/10419823504071203/28406270040883806',
                 'http://www.xs8.cn/chapter/10419823504071203/28479307300041447',
                 'http://www.xs8.cn/chapter/10419823504071203/28479599639243709',
                 'http://www.xs8.cn/chapter/10419823504071203/28479610928156025',
                 'http://www.xs8.cn/chapter/10419823504071203/28502274106113332',
                 'http://www.xs8.cn/chapter/10419823504071203/28524078605899993',
                 'http://www.xs8.cn/chapter/10419823504071203/28639145867293614',
                 'http://www.xs8.cn/chapter/10419823504071203/28639156868952268',
                 'http://www.xs8.cn/chapter/10419823504071203/28657767248172770',
                 'http://www.xs8.cn/chapter/10419823504071203/28661459298223037',
                 'http://www.xs8.cn/chapter/10419823504071203/28708371334266032',
                 'http://www.xs8.cn/chapter/10419823504071203/28728720089435813',
                 'http://www.xs8.cn/chapter/10419823504071203/28803341137423645',
                 'http://www.xs8.cn/chapter/10419823504071203/28865714769756504',
                 'http://www.xs8.cn/chapter/10419823504071203/28869846813453182',
                 'http://www.xs8.cn/chapter/10419823504071203/28869857820731095',
                 'http://www.xs8.cn/chapter/10419823504071203/28961251784214210',
                 'http://www.xs8.cn/chapter/10419823504071203/28961264133416566',
                 'http://www.xs8.cn/chapter/10419823504071203/28961273778324628',
                 'http://www.xs8.cn/chapter/10419823504071203/28961284802848924',
                 'http://www.xs8.cn/chapter/10419823504071203/29077721080701737',
                 'http://www.xs8.cn/chapter/10419823504071203/29104329493108251',
                 'http://www.xs8.cn/chapter/10419823504071203/29121316869741628',
                 'http://www.xs8.cn/chapter/10419823504071203/29128356058672383',
                 'http://www.xs8.cn/chapter/10419823504071203/29143169666279003',
                 'http://www.xs8.cn/chapter/10419823504071203/29189980509835685',
                 'http://www.xs8.cn/chapter/10419823504071203/29195009944879326',
                 'http://www.xs8.cn/chapter/10419823504071203/29241558242862163',
                 'http://www.xs8.cn/chapter/10419823504071203/29264956679577747',
                 'http://www.xs8.cn/chapter/10419823504071203/29286338114493261',
                 'http://www.xs8.cn/chapter/10419823504071203/29289058167487251',
                 'http://www.xs8.cn/chapter/10419823504071203/29305864370661364',
                 'http://www.xs8.cn/chapter/10419823504071203/29312092082013829',
                 'http://www.xs8.cn/chapter/10419823504071203/29314968885509052',
                 'http://www.xs8.cn/chapter/10419823504071203/29406310504481770',
                 'http://www.xs8.cn/chapter/10419823504071203/29447019553140265',
                 'http://www.xs8.cn/chapter/10419823504071203/29469917630282619',
                 'http://www.xs8.cn/chapter/10419823504071203/29495957494104654',
                 'http://www.xs8.cn/chapter/10419823504071203/29518788191796232',
                 'http://www.xs8.cn/chapter/10419823504071203/29542380986839744',
                 'http://www.xs8.cn/chapter/10419823504071203/29564296573473799',
                 'http://www.xs8.cn/chapter/10419865104077003/27971435482281670',
                 'http://www.xs8.cn/chapter/10419865104077003/28199528839541725',
                 'http://www.xs8.cn/chapter/10419872803992603/28540148222049697',
                 'http://www.xs8.cn/chapter/10419884203993903/27970694338082299',
                 'http://www.xs8.cn/chapter/10419884203993903/28030692078135492',
                 'http://www.xs8.cn/chapter/10419884203993903/28030713286620331',
                 'http://www.xs8.cn/chapter/10419884203993903/28053571914547036',
                 'http://www.xs8.cn/chapter/10419884203993903/28053594186553089',
                 'http://www.xs8.cn/chapter/10419884203993903/28074903948032796',
                 'http://www.xs8.cn/chapter/10419884203993903/28080216805383129',
                 'http://www.xs8.cn/chapter/10419884203993903/28098838990801724',
                 'http://www.xs8.cn/chapter/10419884203993903/28104259500744972',
                 'http://www.xs8.cn/chapter/10419884203993903/28121426487398229',
                 'http://www.xs8.cn/chapter/10419884203993903/28126187445766788',
                 'http://www.xs8.cn/chapter/10419884203993903/28144524291246655',
                 'http://www.xs8.cn/chapter/10419884203993903/28149247123067864',
                 'http://www.xs8.cn/chapter/10419884203993903/28167503964393335',
                 'http://www.xs8.cn/chapter/10419884203993903/28169319123732046',
                 'http://www.xs8.cn/chapter/10419884203993903/28189875374154760',
                 'http://www.xs8.cn/chapter/10419884203993903/28194923046272893',
                 'http://www.xs8.cn/chapter/10419884203993903/28213454756727083',
                 'http://www.xs8.cn/chapter/10419884203993903/28218739425232125',
                 'http://www.xs8.cn/chapter/10419884203993903/28228989389068637',
                 'http://www.xs8.cn/chapter/10419884203993903/28241442636318069',
                 'http://www.xs8.cn/chapter/10419884203993903/28260610813049504',
                 'http://www.xs8.cn/chapter/10419884203993903/28265391643921450',
                 'http://www.xs8.cn/chapter/10419884203993903/28281743099728851',
                 'http://www.xs8.cn/chapter/10419884203993903/28288775306908732',
                 'http://www.xs8.cn/chapter/10419884203993903/28307497353095020',
                 'http://www.xs8.cn/chapter/10419884203993903/28312232811916775',
                 'http://www.xs8.cn/chapter/10419884203993903/28329281154962916',
                 'http://www.xs8.cn/chapter/10419884203993903/28337750009267572',
                 'http://www.xs8.cn/chapter/10419884203993903/28352128758893779',
                 'http://www.xs8.cn/chapter/10419884203993903/28357712494927914',
                 'http://www.xs8.cn/chapter/10419884203993903/28376143803626389',
                 'http://www.xs8.cn/chapter/10419884203993903/28382777405482373',
                 'http://www.xs8.cn/chapter/10419884203993903/28399814195807876',
                 'http://www.xs8.cn/chapter/10419884203993903/28403424384127732',
                 'http://www.xs8.cn/chapter/10419884203993903/28422772658413649',
                 'http://www.xs8.cn/chapter/10419884203993903/28428592862801182',
                 'http://www.xs8.cn/chapter/10419884203993903/28446472542659929',
                 'http://www.xs8.cn/chapter/10419884203993903/28451348138196059',
                 'http://www.xs8.cn/chapter/10419884203993903/28470886491275047',
                 'http://www.xs8.cn/chapter/10419884203993903/28475544103142060',
                 'http://www.xs8.cn/chapter/10419884203993903/28492363760685821',
                 'http://www.xs8.cn/chapter/10419884203993903/28497931366209400',
                 'http://www.xs8.cn/chapter/10419884203993903/28513158102384641',
                 'http://www.xs8.cn/chapter/10419884203993903/28517671291010005',
                 'http://www.xs8.cn/chapter/10419884203993903/28539203036630366',
                 'http://www.xs8.cn/chapter/10419884203993903/28543747669228736',
                 'http://www.xs8.cn/chapter/10419884203993903/28561739019610256',
                 'http://www.xs8.cn/chapter/10419884203993903/28566788286848639',
                 'http://www.xs8.cn/chapter/10419884203993903/28567890484463160',
                 'http://www.xs8.cn/chapter/10419884203993903/28567939320032072',
                 'http://www.xs8.cn/chapter/10419884203993903/28574334823647554',
                 'http://www.xs8.cn/chapter/10419884203993903/28590002834289378',
                 'http://www.xs8.cn/chapter/10419884203993903/28595836221544724',
                 'http://www.xs8.cn/chapter/10419884203993903/28596264122614965',
                 'http://www.xs8.cn/chapter/10419884203993903/28610173368991967',
                 'http://www.xs8.cn/chapter/10419884203993903/28610830744213873',
                 'http://www.xs8.cn/chapter/10419884203993903/28656501828020861',
                 'http://www.xs8.cn/chapter/10419884203993903/28658177674572556',
                 'http://www.xs8.cn/chapter/10419884203993903/28658760724167619',
                 'http://www.xs8.cn/chapter/10419884203993903/28659813792495778',
                 'http://www.xs8.cn/chapter/10419884203993903/28664188468646046',
                 'http://www.xs8.cn/chapter/10419884203993903/28668071681052788',
                 'http://www.xs8.cn/chapter/10419884203993903/28689689572174391',
                 'http://www.xs8.cn/chapter/10419884203993903/28707402289048459',
                 'http://www.xs8.cn/chapter/10419884203993903/28716279722294458',
                 'http://www.xs8.cn/chapter/10419884203993903/28716546827718753',
                 'http://www.xs8.cn/chapter/10419884203993903/28751258468737349',
                 'http://www.xs8.cn/chapter/10419884203993903/28752818891999323',
                 'http://www.xs8.cn/chapter/10419884203993903/28783914720707254',
                 'http://www.xs8.cn/chapter/10419884203993903/28786032927220808',
                 'http://www.xs8.cn/chapter/10419884203993903/28798894211649742',
                 'http://www.xs8.cn/chapter/10419884203993903/28819741720040774',
                 'http://www.xs8.cn/chapter/10419884203993903/28844488265489031',
                 'http://www.xs8.cn/chapter/10419884203993903/28848762834307622',
                 'http://www.xs8.cn/chapter/10419884203993903/28867677862895581',
                 'http://www.xs8.cn/chapter/10419884203993903/28873837628810699',
                 'http://www.xs8.cn/chapter/10419884203993903/28875225183927816',
                 'http://www.xs8.cn/chapter/10419884203993903/28887876553115395',
                 'http://www.xs8.cn/chapter/10419884203993903/28891697732306213',
                 'http://www.xs8.cn/chapter/10419884203993903/28912422291434781',
                 'http://www.xs8.cn/chapter/10419884203993903/28937303297819926',
                 'http://www.xs8.cn/chapter/10419884203993903/28938674741110747',
                 'http://www.xs8.cn/chapter/10419884203993903/28943650462887099',
                 'http://www.xs8.cn/chapter/10419884203993903/28965415994893565',
                 'http://www.xs8.cn/chapter/10419884203993903/28968299824032242',
                 'http://www.xs8.cn/chapter/10419884203993903/28988241623533601',
                 'http://www.xs8.cn/chapter/10419884203993903/28990875510188401',
                 'http://www.xs8.cn/chapter/10419884203993903/29012490983436197',
                 'http://www.xs8.cn/chapter/10419884203993903/29019496642326147',
                 'http://www.xs8.cn/chapter/10419884203993903/29019563751994323',
                 'http://www.xs8.cn/chapter/10419884203993903/29037643124247438',
                 'http://www.xs8.cn/chapter/10419884203993903/29037672385835992',
                 'http://www.xs8.cn/chapter/10419884203993903/29039189861025274',
                 'http://www.xs8.cn/chapter/10419884203993903/29039847003524846',
                 'http://www.xs8.cn/chapter/10419884203993903/29077134281955133',
                 'http://www.xs8.cn/chapter/10419884203993903/29077167554663795',
                 'http://www.xs8.cn/chapter/10419884203993903/29078823010003126',
                 'http://www.xs8.cn/chapter/10419884203993903/29085624107272817',
                 'http://www.xs8.cn/chapter/10419884203993903/29133939238609777',
                 'http://www.xs8.cn/chapter/10419884203993903/29150789493350747',
                 'http://www.xs8.cn/chapter/10419884203993903/29165255992676093',
                 'http://www.xs8.cn/chapter/10419884203993903/29166659107858464',
                 'http://www.xs8.cn/chapter/10419884203993903/29168849821877558',
                 'http://www.xs8.cn/chapter/10419884203993903/29189523920158680',
                 'http://www.xs8.cn/chapter/10419884203993903/29191402949286454',
                 'http://www.xs8.cn/chapter/10419884203993903/29213163412018803',
                 'http://www.xs8.cn/chapter/10419884203993903/29221904479705172',
                 'http://www.xs8.cn/chapter/10419884203993903/29236284557043598',
                 'http://www.xs8.cn/chapter/10419884203993903/29237997722179275',
                 'http://www.xs8.cn/chapter/10419884203993903/29238942613036958',
                 'http://www.xs8.cn/chapter/10419989203007303/28005071533539671',
                 'http://www.xs8.cn/chapter/10419989203007303/28165549754336486',
                 'http://www.xs8.cn/chapter/10419993503007803/28053602491839379',
                 'http://www.xs8.cn/chapter/10419993503007803/28222923254417701',
                 'http://www.xs8.cn/chapter/10419993503007803/28294665335136360',
                 'http://www.xs8.cn/chapter/10419993503007803/28502662818207289',
                 'http://www.xs8.cn/chapter/10419993503007803/28527434045778940',
                 'http://www.xs8.cn/chapter/10419993503007803/28554783046552260',
                 'http://www.xs8.cn/chapter/10419993503007803/28600362036167203',
                 'http://www.xs8.cn/chapter/10419993503007803/28609084579221792',
                 'http://www.xs8.cn/chapter/10419993503007803/28642022690369636',
                 'http://www.xs8.cn/chapter/10419993503007803/28654739550228800',
                 'http://www.xs8.cn/chapter/10419993503007803/28665404235098366',
                 'http://www.xs8.cn/chapter/10419993503007803/28697515810011445',
                 'http://www.xs8.cn/chapter/10419993503007803/28710415216256557',
                 'http://www.xs8.cn/chapter/10419993503007803/28732830107972251',
                 'http://www.xs8.cn/chapter/10419993503007803/28759945840373908',
                 'http://www.xs8.cn/chapter/10419993503007803/28780180766530663',
                 'http://www.xs8.cn/chapter/10419993503007803/28800591011072376',
                 'http://www.xs8.cn/chapter/10419993503007803/28828313955502297',
                 'http://www.xs8.cn/chapter/10419993503007803/28851354818239687',
                 'http://www.xs8.cn/chapter/10419993503007803/28893392641234468',
                 'http://www.xs8.cn/chapter/10419993503007803/28911768914321439',
                 'http://www.xs8.cn/chapter/10419993503007803/28923334991003872',
                 'http://www.xs8.cn/chapter/10419993503007803/28944665933641164',
                 'http://www.xs8.cn/chapter/10419993503007803/28969902369243925',
                 'http://www.xs8.cn/chapter/10419993503007803/28969949867885929',
                 'http://www.xs8.cn/chapter/10419993503007803/28972931137694197',
                 'http://www.xs8.cn/chapter/10419993503007803/29020473996326136',
                 'http://www.xs8.cn/chapter/10419993503007803/29037883119814307',
                 'http://www.xs8.cn/chapter/10419993503007803/29058799855868168',
                 'http://www.xs8.cn/chapter/10419993503007803/29082843369829548',
                 'http://www.xs8.cn/chapter/10419993503007803/29106380065126654',
                 'http://www.xs8.cn/chapter/10419993503007803/29129832443657583',
                 'http://www.xs8.cn/chapter/10419993503007803/29153122733023277',
                 'http://www.xs8.cn/chapter/10419993503007803/29179104862911810',
                 'http://www.xs8.cn/chapter/10419993503007803/29198547089307248',
                 'http://www.xs8.cn/chapter/10419993503007803/29243527741367610',
                 'http://www.xs8.cn/chapter/10419993503007803/29245275010940973',
                 'http://www.xs8.cn/chapter/10419993503007803/29269280658529683',
                 'http://www.xs8.cn/chapter/10419993503007803/29302545452147499',
                 'http://www.xs8.cn/chapter/10419993503007803/29315444302588081',
                 'http://www.xs8.cn/chapter/10419993503007803/29360083244486182',
                 'http://www.xs8.cn/chapter/10419993503007803/29363170513779075',
                 'http://www.xs8.cn/chapter/10419993503007803/29365811383305417',
                 'http://www.xs8.cn/chapter/10419993503007803/29406524977425737',
                 'http://www.xs8.cn/chapter/10419993503007803/29431981808144701',
                 'http://www.xs8.cn/chapter/10419993503007803/29502104105117717',
                 'http://www.xs8.cn/chapter/10419993503007803/29544269705162184',
                 'http://www.xs8.cn/chapter/10419993503007803/29592486594174654',
                 'http://www.xs8.cn/chapter/10419993503007803/29617189919326788',
                 'http://www.xs8.cn/chapter/10419993503007803/29639869743556105',
                 'http://www.xs8.cn/chapter/10419993503007803/29663747889667930',
                 'http://www.xs8.cn/chapter/10419993503007803/29709650910625804',
                 'http://www.xs8.cn/chapter/10419993503007803/29755506655852446',
                 'http://www.xs8.cn/chapter/10419993503007803/29779526783685885',
                 'http://www.xs8.cn/chapter/10419993503007803/29825220950195082',
                 'http://www.xs8.cn/chapter/10419993503007803/31288718980534073',
                 'http://www.xs8.cn/chapter/10419993503007803/31495469851821763',
                 'http://www.xs8.cn/chapter/10419993503007803/32516117269829302',
                 'http://www.xs8.cn/chapter/10419993503007803/32539298818184666',
                 'http://www.xs8.cn/chapter/10419993503007803/32560525097842559',
                 'http://www.xs8.cn/chapter/10419993503007803/32578980564476808',
                 'http://www.xs8.cn/chapter/10419993503007803/32600257852179523',
                 'http://www.xs8.cn/chapter/10419993503007803/32625280576119969',
                 'http://www.xs8.cn/chapter/10419993503007803/32656195224263053',
                 'http://www.xs8.cn/chapter/10419993503007803/32670308231523252',
                 'http://www.xs8.cn/chapter/10419993503007803/32695694432305143',
                 'http://www.xs8.cn/chapter/10419993503007803/32714397678496495',
                 'http://www.xs8.cn/chapter/10419993503007803/32724510155110172',
                 'http://www.xs8.cn/chapter/10419993503007803/32757148973414014',
                 'http://www.xs8.cn/chapter/10419993503007803/32769562231745090',
                 'http://www.xs8.cn/chapter/10419993503007803/32778503281010195',
                 'http://www.xs8.cn/chapter/10419993503007803/32801287279731854',
                 'http://www.xs8.cn/chapter/10419993503007803/32809300611637055',
                 'http://www.xs8.cn/chapter/10419993503007803/32854361267353091',
                 'http://www.xs8.cn/chapter/10419993503007803/32875679596326259',
                 'http://www.xs8.cn/chapter/10419993503007803/32924155546145175',
                 'http://www.xs8.cn/chapter/10419993503007803/32940458977906128',
                 'http://www.xs8.cn/chapter/10419993503007803/32961005830105737',
                 'http://www.xs8.cn/chapter/10419993503007803/33003371644873958',
                 'http://www.xs8.cn/chapter/10419993503007803/33046472982981033',
                 'http://www.xs8.cn/chapter/10419993503007803/33071446071509843',
                 'http://www.xs8.cn/chapter/10419993503007803/33094894728980252',
                 'http://www.xs8.cn/chapter/10419993503007803/33118998903377550',
                 'http://www.xs8.cn/chapter/10419993503007803/33137207952539568',
                 'http://www.xs8.cn/chapter/10420291403034503/27972210719615201',
                 'http://www.xs8.cn/chapter/10420291403034503/27973815418189679',
                 'http://www.xs8.cn/chapter/10420291403034503/27974470947736483']

        r.rpush("list_name1", *links)
        print(r.llen("list_name1"))


if __name__ == '__main__':
    redisToo = RedisToo()
    r = redis.Redis(connection_pool=redisToo.pool)
    # r.set('name', 'zhangsan123')   #添加
    # r.lpush("list_name1",1,2,3,4,5,6,7,8,9)
    # print(r.lrange("list_name1",0,5))
    # print (r.get('name'))   #获取

    # print(r.lpop("list_name1"))
    # print(r.llen("list_name1"))
    # redisToo.setData()
    redisToo.getData()
    print(redisToo.links)
    # for item in redisToo.links:
    #    print(item)
    # linkStr = ''
    # for item in redisToo.links:
    #     linkStr += "'%s'," % item
    #
    # print(linkStr)
    # r=StrictRedis()
    # result = r.set('name', 'itheima')
    # print(result)

from pybase import databaseOperator

host = '127.0.0.1'
user = 'ks1'
psd = '1sk'
db = 'KS1'
a = databaseOperator.sqlOperator(host, user, psd, db)
a.active()


def parseData(dic):
    d1 = dic[1][0]
    d3 = dic[3][0]
    d4 = dic[4][0]
    ret = ''
    ret += '时间戳:%s ' % d1['sendTime']
    ret += '防护区:%d 控制状态:%s\n' % (d1['AREA'], '自动' if d3['auto'] == True else '手动')
    ret += '警报数量:%d 故障数量:%d 探测器数量:%d 灭火器数量: %d' %(d1['JBnum'], d1['GZnum'], d1['Fnum'], len(dic[5]))
    ret += '喷洒状态:%s\n' % ('正在喷洒' if d3['rain'] == True else '未喷洒')
    ret += '分区环境信息:\n'
    ret += '温度: %.3f摄氏度 CO: %.3f%% VOC: %.3fg/L 烟雾:%.3fmg/m^3\n' % (d4['oc'], d4['co'], d4['voc'], d4['fog'])
    ret += '故障机器号:'
    if len(dic[2]) == 0:
        ret += '(无故障机器)'
    for each in dic[2]:
        ret += each['id'] + ' '
    ret += '\n'
    return ret


print(parseData(a.select_newest('1')))
    
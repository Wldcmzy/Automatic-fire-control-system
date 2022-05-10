from pybase import dataSR
from pybase import dataformer

df = dataformer.DataFormer()
sr = dataSR.SR()
sr.receive()

while True:
    address = ''
    data = sr.getData()
    if data != None:
        data, address = data
        data = df.parseReport(data)
        data, dic = data
        print('接收到消息 Fcode:%#X ID:%d' % (dic['Fcode'], dic['id']))
        if data == dataformer.DataFormer._ReportError_unkn:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['unkn'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_unkn)
        elif data == dataformer.DataFormer._ReportError_read:
            data = None
            print('消息接受出错:', dataformer.DataFormer._ReportError_read)
        elif data == dataformer.DataFormer._ReportError_crce:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['crce'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_crce)
        elif data == dataformer.DataFormer._ReportError_func:
            data = df.formReplay(dic['Fcode'], dic['id'], True, dataformer.DataFormer._dicErr2Num['func'])
            print('消息接受出错:', dataformer.DataFormer._ReportError_func)
        else:
            # sql
            #
            print(data)
            print('消息正确接受,并存入数据库...')
            data = df.formReplay(dic['Fcode'], dic['id'], False, 0)

        if data != None:
            sr.send(data, address)
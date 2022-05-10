import json

class DataFormer:
    _ReportError_read = '__DataFormer_report_read_error___@_'
    _ReportError_func = '__DataFormer_report_func_error___@_'
    _ReportError_unkn = '__DataFormer_report_unkn_error___@_'
    _ReportError_crce = '__DataFormer_report_crce_error___@_'
    _ReportError_dis_crce = '__DataFormer_report_dis_crce_error___@_'
    _dicErr2Num = { 'unkn' : 0xaa, 'crce' : 0xe0, 'func' : 0x11 }
    _dicMch2Num = {'oc' : 1, 'co' : 2, 'voc' : 3, 'fog' : 4, 'fireEnder' : 5}
    _dicNum2Mch = {1 : 'oc', 2 : 'co', 3 : 'voc', 4 : 'fog', 5 : 'fireEnder'}
    _dicMtype2Chr = {'Light' : chr(0x00) + chr(0x00), 'Normal' : chr(0x00) + chr(0x01)}
    _dicChr2Mtype = {chr(0x00) + chr(0x00) : 'Light', chr(0x00) + chr(0x01) : 'Normal'}
    _testdata = json.loads('{"fes":{"number":4,"values":[{"id":"101","work":false,"error":true},{"id":"102","work":false,"error":true},{"id":"103","work":false,"error":true},{"id":"104","work":false,"error":false}]},"fs":{"numJB":"0","FeelerNumber":"4","oc":{"id":"201","value":"25","error":true},"co":{"id":"202","value":"0.1","error":false},"voc":{"id":"203","value":"20","error":false},"fog":{"id":"204","value":"0.01","error":true}},"fq":{"area":"1","JBlevel":"0","Mid":"1","Mtype":"Light","auto":true,"start":false,"shutdown":false,"rain":false,"startRain":false}}')
    _report05fail = chr(0xa0) + chr(0x01) + chr(0x01) + chr(0x00)
    _report04fail = chr(0x90) + chr(0x01) + chr(0x01) + chr(0x00)
    _report03fail = chr(0x80) + chr(0x01) + chr(0x01) + chr(0x00)
    _report02fail = chr(0x70) + chr(0x01) + chr(0x01) + chr(0x00) 
    _report01fail = chr(0x60) + chr(0x01) + chr(0x01) + chr(0x00) 
    _Fcodes = (0x60, 0x70, 0x80, 0x90, 0xa0)
    def __init__(self):
        self.dic = {}

    def Snum2ChrBit16(self, num):
        num = int(num)
        return chr((num >> 8) & 0xff) + chr(num & 0xff)

    #精度保留三位小数
    def Sfloat2ChrBit16(self, num):
        return self.Snum2ChrBit16(float(num) * 1000)

    def SBit16toNum(self, data):
        return (ord(data[0]) << 8) + ord(data[1])
    
    def SBit16toFloat(self, data):
        return self.SBit16toNum(data) / 1000

    def Snum2ChrBit8(self, num):
        return chr(int(num))
    
    def SBit8toNum(self, data):
        return ord(data)

    def setDic(self, dic):
        if type(dic) == str:
            dic = json.loads(dic)
        self.dic = dic

    def parseReplay(self, data):
        crc = ord(data[-2])
        crc_new = self.crc8(data[ : -2] + data[-1])
        if crc != crc_new:
            return DataFormer._ReportError_crce
        else:
            Fcode = ord(data[5])
            err = ord(data[6])
            if err == 0x7f:
                errType = ord(data[7])
                print(errType, err, Fcode)
                if errType == 0x11:
                    return (Fcode, DataFormer._ReportError_func)
                else:
                    return (Fcode, DataFormer._ReportError_dis_crce)
        return (Fcode, None)

    def parseReport(self, data):
        ret = DataFormer._ReportError_unkn
        crc = ord(data[-2])
        crc_now = self.crc8(data[ : -2] + data[-1])
        id = ord(data[4])
        Fcode = ord(data[5])
        head = data[ : 2]
        tail = data[-1]
        leng = self.SBit16toNum(data[2 : 4])
        if crc_now != crc:
            return DataFormer._ReportError_crce
        elif Fcode not in DataFormer._Fcodes:
            return DataFormer._ReportError_func
        elif head != 'QN' or tail != 'E' or leng != len(data):
            return DataFormer._ReportError_unkn
        else:
            info = data[8 : -2]
            if Fcode == 0x60:
                ret = self.parseReport01(info)
            elif Fcode == 0x70:
                ret = self.parseReport02(info)
            elif Fcode == 0x80:
                ret = self.parseReport03(info)
            elif Fcode == 0x90:
                ret = self.parseReport04(info)
            elif Fcode == 0xa0:
                ret = self.parseReport05(info)
        return (ret, {'Fcode' : Fcode, 'id' : id})

    def formReplay(self, Fcode, id, err, val):
        ret = 'QN'
        ret += chr(0) + chr(9)
        ret += chr(id)
        ret += chr(Fcode)
        ret += chr(0x7f) if err == True else chr(Fcode)
        ret += chr(0) if err == False else chr(val)
        ret += 'E'
        crc = self.crc8(ret)
        ret = ret[ : -1] + chr(crc) + ret[-1]
        return ret

    def formReport(self):
        lst = [
            self.wapperOfFormReport(0x60, self.formReport01()), 
            self.wapperOfFormReport(0x70, self.formReport02()), 
            self.wapperOfFormReport(0x80, self.formReport03()), 
            self.wapperOfFormReport(0x90, self.formReport04()), 
            self.wapperOfFormReport(0xa0, self.formReport05()), 
        ]
        return lst

    def crc8(self, data):
        N = 8
        loc = [8, 2, 1, 0]
        p = [0 for i in range(N + 1)]
        for i in loc: p[i] = 1

        info = []
        for ch in data:
            tmp = []
            ch = ord(ch)
            for i in range(8):
                tmp.append(ch & 1)
                ch >>= 1
            info.extend(tmp[ : : -1])

        leng = len(info)
        n = N + 1
        for i in range(N):
            info.append(0)
        
        for i in range(leng):
            if info[i] == 1:
                for j in range(n):
                    info[j + i] = info[j + i] ^ p[j]

        yu = info[-N::]

        ret = 0
        for each in yu:
            ret <<= 1
            ret |= each

        return ret

    def wapperOfFormReport(self, Funcode, txt):
        fq = self.dic['fq']
        assert 'Mid' in fq
        success = True if ord(txt[1]) == 0x00 else False
        length = 10 + len(txt)
        Mid = fq['Mid']
        ret = 'QN' # 同步字符 2
        ret += self.Snum2ChrBit16(length) # 长度 2
        ret += self.Snum2ChrBit8(Mid) # ID 1
        ret += self.Snum2ChrBit8(Funcode) # 功能码 1
        ret += self.Snum2ChrBit8(success) # 读取成功失败情况 1
        ret += chr(0) # 数据格式 1
        ret += txt # 报文 N
        ret += 'E' # 结束符  1
        crc = self.crc8(ret)
        ret = ret[ : -1] + chr(crc) + ret[-1] # CRC 1
        return ret


    def formReport05(self):
        ret = ''
        try:
            ret += chr(0xa0) + chr(0x00) + chr(0x01)
            fes = self.dic['fes']
            fq = self.dic['fq']
            assert len(fes['values']) > 0
            assert fes['number'] == len(fes['values'])
            assert 'area' in fq
            ret += chr(len(fes['values'])) #长度 1
            for each in fes['values']:
                ret += self.Snum2ChrBit16(fq['area']) # 防护区 2
                ret += self.Snum2ChrBit16(each['id']) #each id 2
                ret += self.Snum2ChrBit16(each['work']) #each 状态 2
        except Exception:
            ret = DataFormer._report05fail
        return ret

    def parseReport05(self, data):
        ret = []
        try:
            if data[0] != chr(0xa0): return self._ReportError_func
            if data[1] != chr(0x00): return self._ReportError_read
            now = 4
            for i in range(ord(data[3])):
                tmp, dic = data[now : now + 6], {}
                dic['area'] = self.SBit16toNum(tmp[0 : 2])
                dic['id'] = self.SBit16toNum(tmp[2 : 4])
                dic['work'] = self.SBit16toNum(tmp[4 : 6])
                ret.append(dic)
                now += 6
        except Exception:
            ret = DataFormer._ReportError_unkn
        return ret

    def formReport04(self):
        ret = ''
        try:
            ret += chr(0x90) + chr(0x00) + chr(0x01)
            fs = self.dic['fs']
            fq = self.dic['fq']
            assert 'numJB' in fs
            assert 'oc' in fs
            assert 'co' in fs
            assert 'fog' in fs
            assert 'voc' in fs
            assert 'area' in fq
            assert 'Mtype' in fq
            assert 'Mid' in fq
            assert 'JBlevel' in fq
            ret += chr(4 + len(fs) - 1 + 3) # 长度 1
            ret += chr(0xff) + chr(0xff) # 预留 2
            ret += self.Snum2ChrBit16(fq['area']) #防护区 2
            ret += DataFormer._dicMtype2Chr[fq['Mtype']] # 设备类型 2
            ret += self.Snum2ChrBit16(fq['Mid']) # 设备ID 2
            ret += self.Snum2ChrBit16(fq['JBlevel']) # 警报等级 2
            ret += self.Sfloat2ChrBit16(fs['oc']['value']) # 温度 2 float精度三位小数
            ret += self.Sfloat2ChrBit16(fs['co']['value']) # CO 2 float精度三位小数
            ret += self.Sfloat2ChrBit16(fs['voc']['value']) # VOC 2 float精度三位小数
            ret += self.Sfloat2ChrBit16(fs['fog']['value']) # FOG 2 float精度三位小数
            ret += chr(0xff) + chr(0xff) # 预留 2
            ret += chr(0xff) + chr(0xff) # 预留 2
            ret += chr(0xff) + chr(0xff) # 预留 2
        except Exception as e:
            #print(e)
            ret = DataFormer._report04fail
        return ret

    def parseReport04(self, data):
        ret = {}
        try:
            if data[0] != chr(0x90): return self._ReportError_func
            if data[1] != chr(0x00): return self._ReportError_read
            now = 3
            ret['length'] = ord(data[now])
            now += 1
            #预留
            now += 2
            ret['area'] = self.SBit16toNum(data[now : now + 2]) # 防护区 2
            now += 2
            ret['Mtype'] = DataFormer._dicChr2Mtype[data[now : now + 2]] # 设备类型
            now += 2
            ret['Mid'] = self.SBit16toNum(data[now : now + 2]) # 设备ID
            now += 2
            ret['JBlevel'] = self.SBit16toNum(data[now : now + 2]) # 警报等级
            now += 2
            ret['oc'] = self.SBit16toFloat((data[now : now + 2])) # oc
            now += 2
            ret['co'] = self.SBit16toFloat((data[now : now + 2])) # co
            now += 2
            ret['voc'] = self.SBit16toFloat((data[now : now + 2])) # voc
            now += 2
            ret['fog'] = self.SBit16toFloat((data[now : now + 2])) # fog
            # 预留
        except Exception as e:
            #print(e)
            ret = self._ReportError_unkn
        return ret

    def formReport03(self):
        ret = ''
        try:
            ret += chr(0x80) + chr(0x00) + chr(0x01)
            fq = self.dic['fq']
            fes = self.dic['fes']
            fs = self.dic['fs']
            assert len(fes['values']) > 0
            assert fes['number'] == len(fes['values'])
            assert 'JBlevel' in fq
            assert 'numJB' in fs
            assert 'oc' in fs
            assert 'co' in fs
            assert 'fog' in fs
            assert 'voc' in fs
            assert 'auto' in fq
            assert 'shutdown' in fq
            assert 'start' in fq
            assert 'rain' in fq
            assert 'startRain' in fq
            ret += chr(11 + 1) # 信息个数 1
            ret += chr(0xff) + chr(0xff) #预留 2
            ret += self.Snum2ChrBit16(fq['area']) #防护区 2
            ret += self.Snum2ChrBit16(fq['JBlevel']) #警报等级 2
            GZcnt = 0
            for each in fes['values']:
                if each['error'] == True:
                    GZcnt += 1
            for each in fs.values():
                if type(each) == dict:
                    if each['error'] == True:
                        GZcnt += 1
            ret += self.Snum2ChrBit16(GZcnt) #故障 2
            ret += self.Snum2ChrBit16(1 if fq['auto'] == False else 0) # 手动模式 2
            ret += self.Snum2ChrBit16(1 if fq['auto'] == True else 0) # 自动模式 2
            ret += self.Snum2ChrBit16(fq['start']) # 手动启动  2
            ret += self.Snum2ChrBit16(fq['shutdown']) # 手动急停 2
            ret += chr(0xff) + chr(0xff) # 启动控制
            ret += chr(0xff) + chr(0xff) # 延时
            ret += self.Snum2ChrBit16(fq['startRain']) # 启动喷洒
            ret += self.Snum2ChrBit16(fq['rain']) # 喷洒
            ret += chr(0xff) + chr(0xff) # 预留
        except Exception as e:
            #print(e)
            ret = DataFormer._report03fail
        return ret

    def parseReport03(self, data):
        ret = {}
        try:
            if data[0] != chr(0x80): return self._ReportError_func
            if data[1] != chr(0x00): return self._ReportError_read
            now = 3
            ret['length'] = ord(data[now])
            now += 1
            # 预留
            now += 2
            ret['area'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['JBlevel'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['GZ'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['NOTauto'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['auto'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['shutdown'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['start'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            # 启动控制
            now += 2
            # 延时
            now += 2
            ret['startRain'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['rain'] = self.SBit16toNum(data[now : now + 2])
            # 预留

        except Exception as e:
            #print(e)
            ret = self._ReportError_unkn
        return ret

    def formReport02(self):
        ret = ''
        try:
            fes = self.dic['fes']
            fs = self.dic['fs']
            fq = self.dic['fq']
            assert len(fes['values']) > 0
            assert fes['number'] == len(fes['values'])
            assert 'numJB' in fs
            assert 'oc' in fs
            assert 'co' in fs
            assert 'fog' in fs
            assert 'voc' in fs
            assert 'area' in fq
            ret += chr(0x70) + chr(0x00) + chr(0x01)
            errlst = []
            for each in fes['values']:
                if each['error'] == True:
                    errlst.append((DataFormer._dicMch2Num['fireEnder'], each))
            for key, val in fs.items():
                if type(val) == dict:
                    if val['error'] == True:
                        errlst.append((DataFormer._dicMch2Num[key], val))
            ret += chr(len(errlst)) # 个数 1
            ret += chr(0xff) + chr(0xff) # 预留 2
            for each in errlst:
                ret += self.Snum2ChrBit8(fq['area']) # 防护区 1
                ret += self.Snum2ChrBit8(each[0]) # 设备类型 1
                ret += self.Snum2ChrBit8(each[1]['id']) # 设备ID 1
                ret += self.Snum2ChrBit8(1) # 故障码(无区分) 1
                ret += chr(0xff) + chr(0xff) # 预留 2

        except Exception as e:
            #print(e)
            ret = self._report02fail
        return ret

    def parseReport02(self, data):
        ret = {}
        try:
            if data[0] != chr(0x70): return self._ReportError_func
            if data[1] != chr(0x00): return self._ReportError_read
            now = 3
            ret['length'] = ord(data[now])
            now += 1
            # 预留
            now += 2
            lst = []
            for i in range(ret['length']):
                dic = {}
                dic['area'] = ord(data[now])
                now += 1
                dic['type'] = ord(data[now])
                now += 1
                dic['id'] = ord(data[now])
                now += 1
                dic['GZcode'] = ord(data[now])
                now += 2
                # 预留
                now += 1
                lst.append(dic)
            ret['values'] = lst

        except Exception as e:
            #print(e)
            ret = self._ReportError_unkn
        return ret

    def formReport01(self):
        ret = ''
        try :
            ret += chr(0x70) + chr(0x00) + chr(0x01)
            ret += chr(4) # 个数
            fes = self.dic['fes']
            fs = self.dic['fs']
            fq = self.dic['fq']
            assert len(fes['values']) > 0
            assert fes['number'] == len(fes['values'])
            assert 'numJB' in fs
            assert 'oc' in fs
            assert 'co' in fs
            assert 'fog' in fs
            assert 'voc' in fs
            assert 'FeelerNumber' in fs
            GZcnt = 0
            for each in fes['values']:
                if each['error'] == True:
                    GZcnt += 1
            for val in fs.values():
                if type(val) == dict:
                    if val['error'] == True:
                        GZcnt += 1
            ret += self.Snum2ChrBit16(fq['area']) # 分区 2
            ret += self.Snum2ChrBit16(fs['numJB']) # 警报个数 2
            ret += self.Snum2ChrBit16(GZcnt) #  故障个数 2
            ret += self.Snum2ChrBit16(fs['FeelerNumber']) # 探测器个数 2
        
        except Exception as e:
            #print(e)
            ret = self._report01fail
        return ret

    def parseReport01(self, data):
        ret = {}
        try :
            if data[0] != chr(0x70): return self._ReportError_func
            if data[1] != chr(0x00): return self._ReportError_read
            now = 3
            ret['length'] = ord(data[now])
            now += 1
            ret['area'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['JBnum'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['GZnum'] = self.SBit16toNum(data[now : now + 2])
            now += 2
            ret['FeelerNum'] = self.SBit16toNum(data[now : now + 2])
        except Exception as e:
            #print(e)
            ret = self._ReportError_unkn
        return ret
config = {
    interval: 3000,
    runNow : false,
    dir_his: '/history',
    dir_new: '/newest'
}

timerTask(config);
__init__();
function timerTask(config){
    if(config.runNow){

    }

     var doRunTime= 1000 ;
     setTimeout(function(){

         //没隔多少天在执执行
         var intTime=config.interval;
         setInterval(function(){
            autowatch();
         },intTime);
 
     },doRunTime);
 
}

//自动监控函数 发送请求给上位机服务器 并打印回复
function autowatch(){
    //console.log('ok');
    var xhrs = [new XMLHttpRequest(),new XMLHttpRequest(), new XMLHttpRequest()];
    for(var i=0; i<3; i++){
        var area = document.getElementById('area' + (i + 1)).value;
        if(area === '') continue;
        area = parseInt(area);
        //console.log(area);
        if(area === 0) continue;
        var id = i + 1;
        // headers = {
        //     name : 'xf_window',
        //     data : area
        // }
        // fetch(config.dir_new, {
        //     method: 'post',
        //     headers: headers,
        // }).then(response => {
        //     console.log(response);
        // });

        xhr = xhrs[i];
        xhr.open('POST', config.dir_new);

        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('name', 'xf_window');
        xhr.setRequestHeader('data', JSON.stringify({'area' : area, 'id': id}));

        xhr.send();
        console.log('send -box:' + id + ' -area:' + area);
        xhr.onreadystatechange = function(){
            for(var j=0; j<3; j++){
                xhr = xhrs[j];
                if(xhr.readyState === 4){
                    if((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304){
                        //console.log(xhr.getAllResponseHeaders());
                        data = xhr.getAllResponseHeaders();
                        //data = JSON.parse(data);
                        //console.log(data);
                        //console.log(typeof data);
                        data = data.split('jsjzhsjSEP');
                        //console.log(s);
                        data = JSON.parse(data[1]);
                        //console.log(data);
                        p = document.getElementById('pp' + data['id']);
                        //console.log(p);
                        data = parse_Data(data);
                        p.innerHTML = data;
                    }
                }
            }
        }

        //console.log(area);
    }
}

function parse_Data(dic, hasbr = true, allowbr = true){
    // console.log(de);
    if(dic.error != null){
        // console.log(dic.error);
        return dic.error;
    }
    //console.log('456');
    d1 = dic[1][0];
    d3 = dic[3][0];
    d4 = dic[4][0];
    d5 = dic[5];
    var FE = {
        values : []
    };
    var F ={
        values : []
    };
    for(var i = 0; i<d5.length; i ++){
        var id = d5[i]['id'];
        // console.log(id);
        // console.log(FE);
        if(FE.values.indexOf(id) == -1){
            FE.values.push(id);
        }
    }
    var shutdown = d3['shutdown'] == true ? "关机" : "运行";
    var autostatus = d3['auto'] == true ? '自动' : '手动' ;
    ret = `状态: ${shutdown} `
    if(hasbr) ret += allowbr ? '<br>' : '\n';
    ret += `时间戳: ${d1["sendTime"]} `;
    ret += `防护区: ${d1['AREA']} 控制状态: ${autostatus}`;
    if(hasbr) ret += allowbr ? '<br>' : '\n';
    ret += `警报数量:${d1['JBnum']} 故障数量:${d1['GZnum']} 探测器数量:${d1['Fnum']} 灭火器数量: ${FE.values.length} `;
    if(hasbr) ret += allowbr ? '<br>' : '\n';
    ret += `喷洒状态:${d3['rain'] == true ? '正在喷洒' : '未喷洒'} `;
    ret += `警报等级:${d3['JBlevel']} `
    if(hasbr) ret += allowbr ? '<br>' : '\n';
    ret += `温度: ${d4['oc']}摄氏度 CO: ${d4['co']}% VOC: ${d4['voc']}g/L 烟雾:${d4['fog']}mg/立方米 `;
    ret += allowbr ? '<br>' : '\n';
    ret += '故障设备:'
    lst = [];
    if(dic[2].length == 0){
        ret += '(无故障设备)'
    }else{
        for(var i=0; i<dic[2].length; i++){
            if(dic[2][i]['id'] == '201'){
                if(F.values.indexOf(dic[2][i]['id']) == -1){
                    if(hasbr) ret += allowbr ? '<br>' : '\n';
                    ret += ' 温度探测器' + dic[2][i]['id'];
                    F.values.push(dic[2][i]['id'])
                }
            }else if(dic[2][i]['id'] == '202'){
                if(F.values.indexOf(dic[2][i]['id']) == -1){
                    if(hasbr) ret += allowbr ? '<br>' : '\n';
                    ret += ' CO探测器' + dic[2][i]['id'];
                    F.values.push(dic[2][i]['id'])
                }
            }else if(dic[2][i]['id'] == '203'){
                if(F.values.indexOf(dic[2][i]['id']) == -1){
                    if(hasbr) ret += allowbr ? '<br>' : '\n';
                    ret += ' VOC探测器' + dic[2][i]['id'];
                    F.values.push(dic[2][i]['id'])
                }
            }else if(dic[2][i]['id'] == '204'){
                if(F.values.indexOf(dic[2][i]['id']) == -1){
                    if(hasbr) ret += allowbr ? '<br>' : '\n';
                    ret += ' 烟雾探测器' + dic[2][i]['id'];
                    F.values.push(dic[2][i]['id'])
                }
            }else{
                var id = dic[2][i]['id'];
                var idx = FE.values.indexOf(id);
                if(idx >= 0){
                    if(hasbr) ret += allowbr ? '<br>' : '\n';
                    ret += ' 灭火器' + id;
                    FE.values.splice(idx, 1);
                }
            }
            
        }
    }
    return ret
}

function __init__(){
    document.getElementById('bt1').onclick = () => {
        area = document.getElementById('area1').value;
        datas = {
            'datelow' : document.getElementById('datelow1').value,
            'hourlow' : document.getElementById('hourlow1').value,
            'minlow' : document.getElementById('minlow1').value,
            'datehigh' : document.getElementById('datehigh1').value,
            'hourhigh' : document.getElementById('hourhigh1').value,
            'minhigh' : document.getElementById('minhigh1').value,
            'area' : area,
        }
        sendd(datas, area);
    }
    document.getElementById('bt2').onclick = () => {
        area = document.getElementById('area2').value;
        datas = {
            'datelow' : document.getElementById('datelow2').value,
            'hourlow' : document.getElementById('hourlow2').value,
            'minlow' : document.getElementById('minlow2').value,
            'datehigh' : document.getElementById('datehigh2').value,
            'hourhigh' : document.getElementById('hourhigh2').value,
            'minhigh' : document.getElementById('minhigh2').value,
            'area' : area,
        }
        sendd(datas, area);
    }
    document.getElementById('bt3').onclick = () => {
        area = document.getElementById('area3').value;
        datas = {
            'datelow' : document.getElementById('datelow3').value,
            'hourlow' : document.getElementById('hourlow3').value,
            'minlow' : document.getElementById('minlow3').value,
            'datehigh' : document.getElementById('datehigh3').value,
            'hourhigh' : document.getElementById('hourhigh3').value,
            'minhigh' : document.getElementById('minhigh3').value,
            'area' : area,
        }
        sendd(datas, area);
    }


}

function sendd(datas, area){
    xxhr = new XMLHttpRequest();
    xxhr.open('POST', config.dir_his);

    xxhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xxhr.setRequestHeader('name', 'xf_window');
    xxhr.setRequestHeader('data', JSON.stringify(datas));

    xxhr.send();
    console.log('send -his:' + ' -area:' + area);
    xxhr.onreadystatechange = function(){
        if(xxhr.readyState === 4){
            if((xxhr.status >= 200 && xxhr.status < 300) || xxhr.status == 304){
                //console.log(xhr.getAllResponseHeaders());
                console.log('start');
                data = xxhr.getAllResponseHeaders();
                //data = JSON.parse(data);
                //console.log('1', data);
                //console.log(typeof data);
                data = data.split('jsjzhsjSEP');
                //console.log(s);
                data = JSON.parse(data[1]);
                //console.log(data);
                //p = document.getElementById('pp' + data['id']);
                //console.log(p);
                ret = '\n'
                for(var k = 0; k<data.length; k++){
                    ret += parse_Data(data[k], false, false);
                    ret += '\n\n'
                }
                //console.log(ret);
                document.getElementById('his').value = ret;
            }
        }
    }
}
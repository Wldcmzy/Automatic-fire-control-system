config = {
    interval: 3000,
    runNow : false,
    dir_his: '/history',
    dir_new: '/newest'
}

timerTask(config);

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

function parse_Data(dic){
    // console.log(de);
    if(dic.error != null){
        // console.log(dic.error);
        return dic.error;
    }
    //console.log('456');
    d1 = dic[1][0];
    d3 = dic[3][0];
    d4 = dic[4][0];
    var autostatus = d3['auto'] == true ? '自动' : '手动' ;
    ret = '';
    ret += `时间戳: ${d1["sendTime"]} `;
    ret += `防护区: ${d1['AREA']} 控制状态: ${autostatus} <br>`;
    ret += `警报数量:${d1['JBnum']} 故障数量:${d1['GZnum']} 探测器数量:${d1['Fnum']} 灭火器数量: ${dic[5].length} <br>`;
    ret += `喷洒状态:${d3['rain'] == true ? '正在喷洒' : '未喷洒'} <br>`;
    ret += `温度: ${d4['oc']}摄氏度 CO: ${d4['co']}% VOC: ${d4['voc']}g/L 烟雾:${d4['fog']}mg/立方米 <br>`;
    ret += '故障设备:'
    lst = [];
    if(dic[2].length == 0){
        ret += '(无故障设备)'
    }else{
        for(var i=0; i<dic[2].length; i++){
            if(dic[2][i]['id'] == '201'){
                ret += '<br>温度探测器' + dic[2][i]['id'];
            }else if(dic[2][i]['id'] == '202'){
                ret += '<br>CO探测器' + dic[2][i]['id'];
            }else if(dic[2][i]['id'] == '203'){
                ret += '<br>VOC探测器' + dic[2][i]['id'];
            }else if(dic[2][i]['id'] == '204'){
                ret += '<br>烟雾探测器' + dic[2][i]['id'];
            }else{
                ret += '<br>灭火器' + dic[2][i]['id'];
            }
            
        }
    }
    return ret
}
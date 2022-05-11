config = {
    interval: 3000,
    runNow : false,
    q_addr : '8.130.23.101:27777',
    dir_his: '/history',
    dir_new: '/newest'
}

timerTask(config);

function timerTask(config){
    if(config.runNow){
        //如果配置了立刻运行则立刻运行任务函数
        sendInfo();
    }

     var doRunTime= 1000 ;
     setTimeout(function(){

         //没隔多少天在执执行
         var intTime=config.interval;
         setInterval(function(){
            sendreqs();
         },intTime);
 
     },doRunTime);
 
}

function sendreqs(){
    //console.log('ok');
    for(var i=0; i<3; i++){
        var area = document.getElementById('area' + (i + 1)).value;
        area = parseInt(area);
        if(area === 0) continue;
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

        const xhr = new XMLHttpRequest();

        xhr.open('POST', config.dir_new);

        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('name', 'xf_window');
        xhr.setRequestHeader('data', area)

        xhr.send();

        xhr.onreadystatechange = function(){
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
                    console.log(data);
                    console.log(parse_Data(data))
                }
            }
        }

        //console.log(area);
    }
}

function parse_Data(dic){
    d1 = dic[1][0]
    d3 = dic[3][0]
    d4 = dic[4][0]
    ret = ''
    ret += '时间戳: ${d1["sendTime"]} '
    // ret += '防护区:%d 控制状态:%s\n' % (d1['AREA'], '自动' if d3['auto'] == True else '手动')
    // ret += '警报数量:%d 故障数量:%d 探测器数量:%d 灭火器数量: %d' %(d1['JBnum'], d1['GZnum'], d1['Fnum'], len(dic[5]))
    // ret += '喷洒状态:%s\n' % ('正在喷洒' if d3['rain'] == True else '未喷洒')
    // ret += '分区环境信息:\n'
    // ret += '温度: %.3f摄氏度 CO: 百分之%.3f VOC: %.3fg/L 烟雾:%.3fmg/立方米\n' % (d4['oc'], d4['co'], d4['voc'], d4['fog'])
    // ret += '故障机器号:'
    // if len(dic[2]) == 0:
    //     ret += '(无故障机器)'
    // for each in dic[2]:
    //     ret += each['id'] + ' '
    // ret += '\n'
    // return ret
    return ret
}
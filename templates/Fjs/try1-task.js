// 变量
var ini_xf = {
    FireEnderNumber : 4,
    FeelerNumber : 4,
    area : 1,
    auto : true,
    numJB : 0,
    numGZ : 0,
    shutdown : 0,
    active_port: 5000,
    machine_type: 'Light',
    lv: 0
}
var xf = ini_xf;

var feelerValues = {
    oc : {now: 25, threshold: 50, danger: false},
    co : {now: 0.1, threshold: 2, danger: false},
    voc : {now: 20, threshold: 160, danger: false},
    fog : {now: 0.01, threshold: 0.08, danger: false},
}

//配置项
var config={
    interval:5000,
    runNow:false//是否立即执行
};

timerTask(config);
__init__();

//定时任务逻辑
function timerTask(config){
    if(config.runNow){
        //如果配置了立刻运行则立刻运行任务函数
        sendInfo();
    }

     var doRunTime= 1000 ;
     setTimeout(function(){
        sendInfo();
         //没隔多少天在执执行
         var intTime=config.interval;
         setInterval(function(){
             if(xf.shutdown == false){
                setJBlevel();
                setJBnum(xf.numJB);
                setGZnum(xf.numGZ);
                sendInfo();
            }
 
         },intTime);
 
     },doRunTime);
 
}

 
//清空日志逻辑
function sendInfo(shutdown = false, start = false, startRain = false){
    //清空web运行程序的日志
    console.log("开始发送");
    info = {};
    info.fes = getFEdata();
    info.fs = getFeelerData();
    info.fq = getFQdata(shutdown = shutdown, start = start, startRain = startRain);
    console.log('startRain? : ' + startRain + 'shd ' + shutdown + 'st ' + start);
    headers = {
        name : 'xf_machine',
        data : JSON.stringify(info)
    }
    console.log(info);
    
    fetch('http://127.0.0.1:' + xf.active_port + '/msg_srer', {
        method: 'post',
        headers: headers,
    }).then(response => {
        console.log(response);
    });
    // const xhr = new XMLHttpRequest();

    // xhr.open('POST', 'http://127.0.0.1:' + xf.active_port + '/msg_srer');

    // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    // xhr.setRequestHeader('name', 'xf_machine');

    // xhr.send(JSON.stringify(info));
    // xhr.onreadystatechange = function(){
    //     if(xhr.readyState === 4){
    //         if(xhr.status >= 200 && xhr.status < 300){
    //             console.log(xhr.response);
    //         }
    //     }
    // }
    //FE_changeAll();
    


    console.log("完成发送");
}


//获取灭火器信息
function getFEdata(){
    let fes = {
        number : xf.FireEnderNumber,
        values : []
    };
    for(var i=0; i < xf.FireEnderNumber; i ++){
        let fe = {};
        //fe.name = 'test';
        //fe.value = i;
        fe.id = document.getElementById('FE' + (i + 1)).innerHTML;
        fe.work = document.getElementById('SFE' + (i + 1)).checked;
        fe.error = document.getElementById('GFE' + (i + 1)).checked;
        //console.log(fe);
        fes.values.push(fe);
    }
    /*fes.forEach(function(item){
        console.log(item);
    });*/
    //console.log(fes);
    return fes;
}

//获取探测器信息
function getFeelerData(){
    let fs = {}
    fs.numJB = document.getElementById('numJB').innerHTML;
    fs.FeelerNumber= '' + xf.FeelerNumber
    fs.oc ={
        id : document.getElementById('FL1').innerHTML,
        value : document.getElementById('TFL1').value,
        error : document.getElementById('GFL1').checked,
    }  
    fs.co = {
        id : document.getElementById('FL2').innerHTML,
        value : document.getElementById('TFL2').value,
        error : document.getElementById('GFL2').checked,
    }
    fs.voc = {
        id : document.getElementById('FL3').innerHTML,
        value : document.getElementById('TFL3').value,
        error : document.getElementById('GFL3').checked,
    }
    fs.fog = {
        id : document.getElementById('FL4').innerHTML,
        value : document.getElementById('TFL4').value,
        error : document.getElementById('GFL4').checked,
    }
    //console.log(fs);
    return fs;
}


//获取分区信息
function getFQdata(shutdown = false, start = false, startRain = false){
    let fq = {}
    fq.area = document.getElementById('Area').innerHTML;
    fq.JBlevel = document.getElementById('JBlevel').innerHTML;
    fq.Mid = document.getElementById('Mid').innerHTML;
    fq.Mtype = document.getElementById('Mtype').innerHTML;
    fq.auto = xf.auto;
    fq.start = start;
    fq.shutdown = shutdown;
    var cnt = 0;
    for(var i=0; i<xf.FireEnderNumber; i++){
        if(document.getElementById('SFE' + (i + 1)).checked == true){
            cnt += 1;
        }
    }
    fq.rain = cnt == 0 ? false : true;
    fq.startRain = startRain;
    return fq;
}

//故障按钮触发函数
function onGZchange(){
    let cnt = 0;
    for(var i=0; i<xf.FireEnderNumber; i++){
        j = document.getElementById('GFE' + (i + 1)).checked;
        if(j == true) cnt += 1;
    }
    for(var i=0; i<xf.FeelerNumber; i++){
        j = document.getElementById('GFL' + (i + 1)).checked;
        if(j == true) cnt += 1;
    }
    xf.numGZ = cnt;
    console.log(xf.numGZ);
    setGZnum(cnt);
}

//初始化
function __init__(){

    document.getElementById('Area').innerHTML = xf.area;
    document.getElementById('Mid').innerHTML = xf.area;
    document.getElementById('Mtype').innerHTML = xf.machine_type;
    document.getElementById('autoCtrl').checked = xf.auto;

    document.getElementById('shutdown').onclick = () => {
        if(xf.shutdown == false) {
            FE_changeAll(0);
            sendInfo(shutdown = true, start = false, startRain = false);
            xf.shutdown = true;
            document.getElementById('working').innerHTML = '否'
        }
    }
    document.getElementById('start').onclick = () => {
        if(xf.shutdown == true) {
            xf.shutdown = false;
            setJBlevel(true);
            sendInfo(shutdown = false, start = true, startRain = false);
            document.getElementById('working').innerHTML = '是'
        }
    }

    for(var i=0; i<xf.FeelerNumber; i++){
        document.getElementById('GFE' + (i + 1)).onchange = onGZchange;
        document.getElementById('GFL' + (i + 1)).onchange = onGZchange;
    }

    document.getElementById('TFL1').onchange = () => {
        obj = document.getElementById('TFL1');
        //console.log(obj.value);
        let last = feelerValues.oc.danger;
        feelerValues.oc.danger = obj.value > feelerValues.oc.threshold;
        if(last != feelerValues.oc.danger){
            if(last == false){
                xf.numJB += 1;
                document.getElementById('SFL1').innerHTML = '异常'
            }else{
                xf.numJB -= 1;
                document.getElementById('SFL1').innerHTML = '正常'
            }
            setJBnum(xf.numJB);
        }
        //console.log(feelerValues.oc.danger);
        setJBlevel();
    }
    document.getElementById('TFL2').onchange = () => {
        obj = document.getElementById('TFL2');
        //console.log(obj.value);
        let last = feelerValues.co.danger;
        feelerValues.co.danger = obj.value > feelerValues.co.threshold;
        if(last != feelerValues.co.danger){
            if(last == false){
                xf.numJB += 1;
                document.getElementById('SFL2').innerHTML = '异常'
            }else{
                xf.numJB -= 1;
                document.getElementById('SFL2').innerHTML = '正常'
            }
            setJBnum(xf.numJB);
        }
        //console.log(feelerValues.co.danger);
        setJBlevel();
    }
    document.getElementById('TFL3').onchange = () => {
        obj = document.getElementById('TFL3');
        //console.log(obj.value);
        let last = feelerValues.voc.danger;
        feelerValues.voc.danger = obj.value > feelerValues.voc.threshold;
        if(last != feelerValues.voc.danger){
            if(last == false){
                xf.numJB += 1;
                document.getElementById('SFL3').innerHTML = '异常'
            }else{
                xf.numJB -= 1;
                document.getElementById('SFL3').innerHTML = '正常'
            }
            setJBnum(xf.numJB);
        }
        //console.log(feelerValues.voc.danger);
        setJBlevel();
    }
    document.getElementById('TFL4').onchange = () => {
        obj = document.getElementById('TFL4');
        //console.log(obj.value);
        let last = feelerValues.fog.danger;
        feelerValues.fog.danger = obj.value > feelerValues.fog.threshold;
        if(last != feelerValues.fog.danger){
            if(last == false){
                xf.numJB += 1;
                document.getElementById('SFL4').innerHTML = '异常'
            }else{
                xf.numJB -= 1;
                document.getElementById('SFL4').innerHTML = '正常'
            }
            setJBnum(xf.numJB);
        }
        //console.log(feelerValues.fog.danger);
        setJBlevel();
    }

    document.getElementById('autoCtrl').onchange = () => {
        obj = document.getElementById('autoCtrl');
        console.log(obj.checked);
        xf.auto = obj.checked;
        setJBlevel();
    }

    document.getElementById('rain').onclick = () => {
        if(xf.auto == false){
            FE_changeAll(1);
            sendInfo(false, false, startRain = true);
        }
    }

    document.getElementById('notrain').onclick = () => {
        if(xf.auto == false){
            FE_changeAll(0);
        }
    }
}


//html设置故障数量
function setGZnum(num){
    if(xf.shutdown == true) return ;
    document.getElementById('numGZ').innerHTML = num;
}

//html设置警报数量
function setJBnum(num){
    if(xf.shutdown == true) return ;
    //config.log(num);
    document.getElementById('numJB').innerHTML = num;
}

//自动判断更新警报等级，并开/关
function setJBlevel(){
    if(xf.shutdown == true) return ;
    let lv = 0;
    if(feelerValues.co.danger == true || 
        feelerValues.voc.danger == true || 
        feelerValues.fog.danger == true) {
        lv = 2;
        if(feelerValues.oc.danger == true){
            lv = 3;
        }
    }else if(feelerValues.oc.danger == true){
        lv = 1;
    }
    document.getElementById('JBlevel').innerHTML = lv;
    if(xf.auto == true){
        FE_changeAll(lv >= 3 ? 1 : 0);
        if(xf.lv < 3 && lv >= 3){
            console.log('in setJBlevel start-rain');
            sendInfo(false, false, startRain = true);
        }
    }
    xf.lv = lv;
}

// 开/关 灭火器
function FE_changeAll(way = 2){
    for(var i=0; i < xf.FireEnderNumber; i ++){
        obj = document.getElementById('SFE' + (i + 1));
        switch(way){
            case 0:
                obj.checked = 0;
                break;
            case 1:
                obj.checked = 1;
                break;
            default:
                obj.checked ^= 1;
        }
        
    }
}
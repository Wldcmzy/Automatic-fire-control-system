// 变量
var ini_xf = {
    FireEnderNumber : 4,
    FeelerNumber : 4,
    area : 1,
    auto : true,
    numJB : 0,
    numGZ : 0,
    shutdown : 0,
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
    interval:5000,//隔几天执行一次
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
function sendInfo(){
    //清空web运行程序的日志
    console.log("开始发送");
    info = {};
    info.fes = getFEdata();

    console.log(info);
    //FE_changeAll();
    console.log("完成发送");
}

function getFEdata(){
    let fes = {
        number : xf.FireEnderNumber,
        values : []
    };
    for(var i=0; i < xf.FireEnderNumber; i ++){
        let fe = {};
        //fe.name = 'test';
        //fe.value = i;
        obj = document.getElementById('FE' + (i + 1));
        fe.id = obj.innerHTML;
        obj = document.getElementById('SFE' + (i + 1));
        fe.work = obj.checked;
        //console.log(fe);
        fes.values.push(fe);
    }
    /*fes.forEach(function(item){
        console.log(item);
    });*/
    //console.log(fes);
    return fes;
}

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

function __init__(){

    document.getElementById('Area').innerHTML = xf.area;
    document.getElementById('autoCtrl').checked = xf.auto;

    document.getElementById('shutdown').onclick = () => {
        FE_changeAll(0);
        xf.shutdown = true;
        document.getElementById('working').innerHTML = '否'
    }
    document.getElementById('start').onclick = () => {
        xf.shutdown = false;
        setJBlevel();
        document.getElementById('working').innerHTML = '是'
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
        }
    }

    document.getElementById('notrain').onclick = () => {
        if(xf.auto == false){
            FE_changeAll(0);
        }
    }
}

function setGZnum(num){
    if(xf.shutdown == true) return ;
    document.getElementById('numGZ').innerHTML = num;
}

function setJBnum(num){
    if(xf.shutdown == true) return ;
    //config.log(num);
    document.getElementById('numJB').innerHTML = num;
}


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
    }
}

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
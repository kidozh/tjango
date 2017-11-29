/**
 * Created by kidozh on 2016/12/4.
 */

// clock for overview
var sec = 0;
// global variables

// for echarts setting


function dynamicGetInfo(){
    sec = 0;
    var interval =  setInterval(function(){
        // get width
        sec +=1;
        timepercent = (sec * 20)% 100 ;
        if (timepercent/100 == 0){

            if (typeof WebSocket != 'undefined') {
                /*supported websocket*/
                getHardWareInfoByWS();
            }
            else{
                getHardwareInfo();
            }


            timepercent = 100;
        }
        widthFormat = timepercent.toString()+'%';
        $('#time-progress').css('width' ,widthFormat);

    }, 1000);
    return interval;
}






var data = [];

for (var i = 0; i <= 360; i++) {
    var t = i / 180 * Math.PI;
    var r = Math.sin(2 * t) * Math.cos(2 * t);
    data.push([r, i]);
}



import {hex_md5} from '../../static/js/common.js'

var token = {
    appkey:localStorage.getItem('appkey'),
    appsecret:localStorage.getItem('appsecret'),
    DEVELOPER_APPKEY:'A0Zr98jxccdvdvvfbfbbbfbfRsdT',
    MD5_KEY:'A0Zr98j/3yX R~XHH!jmN]LWX/,?RsdT',
    getToken: function(){
       var timestamp = Date.parse(new Date())/1000;
       return token.appkey + '&&' + timestamp + '&&' + hex_md5(token.appsecret+'&&'+timestamp.toString());
    },
    getAppToken: function(){
       var timestamp = Date.parse(new Date())/1000;
       return timestamp + '&&' + hex_md5(timestamp+'&&'+token.DEVELOPER_APPKEY);
    },
     getAppToken1: function(pw){
       var timestamp = Date.parse(new Date())/1000;
       return timestamp + '&&' + hex_md5(pw +'&&' + token.MD5_KEY + timestamp);
    },
}
export default token

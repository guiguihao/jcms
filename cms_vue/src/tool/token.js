import {hex_md5} from '../../static/js/common.js'

var token = {
    appkey:'5aae3e0b1fe6371e1ce9533b',
    appsecret:'23e38ab5caedc3a1',
    DEVELOPER_APPKEY:'A0Zr98jxccdvdvvfbfbbbfbfRsdT',
    getToken: function(){
       var timestamp = Date.parse(new Date())/1000;
       return token.appkey + '&&' + timestamp + '&&' + hex_md5(token.appsecret+'&&'+timestamp);
    },
    getAppToken: function(){
       var timestamp = Date.parse(new Date())/1000;
       return timestamp + '&&' + hex_md5(timestamp+'&&'+token.DEVELOPER_APPKEY);
    },
}
export default token

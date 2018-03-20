import {hex_md5} from '../../static/js/common.js'

var token = {
    appkey:'5ab0aacad678fdd7f607d7c6',
    appsecret:'667ab2786bfa763c',
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

import {hex_md5} from '../../static/js/common.js'

var token = {
    appkey:'5aa7974ed678fd38b2a63eb3',
    appsecret:'54ba35ae40d75613',
    getToken: function(){
       var timestamp = Date.parse(new Date())/1000;
       return token.appkey + '&&' + timestamp + '&&' + hex_md5(token.appsecret+'&&'+timestamp);
    },
}
export default token

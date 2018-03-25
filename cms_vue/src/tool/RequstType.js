import token from './token'
import axios from '../http/http'

var RequestType = {
   getTypeList: function(type){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/type/list';
          } else {
            url = '/app/type/list';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
            type:type,
            token:myToken
          }
          let p = new Promise(function(resolve, reject){        //做一些异步操作
            axios.post(url, params).then((res) => {
             // console.log(JSON.stringify(res.data)); 
              resolve(res);
              }).catch(function(error) {

                reject(error)
              });
          });
          return p;
   },

}

export default RequestType

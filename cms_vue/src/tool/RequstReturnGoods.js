import token from './token'
import axios from '../http/http'

var RequstReturnGoods = {
   getReturnGoods: function(){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/admin/shopreturn/get';
          } else {
            url = '/app/admin/shopreturn/get';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
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

   addUpReturnGoods: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/admin/shopreturn/update';
          } else {
            url = '/app/admin/shopreturn/update';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
            set:paramsDic,
            token:myToken,
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

export default RequstReturnGoods

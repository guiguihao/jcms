import token from './token'
import axios from '../http/http'

var RequestFenXiao = {
   getFenXiao: function(){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/shop/fenxiao/get';
          } else {
            url = '/app/shop/fenxiao/get';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
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

   updateFenXiao: function(paramsDic){      //添加或更新
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/shop/fenxiao/update';
          } else {
            url = '/app/shop/fenxiao/update';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
            set:{},
            token:myToken
          }
          for (let k in paramsDic){
             params.set[k] = paramsDic[k];
          }
          console.log(JSON.stringify(params)); 
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

export default RequestFenXiao

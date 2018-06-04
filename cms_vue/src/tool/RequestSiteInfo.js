import token from './token'
import axios from '../http/http'

var RequestSiteinfo = {
   getSiteinfo: function(){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/admin/info/get';
          } else {
            url = '/app/admin/info/get';
          }
          //myTest();
          let params = {
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

   updateSiteinfo: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/admin/info/update';
          } else {
            url = '/app/admin/info/update';
          }
          //myTest();
          let params = {
            set:{},
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

   getAppkeyAndSecret: function(){
            let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/get/appkeyAndSecret';
          } else {
            url = '/app/get/appkeyAndSecret';
          }
          let p = new Promise(function(resolve, reject){        //做一些异步操作
            axios.post(url).then((res) => {
             // console.log(JSON.stringify(res.data)); 
              resolve(res);
              }).catch(function(error) {

                reject(error)
              });
          });
          return p;
   }

}

export default RequestSiteinfo

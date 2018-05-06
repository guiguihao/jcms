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
          let params = {
            type:type,
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

   addType: function(type,paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/type/add';
          } else {
            url = '/app/type/add';
          }
          //myTest();
          let params = {
            type:type,
          }
          for (let k in paramsDic){
               params[k] = paramsDic[k];
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

   updateType: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/type/update';
          } else {
            url = '/app/type/update';
          }
          //myTest();
          let params = {
            _id:paramsDic._id,
            set:{},
          }
          for (let k in paramsDic){
            if (k != '_id') {
               params.set[k] = paramsDic[k];
            }
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

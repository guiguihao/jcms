import token from './token'
import axios from '../http/http'

var RequestReceiveInfo = {
   getReceiveInfo: function(currentPage,pagesize,filter){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/receive/list';
          } else {
            url = '/app/receive/list';
          }
          //myTest();
          let params = {
            page:currentPage,
            pageSize:pagesize,
            filter:filter
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

   addReceiveInfo: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/receive/add';
          } else {
            url = '/app/receive/add';
          }
          //myTest();
          let params = {
          }
          for (let k in paramsDic){
               params[k] = paramsDic[k];
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

   updateReceiveInfo: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/receive/update';
          } else {
            url = '/app/receive/update';
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

export default RequestReceiveInfo

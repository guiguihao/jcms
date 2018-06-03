import token from './token'
import axios from '../http/http'

var RequestCollection = {
   getCollections: function(currentPage,pagesize,filter){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/productCollection/list';
          } else {
            url = '/app/productCollection/list';
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

   addCollection: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/productCollection/add';
          } else {
            url = '/app/productCollection/add';
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

   updateCollection: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/productCollection/update';
          } else {
            url = '/app/productCollection/update';
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

export default RequestCollection

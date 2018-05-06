import token from './token'
import axios from '../http/http'

var RequestOrder = {
   getOrderList: function(currentPage,pagesize,filter){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/order/list';
          } else {
            url = '/app/order/list';
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

   addOrder: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/order/add';
          } else {
            url = '/app/order/add';
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

   updateOrder: function(paramsDic){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/order/update';
          } else {
            url = '/app/order/update';
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

export default RequestOrder

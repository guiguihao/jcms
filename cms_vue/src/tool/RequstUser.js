import token from './token'
import axios from '../http/http'

var RequestUser = {

   //currentPage 当前页, pagesize 每页显示数量,filter 查询条件 字典类型
   getUserList: function(currentPage,pagesize,filter){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/user/list';
          } else {
            url = '/app/user/list';
          }
          //myTest();
          let myToken = token.getToken();
          let params = {
            page:currentPage,
            pageSize:pagesize,
            token:myToken,
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

   //添加\注册用户方法 dic为一个字典, {name:'xx',password:'',....}
   addUser: function(dic){
          let url = '';
          let myToken = token.getToken();
          let params = {
            token:myToken
          }
          for (let k in dic){
            params[k] = dic[k];
          }
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/user/add';
          } else {
            url = '/app/user/add';
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

   //更新用户方法 dic为一个字典, {_id:'xxxxxxxxxxx',name:'xx',password:'',....}
   updateUser: function(dic){
          let url = '';
          let myToken = token.getToken();
          let params = {
            _id:dic._id,
            set:{},
            token:myToken
          }
          for (let k in dic){
            if (k != '_id') {
               params.set[k] = dic[k];
            }
          }
          console.log(JSON.stringify(params));
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/user/update';
          } else {
            url = '/app/user/update';
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

export default RequestUser

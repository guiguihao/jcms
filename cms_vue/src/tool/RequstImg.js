import token from './token'
import axios from '../http/http'

var RequestImg = {
   saveImg: function(file){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/save/img';
          } else {
            url = '/app/save/img';
          }
          //myTest();
          let myToken = token.getToken();
          var formdata = new FormData();
           formdata.append('image', file);
           formdata.append('token', myToken);
          let p = new Promise(function(resolve, reject){        //做一些异步操作
            axios.post(url, formdata,{ 'Content-Type': 'multipart/form-data' }).then((res) => {
             // console.log(JSON.stringify(res.data)); 
              resolve(res);
              }).catch(function(error) {

                reject(error)
              });
          });
          return p;
   },
   delImg: function(fileName){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/del/img';
          } else {
            url = '/app/del/img';
          }
          //myTest();
          let myToken = token.getToken();
          var formdata = new FormData();
           formdata.append('imgname', fileName);
           formdata.append('token', myToken);
          let p = new Promise(function(resolve, reject){        //做一些异步操作
            axios.post(url, formdata).then((res) => {
             // console.log(JSON.stringify(res.data)); 
              resolve(res);
              }).catch(function(error) {

                reject(error)
              });
          });
          return p;
   },
}

export default RequestImg

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
          let params = {
            image:file,
            token:myToken
          }
          var formdata = new FormData();
           formdata.append('image', file);
           formdata.append('token', myToken);
          console.log(params);
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

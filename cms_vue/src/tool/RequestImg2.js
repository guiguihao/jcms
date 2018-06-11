import token from './token'
import axios from '../http/http'
import Orther from './orther'

var RequestImg2 = {
   getImg2tList: function(currentPage,pagesize,filter){
          let url = '';
          if(process.env.NODE_ENV === 'development') { //TEST
            url = '/api/app/img2/list';
          } else {
            url = '/app/img2/list';
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

   //更新描述 


   //更新或添加图片
   updateImg2: function(paramsDic,file){
          let url = '';
          let siteInfo =  Orther.getSiteInfo();
          if(process.env.NODE_ENV === 'development') { //TEST
            url = siteInfo.reserved_1 + '/upload/saveImg.php';
          } else {
            url = siteInfo.reserved_1 + '/upload/saveImg.php';
          }
          let param = new FormData()  // 创建form对象
          // param.append('file', file, file.name)  // 通过append向form对象添加数据
          for (let k in paramsDic){
            param.append(k,paramsDic[k]);
          }
          if (file) {
            param.append('file', file, file.name);
          }
          let p = new Promise(function(resolve, reject){        //做一些异步操作
            axios.post(url, param,{
              headers: {
                            'Content-Type': 'multipart/form-data',
                      }
            }).then((res) => {
             // console.log(JSON.stringify(res.data)); 
              resolve(res);
              }).catch(function(error) {

                reject(error)
              });
          });
          return p;
   },

}

export default RequestImg2

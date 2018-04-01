/**
 * Created by superman on 17/2/16.
 * http配置
 */

import axios from 'axios'
// import store from './store/store'
//import router from './router'

// axios 配置
axios.defaults.timeout = 30000;
//axios.defaults.baseURL = 'https://api.github.com';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        let token = localStorage.getItem('token');
           if(token){
            //alert(localStorage.getItem('token'));
              config.headers.Authorization = token;
           }
           return config;
    },
    err => {
        return Promise.reject(err);
});

// http response 拦截器
axios.interceptors.response.use(
    response => {
//  	  alert('response');
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 401 清除token信息并跳转到登录页面
//                  store.commit(types.LOGOUT);
//                  router.replace({
//                      path: 'login',
//                      query: {redirect: router.currentRoute.fullPath}
//                  })
            }
            // alert('error');
        }
        // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
        return Promise.reject(error.response.data)
});

export default axios;

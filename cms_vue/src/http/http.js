/**
 * Created by superman on 17/2/16.
 * http配置
 */
import router from '../router'
import token from '../tool/token'
import axios from 'axios'
// import store from './store/store'
//import router from './router'

// axios 配置
axios.defaults.timeout = 3000;
//axios.defaults.baseURL = 'https://api.github.com';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        let mtoken = token.getToken();
           if(mtoken){
            //alert(localStorage.getItem('token'));
              config.headers.Authorization = mtoken;
           }
           return config;
    },
    err => {
        return Promise.reject(err);
});

// http response 拦截器
axios.interceptors.response.use(
    response => {
 	
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                 router.replace({
                        path: '/admin/login',
                    })
            }
        }
        console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
        return Promise.reject(error.response.data)
});

export default axios;

import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/admin/login'
import applogin from '@/components/app/login'
import home from '@/components/admin/component/home.vue'
import apphome from '@/components/app/component/home.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: login,
      meta: {
            title: '登陆页面'
        }
      
    },
    {
      path: '/login',
      name: 'login1',
      meta: { ignore: true },
      component: login,
      meta: {
            title: '登陆页面'
        }
    },
    {
      path: '/applogin',
      name: 'applogin',
      meta: { ignore: true },
      component: applogin,
      meta: {
            title: 'APP管理登陆页面'
        }
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      meta: { admin: true },
      children:[
                {
                    path: '/',
                       component: resolve => require(['../components/admin/ArticleList.vue'], resolve),
                },{
                    path: '/ArticleList',
                    meta: {
                         title: '文章列表'
                    },
                       component: resolve => require(['../components/admin/ArticleList.vue'], resolve),
                },{
                    path: '/ArticleEdit',
                    name:'ArticleEdit',
                    meta: {
                         title: '编辑文章'
                    },
                       component: resolve => require(['../components/admin/ArticleEdit.vue'], resolve),
                },{
                    path: '/ArticleType',
                    name:'ArticleType',
                    meta: {
                         title: '类别管理'
                    },
                       component: resolve => require(['../components/admin/ArticleType.vue'], resolve),
                },{
                    path: '/ProductList',
                    name:'ProductList',
                    meta: {
                         title: '产品列表'
                    },
                       component: resolve => require(['../components/admin/ProductList.vue'], resolve),
                },{
                    path: '/ProductEdit',
                    name:'ProductEdit',
                    meta: {
                         title: '编辑产品'
                    },
                       component: resolve => require(['../components/admin/ProductEdit.vue'], resolve),
                },
                {
                    path: '/ProductSales',
                    name:'ProductSales',
                    meta: {
                         title: '促销活动管理'
                    },
                       component: resolve => require(['../components/admin/ProductSales.vue'], resolve),
                },
                {
                    path: '/ProductSaleEdit',
                    name:'ProductSaleEdit',
                    meta: {
                         title: '促销活动管理编辑'
                    },
                       component: resolve => require(['../components/admin/ProductSaleEdit.vue'], resolve),
                },
                {
                    path: '/ProductOrderList',
                    name:'ProductOrderList',
                    meta: {
                         title: '订单管理'
                    },
                       component: resolve => require(['../components/admin/ProductOrderList.vue'], resolve),
                },{
                    path: '/ProductType',
                    name:'ProductType',
                    meta: {
                         title: '产品类别'
                    },
                       component: resolve => require(['../components/admin/ProductType.vue'], resolve),
                },{
                    path: '/ProductSaleCode',
                    name:'ProductSaleCode',
                    meta: {
                         title: '产品促销码'
                    },
                       component: resolve => require(['../components/admin/ProductSaleCode.vue'], resolve),
                },{
                    path: '/ProductReturnGoods',
                    name:'ProductReturnGoods',
                    meta: {
                         title: '退货信息'
                    },
                       component: resolve => require(['../components/admin/ProductReturnGoods.vue'], resolve),
                },{
                    path: '/UserList',
                    name:'UserList',
                    meta: {
                         title: '用户列表'
                    },
                       component: resolve => require(['../components/admin/UserList.vue'], resolve),
                },{
                    path: '/UserType',
                    name:'UserType',
                    meta: {
                         title: '用户类型管理'
                    },
                       component: resolve => require(['../components/admin/UserType.vue'], resolve),
                },{
                    path: '/SiteInfo',
                    name:'SiteInfo',
                    meta: {
                         title: '网站信息管理'
                    },
                       component: resolve => require(['../components/admin/SiteInfo.vue'], resolve),
                },{
                    path: '/AdminList',
                    name:'AdminList',
                    meta: {
                         title: '管理员列表'
                    },
                       component: resolve => require(['../components/admin/AdminList.vue'], resolve),
                },



                ]
    },
    {
      path: '/app',
      name: 'app',
      component: apphome,
      meta: { app: true },
      children:[{
                    path: '/',
                    meta: {
                         title: '应用列表'
                    },
                       component: resolve => require(['../components/app/appList.vue'], resolve),
                },{
                    path: '/appList',
                    meta: {
                         title: '应用列表'
                    },
                       component: resolve => require(['../components/app/appList.vue'], resolve),
                },{
                    path: '/ArticleList',
                    meta: {
                         title: '文章列表'
                    },
                       component: resolve => require(['../components/admin/ArticleList.vue'], resolve),
                },]
    }
  ]
});

router.beforeEach((to, from, next) => {
    /*if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
        if (store.state.token) {  // 通过vuex state获取当前的token是否存在
            next();
        }
        else {
            next({
                path: '/login',
                query: {redirect: to.fullPath}  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    }
    else {
        next();
    }*/
 //    next();
//    alert();
            // alert(JSON.stringify(to.path))
            if (to.meta.title) {

                document.title = to.meta.title;
             }
      if (to.path.indexOf('/home/')>-1) {
          let token = localStorage.getItem('token1');
             
            if(token){
            // alert(localStorage.getItem('token'));
//            config.headers.Authorization = token;
             next();
           }else{
            // alert(localStorage.getItem('token'));
              if (to.meta.ignore ) {
                next();
                
              }else{
                next({
                        name: 'login',
                })
              }
           }
      }

      else if (to.path.indexOf('/app/')>-1) {
          let token = localStorage.getItem('apptoken');
            if(token){
              next();
           }else{
              if (to.meta.ignore ) {
                next();
                
              }else{
                next({
                        name: 'applogin',
                })
              }
           }
      }else{

        next();
      }


			

})

export default router;

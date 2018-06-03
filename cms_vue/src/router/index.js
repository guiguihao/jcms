import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/admin/login'
import register from '@/components/admin/register'
import applogin from '@/components/app/login'
import home from '@/components/admin/component/home.vue'
import apphome from '@/components/app/component/home.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/admin/login',
      name: 'login',
      meta: { ignore: true },
      component: login,
      meta: {
            title: '登陆页面'
        }
    },
    {
      path: '/admin/',
      name: 'login',
      meta: { ignore: true },
      component: login,
      meta: {
            title: '登陆页面'
        }
    },
     {
      path: '/admin/register',
      name: 'register',
      component: register,
      meta: {
            title: '应用注册'
        }
    },
   
    {
      path: '/admin/home',
      name: 'admin',
      component: home,
      meta: { admin: true },
      children:[
                {
                    path: '/',
                    meta: {
                         title: '网站信息管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/SiteInfo.vue'], resolve),
                },{
                    path: '/admin/Article/ArticleList',
                    name:'ArticleList',
                    meta: {
                         title: '文章列表',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ArticleList.vue'], resolve),
                },{
                    path: '/admin/Article/ArticleEdit/:id',
                    name:'ArticleEdit',
                    meta: {
                         title: '编辑文章',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ArticleEdit.vue'], resolve),
                },{
                    path: '/admin/Article/ArticleType',
                    name:'ArticleType',
                    meta: {
                         title: '类别管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ArticleType.vue'], resolve),
                },{
                    path: '/admin/Article/ArticleRcmType',
                    name:'ArticleRcmType',
                    meta: {
                         title: '推荐类别管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ArticleRcmType.vue'], resolve),
                },{
                    path: '/admin/Product/ProductList',
                    name:'ProductList',
                    meta: {
                         title: '产品列表',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductList.vue'], resolve),
                },{
                    path: '/admin/Product/ProductCollection',
                    name:'ProductCollection',
                    meta: {
                         title: '收藏列表',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductCollection.vue'], resolve),
                },{
                    path: '/admin/Product/ReceiveInfo',
                    name:'ReceiveInfo',
                    meta: {
                         title: '收货地址',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ReceiveInfo.vue'], resolve),
                },{
                    path: '/admin/Product/ProductEdit/:id',
                    name:'ProductEdit',
                    meta: {
                         title: '编辑产品',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductEdit.vue'], resolve),
                },
                {
                    path: '/admin/Product/ProductSales',
                    name:'ProductSales',
                    meta: {
                         title: '促销活动管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductSales.vue'], resolve),
                },
               
                {
                    path: '/admin/Product/ProductOrderList',
                    name:'ProductOrderList',
                    meta: {
                         title: '订单管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductOrderList.vue'], resolve),
                },{
                    path: '/admin/Product/ProductType',
                    name:'ProductType',
                    meta: {
                         title: '产品类别',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductType.vue'], resolve),
                },{
                    path: '/admin/Product/ProductRcmType',
                    name:'ProductRcmType',
                    meta: {
                         title: '产品推荐类别管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductRcmType.vue'], resolve),
                },{
                    path: '/admin/Product/ProductSaleCode',
                    name:'ProductSaleCode',
                    meta: {
                         title: '产品促销码',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductSaleCode.vue'], resolve),
                },{
                    path: '/admin/Product/FenXiao',
                    name:'ProductFenxiao',
                    meta: {
                         title: '分销设置',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductFenXiao.vue'], resolve),
                },{
                    path: '/admin/Product/ProductReturnGoods',
                    name:'ProductReturnGoods',
                    meta: {
                         title: '退货信息',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/ProductReturnGoods.vue'], resolve),
                },{
                    path: '/admin/user/UserList',
                    name:'UserList',
                    meta: {
                         title: '用户列表',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/UserList.vue'], resolve),
                },{
                    path: '/admin/user/UserType',
                    name:'UserType',
                    meta: {
                         title: '用户类型管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/UserType.vue'], resolve),
                },{
                    path: '/admin/comment',
                    name:'comment',
                    meta: {
                         title: '评论管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/Comment.vue'], resolve),
                },{
                    path: '/admin/message',
                    name:'message',
                    meta: {
                         title: '留言管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/Message.vue'], resolve),
                },{
                    path: '/admin/img',
                    name:'img',
                    meta: {
                         title: '图片/资源管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/Img.vue'], resolve),
                },{
                    path: '/admin/rsc',
                    name:'rsc',
                    meta: {
                         title: '图片/资源管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/Rsc.vue'], resolve),
                },{
                    path: '/admin/adImg',
                    name:'rsc',
                    meta: {
                         title: '广告图片/资源管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/AdImg.vue'], resolve),
                },{
                    path: '/admin/SiteInfo',
                    name:'SiteInfo',
                    meta: {
                         title: '网站信息管理',
                         requireAuth: true
                    },
                       component: resolve => require(['../components/admin/SiteInfo.vue'], resolve),
                },{
                    path: '/admin/AdminList',
                    name:'AdminList',
                    meta: {
                         title: '管理员列表',
                         requireAuth: true
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
    if (to.meta.title) {
       document.title = to.meta.title;
    }
     next();
    // if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
    //     if (localStorage.getItem('appkey')) {  // 通过vuex state获取当前的token是否存在
    //         next();
    //     }
    //     else {
    //         next({
    //             name: 'login',
    //         })
    //     }
    // }
    // else {
    //     next();
    // }

})

export default router;

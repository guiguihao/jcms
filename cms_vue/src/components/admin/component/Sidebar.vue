<template>
	<div class="sidebar">
		<el-menu :default-active="onRoutes" class="el-menu-vertical-demo" theme="dark" unique-opened router>
			<template v-for="item in items">
				<template v-if="item.subs" ><!-- 包含子节点的情形 -->
					<el-submenu :index="item.index">  
						<!--v-if="item.role"-->
						<template slot="title"><i :class="item.icon"></i>{{ item.title }}</template>
						<el-menu-item v-for="(subItem,i) in item.subs" :key="i" :index="subItem.index">{{ subItem.title }}
						</el-menu-item>
					</el-submenu>
				</template>
			</template>
		</el-menu>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				items: [
					//add
					{
						icon: 'el-icon-tickets',
						index: '1',
						title: '文章模块',
						permission:0,//1 显示 0不显示
						subs: [{
							index: '/admin/Article/ArticleList',
							title: '文章管理',
						},{
							index: '/admin/Article/ArticleType',
							title: '类别管理',
						},{
							index: '/admin/Article/ArticleRcmType',
							title: '推荐类型管理',
						},]
					},
					{
						icon: 'el-icon-goods',
						index: '2',
						title: '产品模块',
						permission:0,//权限信息
						subs: [{
							index: '/admin/Product/ProductList',
							title: '产品列表',
						},{
							index: '/admin/Product/ProductSales',
							title: '活动管理',
						},{
							index: '/admin/Product/ProductOrderList',
							title: '订单管理',
						},{
							index: '/admin/Product/ProductCollection',
							title: '收藏列表',
						},{
							index: '/admin/Product/ReceiveInfo',
							title: '收货地址',
						},{
							index: '/admin/Product/ProductType',
							title: '类别管理',
						},{
							index: '/admin/Product/ProductRcmType',
							title: '推荐类型管理',
						},{
							index: '/admin/Product/ProductSaleCode',
							title: '优惠码',
						},{
							index: '/admin/Product/FenXiao',
							title: '分销设置',
						},{
							index: '/admin/Product/home',
							title: '支付插件',
						},{
							index: '/admin/Product/ProductReturnGoods',
							title: '退货信息',
						}]
					},
					{
						icon: 'el-icon-news',
						index: '3',
						title: '用户模块',
						permission:0,//1 显示 0不显示
						subs: [{
							index: '/admin/user/UserList',
							title: '用户列表',
						},{
							index: '/admin/user/UserType',
							title: '用户类型',
						}]
					},
					{
						icon: 'el-icon-edit',
						index: '4',
						title: '评论/留言模块',
						permission:0,//1 显示 0不显示
						subs: [{
							index: '/admin/comment',
							title: '评论管理',
						},{
							index: '/admin/message',
							title: '留言管理',
						}]
					},
                    {
                    	icon: 'el-icon-upload',
                    	index: '5',
                    	title: '图片/资源管理',
                    	permission:0,//1 显示 0不显示
                    	subs: [{
                    		index: '/admin/img',
                    		title: '图片空间',
                    	},{
                    		index: '/admin/rsc',
                    		title: '其他类型',
                    	},{
                    		index: '/admin/adImg',
                    		title: '广告图片',
                    	}]
                    },

					{
						icon: 'el-icon-setting',
						index: '6',
						title: '系统设置',
						permission:0,//1 显示 0不显示
						subs: [{
							index: '/admin/SiteInfo',
							title: '网站信息管理',
						},{
							index: '/admin/AdminList',
							title: '管理员列表',
						}]
					}
					/*{icon: 'el-icon-menu',
					    index: '1',
					    title: '主机监控',
					    subs: [
					        {
					            index: 'home',
					            title: '主机日志查询'
					        },{
					            index: 'crodigyLogCount',
					            title: '主机日志统计'
					        },
					         {
					            index: 'logChart',
					            title: '图表展示'
					        }
					    ]
					}
					,
					//add
					// {
					//     icon: 'el-icon-setting',
					//     index: 'readme222',
					//     title: '自述'
					//     // icon: 'el-icon-setting',
					//     // index: 'readme',
					//     // title: '日志监控'
					// },
					{
					    icon: 'el-icon-menu',
					    index: '2',
					    title: '表格',
					    subs: [
					        {
					            index: 'basetable',
					            title: '基础表格'
					        },
					        {
					            index: 'vuetable',
					            title: 'Vue表格组件'
					        }
					    ]
					},
					{
					    icon: 'el-icon-date',
					    index: '3',
					    title: '表单',
					    subs: [
					        {
					            index: 'baseform',
					            title: '基本表单'
					        },
					        {
					            index: 'vueeditor',
					            title: '编辑器'
					        },
					        {
					            index: 'markdown',
					            title: 'markdown'
					        },
					        {
					            index: 'upload',
					            title: '文件上传'
					        }
					    ]
					},
					{
					    icon: 'el-icon-star-on',
					    index: 'basecharts',
					    title: '图表'
					},
					{
					    icon: 'el-icon-upload2',
					    index: 'drag',
					    title: '拖拽'
					}
					*/
				]
			}
		},
		computed: {
			onRoutes() {
				console.log(this.$route.path.replace('/', ''));
				return this.$route.path.replace('/', '');
			},
			// roleType(){
			// 	let roleType = localStorage.getItem('roleType');
				
			// 	return roleType;
			// }
		}
	}
</script>

<style scoped>
	.sidebar {
		display: block;
		position: absolute;
		width: 250px;
		left: 0;
		top: 70px;
		bottom: 0;
		background: #2E363F;
	}
	
	.sidebar>ul {
		height: 100%;
	}
</style>
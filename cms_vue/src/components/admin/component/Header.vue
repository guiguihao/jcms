<template>
	<div class="header">
		<div class="user-info" style="border-radius: 0;float: left;padding-right: 0px;padding-left: 40px;">
				<img class="el-dropdown-link" :src="app.logo" style="width: 178px;height: 68px; text-align: left;padding-left: 0px;">
				</div>

		<div class="logo" style=" width: 60%;text-align: left;">
			<!--<img class="user-logo" src="../../../static/img/logo2.jpg" style="width: 18px;height: 18px; ">-->
			<font style="margin-left: 10px;">{{app.name}}后台管理系统</font>
				
		</div>
		
		<div class="user-info">
			<el-dropdown trigger="click" @command="handleCommand">
				<span class="el-dropdown-link" style="font-size: 18px;">
                    <img class="user-logo" src="../../../../static/img/img.jpg">
                    {{name}}
                </span>
              	
				<el-dropdown-menu slot="dropdown">
					<el-dropdown-item command="loginout">退出</el-dropdown-item>
				</el-dropdown-menu>
			</el-dropdown>
		</div>
	</div>
</template>
<script>
    import {hex_md5} from '../../../../static/js/common.js'
	export default {
		data() {
			return {
				app:{},
			}
		},
		created(){
           this.requestApp();
		},
		computed: {
			// username() {
			// 	let username = localStorage.getItem('ms_username');
			// 	return username ? username : this.name;
			// },
			name(){
//						localStorage.setItem('loginName', res.data.data.loginName);
//						localStorage.setItem('name', res.data.data.name);
//						localStorage.setItem('type', res.data.data.type);
				let userData = localStorage.getItem('userData');
				let user = JSON.parse(userData);
				let name = user.name;
				return name;
			}
			
		},
		methods: {
			handleCommand(command) {
				if(command == 'loginout') {
					
					this.requestData();
				}
			},
			requestData() {
				let self = this;
				if(process.env.NODE_ENV === 'development') { //TEST
					self.url = '/api/admin/logout';
				} else {
					self.url = '/admin/logout';
				}

				var params = {
					token: self.$token.getToken(),
				}
				self.loadingFlag = true;
				self.$axios.post(self.url, params).then((res) => {
					self.loadingFlag = false;
					if(res && res.data && res.data.code && res.data.code == 1) {
//						self.tableData = res.data.data.data;
//						self.totalCount = res.data.data.count;
						self.$message.success('注销成功');
						this.$router.push('/admin/login');
						localStorage.removeItem('appkey');
					    localStorage.removeItem('appsecret');
						
					} else {
						self.$message.error('服务器发生异常：' + res.data.msg);
					}
				}).catch(function(error) {
					self.$message('请求异常');
					//comJs.handleCommonRequestCallback('rer');
					
					self.loadingFlag = false;
					console.log('----error--' + JSON.stringify(error));
				
				});
			},
			requestApp() {
			  let self = this;

			  self.$request.siteInfo.getSiteinfo().then((res)=>{
			    if(res && res.data && res.data.code && res.data.code == 1) {
			      if (res.data.data) {
			        this.app = res.data.data;
			       }
			     } else {
			      self.$message(res.data.msg);
			    }

			  }).catch(function(error){
			    self.$message('请求异常');
			    console.log('---产品列表-error--' + JSON.stringify(error));
			  });
            }
		}
	}
</script>
<style scoped>
	.header {
		position: relative;
		box-sizing: border-box;
		width: 100%;
		height: 70px;
		font-size: 22px;
		line-height: 70px;
		color: #fff;
	}
	
	.header .logo {
		float: left;
		width: 250px;
		text-align: center;
	}
	
	.user-info {
		float: right;
		padding-right: 50px;
		font-size: 16px;
		color: #fff;
	
	}
	
	.user-info .el-dropdown-link {
		position: relative;
		display: inline-block;
		padding-left: 50px;
		color: #fff;
		cursor: pointer;
		vertical-align: middle;
	}
	
	.user-info .user-logo {
		position: absolute;
		left: 0;
		top: 15px;
		width: 40px;
		height: 40px;
		border-radius: 50%;
	}
	
	.el-dropdown-menu__item {
		text-align: center;
	}
</style>
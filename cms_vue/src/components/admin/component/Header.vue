<template>
	<div class="header">
		<div class="user-info" style="border-radius: 0;float: left;padding-right: 0px;padding-left: 40px;">
				<img class="el-dropdown-link" src="../../../../static/img/logo2_03.png" style="width: 128px;height: 18px; text-align: left;padding-left: 0px;">
				</div>

		<div class="logo" style=" width: 60%;text-align: left;">
			<!--<img class="user-logo" src="../../../static/img/logo2.jpg" style="width: 18px;height: 18px; ">-->
			<font style="margin-left: 10px;">后台系统</font>
				
		</div>
		
		<div class="user-info">
			<el-dropdown trigger="click" @command="handleCommand">
				<span class="el-dropdown-link" style="font-size: 18px;">
                    <img class="user-logo" src="../../../../static/img/img.jpg">
                    {{name}}   <span style="color: darkgrey;	">{{role_name}}</span>
                </span>
              	
				<el-dropdown-menu slot="dropdown">
					<el-dropdown-item command="loginout">退出</el-dropdown-item>
				</el-dropdown-menu>
			</el-dropdown>
		</div>
	</div>
</template>
<script>
	export default {
		data() {
			return {
				//name: ''
			}
		},
		computed: {
			username() {
				let username = localStorage.getItem('ms_username');
				return username ? username : this.name;
			},
			name(){
//						localStorage.setItem('loginName', res.data.data.loginName);
//						localStorage.setItem('name', res.data.data.name);
//						localStorage.setItem('type', res.data.data.type);
				let name = localStorage.getItem('name');
				return name;
			}
			,role_name(){
//						localStorage.setItem('loginName', res.data.data.loginName);
//						localStorage.setItem('name', res.data.data.name);
//						localStorage.setItem('type', res.data.data.type);
				let roleType = localStorage.getItem('roleType');
				let roleName ='';
				if(roleType==='AD'){
					roleName='超级管理员';
				}else if(roleType==='HM'){
					roleName='酒店经理';
				}else if(roleType==='HQ'){
					roleName='酒店前台';
				}else{
					roleName='角色异常';
				}
				return roleName;
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
					self.url = '/api/sys/logout';
				} else {
					self.url = '/sys/logout';
				}

				var params = {
				}
				self.loadingFlag = true;
				self.$axios.post(self.url, params).then((res) => {
					self.loadingFlag = false;
					if(res && res.data && res.data.code && res.data.code == 1) {
//						self.tableData = res.data.data.data;
//						self.totalCount = res.data.data.count;
						self.$message('注销成功');
						
						localStorage.removeItem('ms_username');
						localStorage.removeItem('token');
						this.$router.push('/login');
						
					} else {
						self.$message('服务器发生异常：' + res.data.msg);
					}
				}).catch(function(error) {
					self.$message('请求异常');
					//comJs.handleCommonRequestCallback('rer');
					
					self.loadingFlag = false;
					console.log('----error--' + JSON.stringify(error));
				
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
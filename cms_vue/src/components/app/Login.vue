<template>
<div class="login-wrap">


<div class="ms-title">app管理</div>
		<div class="ms-login">
			<el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">
				<el-form-item prop="username">
					<el-input v-model="ruleForm.username" placeholder="用户名"></el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input type="password" placeholder="密码" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')"></el-input>
				</el-form-item>
				<div class="login-btn">
					<el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
				</div>
				<!--  <p style="font-size:12px;line-height:30px;color:#999;">Tips : 用户名和密码随便填。</p>-->
			</el-form>
		</div>
</div>
</div>
</template>

<script>
	import {hex_md5} from '../../../static/js/common.js'
	export default {
		data: function() {
			return {
				ruleForm: {
					username: 'admin',
					password: '12345678'
				},
				rules: {
					username: [{
						required: true,
						message: '请输入用户名',
						trigger: 'blur'
					}],
					password: [{
						required: true,
						message: '请输入密码',
						trigger: 'blur'
					}]
				}
			}
		},
		methods: {
			submitForm(formName) {
				const self = this;
				self.$refs[formName].validate((valid) => {
					if(valid) {
						//localStorage.setItem('ms_username', self.ruleForm.username);
						self.requestData();
					} else {
						console.log('error submit!!');
						return false;
					}
				});
			},
			requestData() {
				let self = this;
				// if(process.env.NODE_ENV === 'development') { //TEST
				// 	self.url = '/api/sys/login';
				// } else {
				// 	self.url = '/sys/login';
				// }
				// //myTest();
				// var params = {
				// 	loginName: self.ruleForm.username,
				// 	loginPwd: hex_md5(self.ruleForm.password)

				// }

				if (self.ruleForm.username === 'admin' && self.ruleForm.password === '12345678') {
					self.loadingFlag = true;
					localStorage.setItem('ms_username', self.ruleForm.username);
				    localStorage.setItem('apptoken', "xxdssdxcsdsdsdsxxxsdxxsdsewwe");
				    self.$router.push('/app/');

				};


				
// 				self.$axios.post(self.url, params).then((res) => {
// 					self.loadingFlag = false;
// 					if(res && res.data && res.data.code && res.data.code == 1) {
// //						self.tableData = res.data.data.data;
// //						self.totalCount = res.data.data.count;
// 						self.$message('登录成功');
						
// 						localStorage.setItem('token', "xxdssdxcsdsdsdsxxxsdxxsdsewwe");
// 						self.$router.push('/home');
						
// 						//alert(JSON.stringify(res.data.data.loginName));
// 						localStorage.setItem('loginName', res.data.data.loginName);
// 						localStorage.setItem('name', res.data.data.name);
// 						localStorage.setItem('roleType', res.data.data.roleType);
						
// 					} else {
// 						self.$message('服务器发生异常：' + res.data.msg);
// 					}
// 				}).catch(function(error) {
// 					self.$message('请求异常');
// 					//comJs.handleCommonRequestCallback('rer');
					
// 					self.loadingFlag = false;
// 					console.log('----error--' + JSON.stringify(error));
				
// 				});
			}
		},//生命周期, 1.创建
		created() {
			console.log('--------------created-------------------------');
			//alert();
			//let token = localStorage.getItem('token');
          //  if(token){
           	//alert(localStorage.getItem('token'));
//         	  config.headers.Authorization = token;
			//  this.$router.push('/home');
          // }

		},
		mounted() {
			console.log('--------------mounted-------------------------');
		}
	}
</script>

<style scoped>
	.login-wrap {
		position: relative;
		width: 100%;
		height: 100%;
	}
	
	.ms-title {
		position: absolute;
		top: 50%;
		width: 100%;
		margin-top: -230px;
		text-align: center;
		font-size: 30px;
		color: #fff;
	}
	
	.ms-login {
		position: absolute;
		left: 50%;
		top: 50%;
		width: 300px;
		height: 160px;
		margin: -150px 0 0 -190px;
		padding: 40px;
		border-radius: 5px;
		background: #fff;
	}
	
	.login-btn {
		text-align: center;
	}
	
	.login-btn button {
		width: 100%;
		height: 36px;
	}
</style>
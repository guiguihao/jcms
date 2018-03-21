<template>
<div class="login-wrap">


<div class="ms-title">后台控制系统</div>
		<div class="ms-login">
			<el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">
				<el-form-item prop="username">
					<el-input v-model="ruleForm.username" placeholder="用户名"></el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input type="password" placeholder="密码" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')"></el-input>
				</el-form-item>
				<div class="login-btn">
					<el-button type="primary"  @click="submitForm('ruleForm')">登录</el-button>
				</div>
				<div class="login-btn">
					<el-button type="text" style="width: 80px" @click="register()">注册</el-button>
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
					password: 'admin888'
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
				if(process.env.NODE_ENV === 'development') { //TEST
					self.url = '/api/admin/login';
				} else {
					self.url = '/admin/login';
				}
				//myTest();
				let myToken = self.$token.getToken();
				var params = {
					name: self.ruleForm.username,
					password: hex_md5(self.ruleForm.password),
                    token:myToken
				}
				console.log(params);
				self.$axios.post(self.url, params).then((res) => {
					self.loadingFlag = false;
					if(res && res.data && res.data.code && res.data.code == 1) {
//						self.tableData = res.data.data.data;
//						self.totalCount = res.data.data.count;
					   // console.log(JSON.stringify(res.data));

						self.$message('登录成功');
						localStorage.setItem('userData',JSON.stringify(res.data.data));
						self.$router.push('/admin/home');
					} else {
						self.$message(res.data.msg);
					}
				}).catch(function(error) {
					self.$message('请求异常');
					//comJs.handleCommonRequestCallback('rer');
					self.loadingFlag = false;
					console.log('----error--' + JSON.stringify(error));
				
				});
			},

			register(){

				this.$router.push('/admin/register');
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
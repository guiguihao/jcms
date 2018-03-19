<template>
<div class="login-wrap">


<div class="ms-title">应用注册</div>
		<div class="ms-login">
			<el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">
			    <el-form-item prop="username">
					<el-input v-model="ruleForm.username" placeholder="用户名"></el-input>
				</el-form-item>
				<el-form-item prop="email">
					<el-input v-model="ruleForm.email" placeholder="邮箱"></el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input type="password" placeholder="密码" v-model="ruleForm.password" ></el-input>
				</el-form-item>
				<el-form-item prop="repassword">
					<el-input type="password" placeholder="重复密码" v-model="ruleForm.repassword" @keyup.enter.native="submitForm('ruleForm')"></el-input>
				</el-form-item>
				<div class="login-btn">
					<el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
				</div>
				  <p style="font-size:12px;line-height:30px;color:red;">Tips : 验证码邮件可能在垃圾邮件里。</p>
			</el-form>
		</div>

    <el-dialog title='激活账号' :visible.sync="dialogFormVisible">
       <p>您已注册成功,激活邮件已发送您邮箱,到请进入邮箱{{ruleForm.email}}激活账号</p>
       <p>注:邮件可能在垃圾邮件里面</p>
       <div slot="footer" class="dialog-footer">
         <el-button @click="requestSendActive()">{{resend}}</el-button>
         <el-button type="primary" @click="done">完 成</el-button>
       </div>
     </el-dialog>
</div>

 
</div>
</template>

<script>
	import {hex_md5} from '../../../static/js/common.js'
	export default {

		
		data: function() {
			var validatePass2 = (rule, value, callback) => {
			        if (value === '') {
			          callback(new Error('请再次输入密码'));
			        } else if (value !== this.ruleForm.password) {
			          callback(new Error('两次输入密码不一致!'));
			        } else {
			          callback();
			        }
			      };
			var validateEmail = (rule, value, callback) => {
				    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/; 
				    let rerule = reg.test(value);
			        if (value === '') {
			          callback(new Error('请输入邮箱'));
			        } 
			        else if (rerule === false) {
			          callback(new Error('邮箱格式不正确'));
			        } else {
			          callback();
			        }
			      };
			return {
				count :0,
                dialogFormVisible:false,
                resend:'',
                timer:null,
				ruleForm: {
					email:'',
					username: '',
					password: '',
					repassword:''
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
					}],
					repassword: [{
						validator: validatePass2, trigger: 'blur'
					}],
					email: [{
						validator: validateEmail, trigger: 'blur'
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
			requestSendActive() {
				if (this.count>0) {
                    this.$message('60秒后再试');
				}else{
					let self = this;
					if(process.env.NODE_ENV === 'development') { //TEST
						self.url = '/api/app/sendmial/activate';
					} else {
						self.url = '/app/sendmial/activate';
					}
					//myTest();
					let myToken = self.$token.getAppToken();
					var params = {
						toemail: self.ruleForm.email,
	                    token:myToken
					}
					// console.log(self.$token.getToken());
					self.$axios.post(self.url, params).then((res) => {
						self.loadingFlag = false;
						if(res && res.data && res.data.code && res.data.code == 1) {
	//						self.tableData = res.data.data.data;
	//						self.totalCount = res.data.data.count;
						   // console.log(JSON.stringify(res.data));
							self.dialogFormVisible = true;
							self.$message('激活邮件已发送至您的邮箱');
							self.getCode();

						} else {
							self.$message(res.data.msg);
						}
					}).catch(function(error) {
						self.$message('请求异常');
						//comJs.handleCommonRequestCallback('rer');
						self.loadingFlag = false;
						console.log('----error--' + JSON.stringify(error));
					
					});
                   
        
				}
				
			},
			requestData() {
				let self = this;
				if(process.env.NODE_ENV === 'development') { //TEST
					self.url = '/api/app/register';
				} else {
					self.url = '/app/register';
				}
				//myTest();
				let myToken = self.$token.getAppToken();
				var params = {
					name: self.ruleForm.username,
					email:self.ruleForm.email,
					password: self.ruleForm.password,
                    token:myToken
				}
				// console.log(self.$token.getToken());
				self.$axios.post(self.url, params).then((res) => {
					self.loadingFlag = false;
					if(res && res.data && res.data.code && res.data.code == 1) {
//						self.tableData = res.data.data.data;
//						self.totalCount = res.data.data.count;
					   // console.log(JSON.stringify(res.data));
						self.$message('注册成功');
						self.requestSendActive()
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
			getCode(formData){
			           if (!this.timer) {
			               this.count = 60;
			               this.show = false;
			               this.timer = setInterval(() => {
			                 if (this.count > 0 && this.count <= 60) {
			                   this.count--;
			                   this.resend = '已发送(' + this.count + ')'
			                 } else {
			                   // this.show = true;
			                   this.resend = '重新发送激活邮件'
			                   clearInterval(this.timer);
			                   this.timer = null;
			                 }
			               }, 1000)
			             }
			       },
			done(){
				this.dialogFormVisible = false;
                this.$router.push('/admin/login');
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
		},
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
		margin-top: -280px;
		text-align: center;
		font-size: 30px;
		color: #fff;
	}
	
	.ms-login {
		position: absolute;
		left: 50%;
		top: 50%;
		width: 300px;
		height: 360px;
		margin: -200px 0 0 -190px;
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
<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
     <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
     <el-breadcrumb-item>网站信息管理</el-breadcrumb-item>
   </el-breadcrumb>


   <div class ="mytable">
    <el-form ref="form" :model="form" label-width="120px">
       <el-form-item label="appkey" style="width: 380px">
        <el-input v-model="form.appkey" :disabled = "true"></el-input>
      </el-form-item>
       <el-form-item label="appsecret" style="width: 380px">
        <el-input v-model="appsecret" :disabled="true"></el-input>
      </el-form-item>
       <el-form-item label="应用名称" style="width: 280px">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="应用名称" style="width: 280px">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="网址" style="width: 280px">
        <el-input v-model="form.domian"></el-input>
      </el-form-item>
      <el-form-item label="图片空间地址" style="width: 360px">
        <el-input v-model="form.reserved_1"></el-input>
        <el-button type="text">默认共享图片地址:http://img.0566jh.com 私有图片空间地址设置教程,注:必须以http://开头</el-button>
      </el-form-item>
      <el-form-item label="Logo" style="width: 280px">
         <el-upload
           class="avatar-uploader"
           :action='form.reserved_1 + "/upload/saveImg.php"'
           :show-file-list="false"
           :data="imgdata"
           :on-success="handleAvatarSuccess"
           :before-upload="beforeAvatarUpload">
           <img v-if="imageUrl" :src="imageUrl" class="avatar">
           <i v-else class="el-icon-plus avatar-uploader-icon"></i>
         </el-upload>
      </el-form-item>
      <el-form-item label="网站状态" style="width: 280px" >
       <el-radio-group v-model="radio3">
        <el-radio-button label="开启"></el-radio-button>
        <el-radio-button label="关闭"></el-radio-button>
      </el-radio-group>
      </el-form-item>
      <el-form-item label="session" style="width: 280px" >
       <el-radio-group v-model="radio4">
        <el-radio-button label="开启"></el-radio-button>
        <el-radio-button label="关闭"></el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="网站备案号" style="width: 380px">
      <el-input v-model="form.beian"></el-input>
    </el-form-item>
    <el-form-item label="联系人Email" style="width: 280px">
      <el-input v-model="form.email"></el-input>
    </el-form-item>
    <el-form-item label="联系人电话" style="width: 280px">
      <el-input v-model="form.phone"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="ssonSubmit">保存</el-button>
    </el-form-item>
  </el-form>
</div>

</div>

</template>

<script>
  export default {
    created(){
      this.requestData();
      this._getappkeyAndSecret();
    },
    methods: {
      handleAvatarSuccess(res, file) {
        if (res.code == 1) {
           this.$message.success(res.msg);
           this.imageUrl = res.data.url;
           this.form.logo =  res.data.ourl;
         }else{
           this.$message.error(res.msg);
         }
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg' || 'image/png' || 'image/gif';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      handsss(){
        console.log(val);
      },
      ssonSubmit(){
        this.requestUpdateData();
      },
      requestUpdateData() {
        let self = this;
        //myTest();
        let myToken = self.$token.getToken();
        if (self.radio3==='开启') {
          self.form.status = 1;
        }else{
          self.form.status = 0;
        }
        if (self.radio4==='开启') {
          self.form.session = 1;
        }else{
          self.form.session = 0;
        }
        if (self.form.domian.indexOf('http')!=0) {
          self.form.domian = 'http://' + self.form.domian;
        }

        self.$request.siteInfo.updateSiteinfo(self.form).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
            self.$message.success('更新应用信息成功');
           this.requestData();
         } else {
          self.$message.error(res.data.msg);
        }

      }).catch(function(error){
        self.$message.error('请求异常');
        console.log('---产品列表-error--' + JSON.stringify(error));
      });
    },
    requestData() {
      let self = this;

      self.$request.siteInfo.getSiteinfo().then((res)=>{
        if(res && res.data && res.data.code && res.data.code == 1) {
          if (res.data.data) {
            self.form = res.data.data;
            if (self.form.status == 1) {
             self.radio3='开启';
           }else{
             self.radio3='关闭';
           }
           if (self.form.session == 1) {
             self.radio4='开启';
           }else{
             self.radio4='关闭';
           }
           this.imageUrl = self.form.reserved_1 + '/upload/' + res.data.data.logo;
             console.log(JSON.stringify(res.data));
           }
         } else {
          self.$message(res.data.msg);
        }

      }).catch(function(error){
        self.$message('请求异常');
        console.log('---产品列表-error--' + JSON.stringify(error));
      });

        // console.log(params);
      },

      _getappkeyAndSecret() {
        let self = this;

        self.$request.siteInfo.getAppkeyAndSecret().then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
               if (res.data.data.count>0) {
                console.log('===============')
                  let user = res.data.data.data[0];
                   console.log(user)
                  this.appsecret = user.appsecret;
               }

           } else {
            self.$message(res.data.msg);
          }

        }).catch(function(error){
          self.$message('请求异常');
          console.log('---产品列表-error--' + JSON.stringify(error));
        });

          // console.log(params);
        },
    },
    data() {
      return {
        appsecret:'',
        imgdata:{token:this.$token.getToken()}, 
        radio3:'关闭',
        radio4:'关闭',
        formLabelWidth: '80px',
        imageUrl: '',
        form: {

        },
      }
    }
  }
</script>


<style >
	.mytable{

    margin-top: 40px;

  }
  .mypage{
    margin-top: 20px;
  }
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
   .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
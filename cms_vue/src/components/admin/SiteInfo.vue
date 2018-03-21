<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>网站信息管理</el-breadcrumb-item>
	    </el-breadcrumb>


	    <div class ="mytable">
        <el-form ref="form" :model="form" label-width="120px">
          <el-form-item label="应用名称" style="width: 280px">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="网址" style="width: 280px">
            <el-input v-model="form.domian"></el-input>
          </el-form-item>
          <el-form-item label="网站状态" style="width: 280px" >
           <el-radio-group v-model="radio3">
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
    },
    methods: {
      handsss(){
        console.log(val);
      },
      ssonSubmit(){
        this.requestUpdateData();
      },
      requestUpdateData() {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/info/update';
        } else {
          self.url = '/app/admin/info/update';
        }
        //myTest();
        let myToken = self.$token.getToken();
        if (self.radio3==='开启') {
            self.form.status = 1;
        }else{
            self.form.status = 0;
        }
        var params = {
          set:self.form,
          token:myToken
        }
        // console.log(params);
        self.$axios.post(self.url, params).then((res) => {
          // console.log(JSON.stringify(res.data));
          if(res && res.data && res.data.code && res.data.code == 1) {
              this.requestData();
             // self.form = res.data.data;
             // console.log(JSON.stringify(res.data));

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
      requestData() {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/info/get';
        } else {
          self.url = '/app/admin/info/get';
        }
        //myTest();
        let myToken = self.$token.getToken();
        var params = {
          token:myToken
        }
        // console.log(params);
        self.$axios.post(self.url, params).then((res) => {
          // console.log(JSON.stringify(res.data));
          if(res && res.data && res.data.code && res.data.code == 1) {
             self.form = res.data.data;
             if (self.form.status == 1) {
                 self.radio3='开启';
             }else{
                 self.radio3='关闭';
             }
             // console.log(JSON.stringify(res.data));

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
    },
    data() {
      return {
        radio3:'关闭',
        formLabelWidth: '80px',
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
</style>
<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>3级分销设置</el-breadcrumb-item>
	    </el-breadcrumb>


	    <div class ="mytable">
        <el-form ref="form" :model="form" label-width="100px">
          <el-form-item label="分销状态" style="width: 280px" >
           <el-radio-group v-model="radio3">
                <el-radio-button label="开启"></el-radio-button>
                <el-radio-button label="关闭"></el-radio-button>
              </el-radio-group>
          </el-form-item>
          <el-form-item label="一级分销" >
            <el-input v-model.number="form.fx1" style="width: 60px" ></el-input> (分销比例0-1,三级分销比例总和不大于1,利润提成百分比,订单完成自动分配到账户)
          </el-form-item>
         
          <el-form-item label="二级分销" >
            <el-input v-model.number="form.fx2" style="width: 60px" ></el-input> (分销比例0-1,三级分销比例总和不大于1,利润提成百分比,订单完成自动分配到账户)
          </el-form-item>
          <el-form-item label="三级分销" >
            <el-input v-model.number="form.fx3" style="width: 60px" ></el-input> (分销比例0-1,三级分销比例总和不大于1,利润提成百分比,订单完成自动分配到账户)
          </el-form-item>
            <el-button type="primary" @click="ssonSubmit" style="margin-left: 40px;margin-top: 60px;">保存</el-button>
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
        //myTest();
        let myToken = self.$token.getToken();
        if (self.radio3==='开启') {
          self.form.status = 1;
        }else{
          self.form.status = 0;
        }

        self.$request.fenxiao.updateFenXiao(self.form).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
           this.requestData();
         } else {
          self.$message(res.data.msg);
        }

      }).catch(function(error){
        self.$message('请求异常');
        console.log('---产品列表-error--' + JSON.stringify(error));
      });
    },
    requestData() {
      let self = this;

      self.$request.fenxiao.getFenXiao().then((res)=>{
        if(res && res.data && res.data.code && res.data.code == 1) {
          if (res.data.data) {
            self.form = res.data.data;
            if (self.form.status == 1) {
             self.radio3='开启';
           }else{
             self.radio3='关闭';
           }
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
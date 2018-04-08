<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>退货信息管理</el-breadcrumb-item>
      </el-breadcrumb>


      <div class ="mytable">
        <el-form ref="form" :model="form" label-width="120px">
          <el-form-item label="收件人" style="width: 280px">
            <el-input v-model="form.receiver"></el-input>
          </el-form-item>
          <el-form-item label="手机" style="width: 280px">
            <el-input v-model="form.phone"></el-input>
          </el-form-item>
          <el-form-item label="电话" style="width: 280px">
            <el-input v-model="form.telephone"></el-input>
          </el-form-item>
          <el-form-item label="邮编" style="width: 380px">
            <el-input v-model="form.code"></el-input>
          </el-form-item>
          <el-form-item  label="收货地址" style="width: 580px">
            <el-input type="textarea" v-model="form.address"></el-input>
          </el-form-item>
          <el-form-item label="备注" style="width: 580px">
            <el-input type="textarea" v-model="form.mark"></el-input>
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
        self.$request.RequstReturnGoods.addUpReturnGoods(this.form).then((res)=>{
         console.log(JSON.stringify(res.data));
           if(res && res.data && res.data.code && res.data.code == 1) {
               self.$message('更新成功');
               this.requestData();
           } else {
             self.$message(res.data.msg);
           }
        }).catch(function(error){
         self.$message('请求异常');
          console.log('----error--' + JSON.stringify(error));
        });
      },
      requestData() {
        let self = this;
        self.$request.RequstReturnGoods.getReturnGoods().then((res)=>{
         console.log(JSON.stringify(res.data));
           if(res && res.data && res.data.code && res.data.code == 1) {
               if (res.data.data) {
                   self.form = res.data.data;
               }
           } else {
             self.$message(res.data.msg);
           }
        }).catch(function(error){
         self.$message('请求异常');
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
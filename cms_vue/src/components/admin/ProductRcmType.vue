<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>添加类别</el-breadcrumb-item>
      </el-breadcrumb>

      <div class ="mytable">
        <el-button v-on:click="addType">添加类别</el-button>
      </div>

      <div class ="mytable">
         <template>
           <el-table
             :data="tableData2"
             style="width: 100%"
            >
             <el-table-column
               prop="type.name"
               label="类别名称"
               width="200">
             </el-table-column>

              <el-table-column
               prop="type.dec"
               label="描述"
               width="300">
             </el-table-column>
         
             <el-table-column
               prop="type.level"
               width="160"
               label="排序(级别)">
             </el-table-column>

              <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.row)">编辑</el-button>
                     <el-button type="danger" size="small" v-on:click="del(scope.row)">删除</el-button>
                   </template>
              </el-table-column>
           </el-table>
         </template>
      </div>

     
      <el-dialog :title=title :visible.sync="dialogFormVisible">
       <el-form :model="form" :rules="rules" ref="form">
         <el-form-item label="类别名称" :label-width="formLabelWidth" prop = "name">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth" prop = "dec">
           <el-input v-model="form.dec" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="级别" :label-width="formLabelWidth" prop = "level">
           <el-input v-model.number="form.level" auto-complete="off" style="width: 80px;"></el-input>
         </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
         <el-button @click="dialogFormVisible = false">取 消</el-button>
         <el-button type="primary" @click="submitForm('form')">确 定</el-button>
       </div>
     </el-dialog>
    
    </div>

</template>

<script>
  export default {

    created(){
  
        this.requestData();

      },

    methods: {

      addType(){
        this.form={
          name: '',
          level: 1,
          dec:''
        };
        this.title='添加推荐类别';
        this.addOrEdit = true;
        this.dialogFormVisible = true;
      },
      edit(data){
        this.form = JSON.parse(JSON.stringify(data.type));
        this.title='编辑推荐类别';
        this.addOrEdit = false;
        this.dialogFormVisible = true;
      },
      del(data){
        this.form={
          del:0,
          _id:''
        };
        let ojc = JSON.parse(JSON.stringify(data.type));
        this.form.del = 1;
        this.form._id = ojc._id;
        this.requestUpData(this.form);

      },
      submitForm(formName){
         this.$refs[formName].validate((valid) => {
          if (valid) {
            if (this.addOrEdit) {
               this.requestAddData(this.form);
             }else{
               this.requestUpData(this.form);

             }

          } else {
            console.log(typeof(this.form.level));
            console.log('error submit!!');
            return false;
          }
        });

      },

      requestData() {
        let self = this;
         self.$request.type.getTypeList('shop_hot').then((res)=>{
          console.log(JSON.stringify(res.data));
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.tableData2 = res.data.data;
                this.dialogFormVisible = false;
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('----error--' + JSON.stringify(error));
         });
      },

      requestAddData(data) {
        let self = this;
        self.$request.type.addType('shop_hot',data).then((res)=>{
          // console.log(JSON.stringify(res.data));
            if(res && res.data && res.data.code && res.data.code == 1) {
                this.requestData();
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
           self.$message('请求异常');
           console.log('----error--' + JSON.stringify(error));
         });
        
      },


       requestUpData(data) {
        let self = this;
         self.$request.type.updateType(data).then((res)=>{
          // console.log(JSON.stringify(res.data));
            if(res && res.data && res.data.code && res.data.code == 1) {
                this.requestData();
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
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        tableData2: [],
        addOrEdit:false,
        form: {
          name: '',
          level: 1,
          dec:''
        },
        rules: {
          name: [
            { required: true, message: '请输入类别名称', trigger: 'blur' },
            { min: 2, max: 16, message: '长度在 2 到 16 个字符', trigger: 'blur' }
          ],
          dec: [
            { required: true, message: '请输入类别描述', trigger: 'blur' },
          ],
          level: [
            { required: true, message: '请输入级别', trigger: 'blur' },
            { type: 'number', message: '必须为数字值'}
          ],
        }
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
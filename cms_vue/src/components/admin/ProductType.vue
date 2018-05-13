<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>添加类别</el-breadcrumb-item>
      </el-breadcrumb>

      <div class ="mytable">
        <el-button v-on:click="addType">添加一级分类</el-button>
      </div>

      <div class ="mytable">
         <el-tree :data="tableData2" :props="defaultProps" :default-expand-all="true">
              <span class="custom-tree-node" slot-scope="{ node, data }">
                      <span>{{ node.label }}</span>
                      <span>
                        <el-button
                          type="text"
                          size="mini"
                          @click="() => append(data)">
                          添加子类
                        </el-button>
                        <el-button
                          type="text"
                          size="mini"
                          @click="() => edit(node, data)">
                          编辑
                        </el-button>
                        <el-button
                          type="text"
                          size="mini"
                          @click="() => remove(node, data)">
                          删除
                        </el-button>
                      </span>
                    </span>
         </el-tree>
      </div>

     
      <el-dialog :title=title :visible.sync="dialogFormVisible">
       <el-form :model="form" :rules="rules" ref="form">
         <el-form-item label="类别名称" :label-width="formLabelWidth" prop = "name">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth" prop = "dec">
           <el-input v-model="form.dec" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="icon" :label-width="formLabelWidth" >
           <el-input v-model="form.reserved_1" auto-complete="off" style="width: 300px;"></el-input>
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

      append(data){
         this.form={
          parentID:data.type._id,
          name: '',
          level: 1,
          dec:''  
        };
        this.title='添加一级分类';
        this.addOrEdit = true;
        this.dialogFormVisible = true;

      },
      remove(node, data) {
        this.form={
          del:0,
          _id:''
        };
        let ojc = JSON.parse(JSON.stringify(data.type));
        this.form.del = 1;
        this.form._id = ojc._id;
        console.log
        this.requestUpData(this.form);
       },
      addType(){
        this.form={
          name: '',
          level: 1,
          dec:''  
        };
        this.title='添加一级分类';
        this.addOrEdit = true;
        this.dialogFormVisible = true;
      },
      edit(node,data){
        this.form = JSON.parse(JSON.stringify(data.type));
        this.title='编辑类别';
        this.addOrEdit = false;
        this.dialogFormVisible = true;
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
         self.$request.type.getTypeList('shop').then((res)=>{
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
        self.$request.type.addType('shop',data).then((res)=>{
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
        },
        defaultProps: {
          children: 'children',
          label: 'title',
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
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 18px;
  }
</style>
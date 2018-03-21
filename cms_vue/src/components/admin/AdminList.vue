<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>管理员列表</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">添加管理员</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           >
	           <el-table-column
	             prop="name"
	             label="管理员"
	             width="200">
	           </el-table-column>
              <el-table-column
               width="360"
               label="权限">
               <template slot-scope="scope">
                   <span v-for="(item,index) in scope.row.permission">
                      <el-tag type="info" v-if="item == 1 && index == 0">系统设置</el-tag>
                      <el-tag type="info" v-if="item == 1 && index == 1">文章模块</el-tag>
                      <el-tag type="info" v-if="item == 1 && index == 2">产品模块</el-tag>
                      <el-tag type="info" v-if="item == 1 && index == 3">用户模块</el-tag>
                   </span>
                </template>
             </el-table-column>
             <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.row)" >编辑</el-button>
                     <el-button type="danger" size="small" v-if="scope.row.superadmin==0" v-on:click="del(scope.row)">删除</el-button>
                   </template>
              </el-table-column>
	         </el-table>
	       </template>
	    </div>

      <div class="mypage">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[20, 40, 60, 100]"
            :page-size='pagesize'
            layout="total, sizes, prev, pager, next"
            :total=total>
          </el-pagination>
        </div>

     
      <el-dialog title='添加管理员' :visible.sync="dialogFormVisible">
       <el-form :model="form" :rules="rules" ref="form">
         <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
           <el-input v-model="form.password" auto-complete="off" style="width: 160px;"></el-input> 
         </el-form-item>
         <el-form-item label="权限设置" :label-width="formLabelWidth">
              <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
              </el-checkbox-group>
         </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
         <el-button @click="dialogFormVisible = false">取 消</el-button>
         <el-button type="primary" @click="upUserSure('form')">确定</el-button>
       </div>
     </el-dialog>
	  
    </div>

</template>

<script>
  const cityOptions = ['文章模块', '产品模块', '系统设置', '用户模块'];
  export default {

    computed: {
  
    },
    methods: {
      upUserSure(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if (this.addOrEdit) {
              this.requestAddData(this.form);
            }else{
              this.requestUpdateData(this.form);
            }
          } 
        });
      },
      addType(data){
        this.form = {};
        this.checkedCities = [];
        this.addOrEdit = true;
        this.title='添加类别';
        this.dialogFormVisible = true;
      },
      edit(data){
        this.form = data;
        this.form.password = '';
        this.addOrEdit = false;
      	this.title='编辑类别';
        for (let item in this.form.permission) {
          if (this.form.permission[0] == 1) {this.checkedCities.push('系统设置')};
          if (this.form.permission[1] == 1) {this.checkedCities.push('文章模块')};
          if (this.form.permission[2] == 1) {this.checkedCities.push('产品模块')};
          if (this.form.permission[3] == 1) {this.checkedCities.push('用户模块')};
        }
        this.dialogFormVisible = true;
      },
      del(data){
        let obj = JSON.parse(JSON.stringify(data));
        obj.del = 1;
        this.requestUpdateData(obj);
      },
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
        this.pagesize = val;
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.currentPage = val;
        this.requestData();
      },
      handleCheckedCitiesChange(value) {
        let checkedCount = value.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;

        this.form.permission = [0,0,0,0];
        for (let item in value) {
          if (value[item] == '系统设置') {this.form.permission[0]=1};
          if (value[item] == '文章模块') {this.form.permission[1]=1};
          if (value[item] == '产品模块') {this.form.permission[2]=1};
          if (value[item] == '用户模块') {this.form.permission[3]=1};
        }
      },
      requestData() {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/list';
        } else {
          self.url = '/app/admin/list';
        }
        //myTest();
        let myToken = self.$token.getToken();
        var params = {
          page: self.currentPage,
          pageSize: self.pagesize,
          token:myToken
        }
        console.log(params);
        self.$axios.post(self.url, params).then((res) => {
          console.log(JSON.stringify(res.data));
          if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              this.dialogFormVisible = false;
//            self.totalCount = res.data.data.count;
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
      requestUpdateData(data) {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/update';
        } else {
          self.url = '/app/admin/update';
        }
        //myTest();
        let myToken = self.$token.getToken();
        var params = {
          _id: data._id,
          set:data,
          token:myToken
        }
        self.$axios.post(self.url, params).then((res) => {
          if(res && res.data && res.data.code && res.data.code == 1) {
             self.requestData();
             

          } else {
            self.$message(res.data.msg);
          }
        }).catch(function(error) {
          self.$message('请求异常');
          //comJs.handleCommonRequestCallback('rer');
          self.loadingFlag = false;
        
        });
      },

      requestAddData(data) {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/add';
        } else {
          self.url = '/app/admin/add';
        }
        //myTest();
        let myToken = self.$token.getToken();
        var params = {
          name: self.form.name,
          password:self.form.password,
          permission:self.form.permission,
          token:myToken
        }
        console.log(params);
        self.$axios.post(self.url, params).then((res) => {
          console.log(JSON.stringify(res.data));
          if(res && res.data && res.data.code && res.data.code == 1) {
             self.requestData();
              
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
    created(){
      this.requestData();
    },
    data() {
      return {
        addOrEdit:true,  //true添加 false编辑
        checkedCities: [],
        cities: cityOptions,
        isIndeterminate: true,
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        form: {
          name: '',
          password: '',
          permission: [0,0,0,0,0],
        },
        rules: {
          name: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
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
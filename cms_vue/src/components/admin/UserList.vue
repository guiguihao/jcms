<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>用户管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button type="text" style="color: #606266">类别</el-button>
	      <el-select v-model="userType" placeholder="请选择类别">
	                <el-option
	                    
	                     key=""
	                     label="所有"
	                     value="">
	               </el-option>
	            <el-option
	                     v-for="item in type"
	                     :key="item.type._id"
	                     :label="item.type.name"
	                     :value="item.type._id">
	               </el-option>
	       </el-select>

	       <el-input v-model="username" placeholder="请输入用户名" style="width: 160px;"></el-input>
	       <el-input v-model="userphone" placeholder="请输入手机号码" style="width: 160px;" ></el-input>
	       <el-input v-model="useremail" placeholder="请输入邮箱" style="width: 160px; "></el-input>
	       <el-button type="primary" icon="el-icon-search" v-on:click="query">搜索</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           >
	           <el-table-column
	             prop="name"
	             label="用户名"
	             width="160">
	           </el-table-column>
	           <el-table-column
	             prop="vip.name"
	             label="级别(vip)"
	             width="120">
	           </el-table-column>
	           <el-table-column
	                 width="100"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == 1" type="text" size="small" style='color: #67C23A'>正常</el-button>
	                   <el-button v-if="scope.row.status == 2" type="text" size="small" style='color: #F56C6C' >禁用</el-button>
	                 </template>
	            </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="注册日期">
	           </el-table-column>
	           
	            <el-table-column
	                 width="220"
	                 label="操作"
	                 >
	                 <template slot-scope="scope">
	                   <el-button type="primary" size="small" v-on:click="edit(scope.row)">编辑</el-button>
	                   <el-button type="danger" size="small"  v-on:click="del(scope.row)">删除</el-button>
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

	       <el-dialog title='管理用户' :visible.sync="dialogFormVisible">
	        <el-form :model="form" label-position="right" :rules="rules"  label-width="80px">
	          <el-form-item label=" 用户名"  style="width: 280px" prop = "name">
	            <el-input v-model="form.name" ></el-input>
	          </el-form-item>
	          <el-form-item label="用户类型" >
	            <el-select v-model="form.vip" placeholder="请选择类型">
	            
	               <el-option
	                     v-for="item in type"
	                     :key="item.type._id"
	                     :label="item.type.name"
	                     :value="item.type._id">
	               </el-option>
	             </el-select>
	          </el-form-item>
	          <el-form-item label="积分" prop = "integral">
	            <el-input v-model.number="form.integral"  style="width: 280px;" ></el-input>
	          </el-form-item>
	          <el-form-item label="手机号码" >
	            <el-input v-model="form.phone"  style="width: 280px;" ></el-input>
	          </el-form-item>
	          <el-form-item label="邮箱" >
	            <el-input v-model="form.email"  style="width: 280px;"></el-input>
	          </el-form-item>
	          <el-form-item label="状态" >
	            <el-select v-model="status" placeholder="请选择类别">
	              <el-option label="正常" value=1></el-option>
	               <el-option label="禁用" value=2></el-option>
	             </el-select>
	          </el-form-item>
	          <el-form-item label="注册时间" >
	            <el-input v-model="form.date" :disabled="true" style="width: 180px;"></el-input>
	          </el-form-item>
	          
	        </el-form>
	        <div slot="footer" class="dialog-footer">
	          <el-button @click="dialogFormVisible = false">取 消</el-button>
	          <el-button type="primary" @click="submit()">确 定</el-button>
	        </div>
	      </el-dialog>
    </div>
</template>

<script>
  export default {
  	watch:{
  		status: function (val) {
  		      if (val === '正常' || val === '1') {
  		      	this.form.status = 1;
  		      }else if (val === '禁用' || val === '2') {
  		      	this.form.status = 2;
  		      }else{
  		      	this.form.status = 0;
  		      }
  		},
  		userType: function (val) {

  		    let params = {
  		    	vip:val,
  		    }
  		    if (val === '') {
  		    	delete(params['vip'])
  		    }
  		    this.requestData(params);
  		},

  		
  	},
  	created(){

      this.requestData();
      this.requestUserType();

  	},
    methods: {
    	query(){

    		let params = {
  		    	name:this.username,
  		    	email:this.useremail,
  		    	phone:this.userphone,
  		    }
  		    if (this.username === '') {
  		    	delete(params['name'])
  		    }
  		    if (this.useremail === '') {
  		    	delete(params['email'])
  		    }
  		    if (this.userphone === '') {
  		    	delete(params['phone'])
  		    }
  		    this.requestData(params);

    	},
	   submit(){
	   	 for (let i in this.type) {
	   	 	let vip = this.type[i];
	   	 	if (this.form.vip === vip.type.name) {
	   	 		this.form.vip = vip.type._id;
	   	 	}
	   	 }
         // console.log(this.form);
         // let dic = {_id:data._id,del:1,};
         this.updataUser(this.form);
	  },
      edit(data){
      	this.form = JSON.parse(JSON.stringify(data));
      	this.form.vip = this.form.vip.name;
      	if (this.form.status === 1) {
      		this.status = '正常';
      	}else if (this.form.status === 2) {
      		this.status = '禁用';
      	}else {
      		this.status = '非法';
      	}
      	this.dialogFormVisible = true;
      },
      del(data){
         let dic = {_id:data._id,del:1,};
         this.updataUser(dic);
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
 
      //获取用户类型
      requestUserType(){
      	 let self = this;
         self.$request.type.getTypeList('user').then((res)=>{
         	// console.log(JSON.stringify(res.data));
         	  if(res && res.data && res.data.code && res.data.code == 1) {
         	      self.type = res.data.data;
         	     // console.log(JSON.stringify(self.type));  
         	  } else {
         	    self.$message(res.data.msg);
         	  }
         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('----error--' + JSON.stringify(error));
         });
      }, 

      //获取用户列表
      requestData(data) {
        let self = this;
        self.$request.user.getUserList(self.currentPage,self.pagesize,data).then((res)=>{
         	if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
             console.log(JSON.stringify(res.data.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('----error--' + JSON.stringify(error));
         });
        },

        //更新用户信息
        updataUser(dic){
        	 let self = this;
             self.$request.user.updateUser(dic).then((res)=>{
             	console.log(JSON.stringify(res.data));
             	  if(res && res.data && res.data.code && res.data.code == 1) {
             	     self.requestData();
             	     // console.log(JSON.stringify(self.type));  
             	  } else {
             	    self.$message(res.data.msg);
             	  }
             }).catch(function(error){
             	self.$message('请求异常');
             	 console.log('----error--' + JSON.stringify(error));
             });
        }
    },
    data() {
      return {
      	username:'',
      	useremail:'',
      	userphone:'',
      	status: 0,
      	formLabelWidth:120,
      	dialogFormVisible:false,
      	userType:'',
      	input:'',
      	pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        type:[],
        form: {
          name:'',
          vip:'',
        },
        rules: {
          name: [
            { required: true, message: '请输入类别名称', trigger: 'blur' },
            { min: 2, max: 16, message: '长度在 2 到 16 个字符', trigger: 'blur' }
          ],
          
          integral: [
            { required: true, message: '请输入积分', trigger: 'blur' },
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
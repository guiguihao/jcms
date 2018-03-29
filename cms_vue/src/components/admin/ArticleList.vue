<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>活动管理</el-breadcrumb-item>
	          <el-breadcrumb-item>活动列表</el-breadcrumb-item>
	          <el-breadcrumb-item>活动详情</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button>推荐</el-button>
	      <el-button>已发布</el-button>
	      <el-button>未发布</el-button>
	      <el-button>待审核</el-button>
	      <el-button type="text" style="color: #606266">类别</el-button>
	      <el-select v-model="productType" placeholder="请选择类别">
	            <el-option label="类别一" value="shanghai"></el-option>
	            <el-option label="类别二" value="beijing"></el-option>
	       </el-select>
	      <el-button v-on:click = "addArticle">添加文章</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           >
	           <el-table-column
	             prop="title"
	             label="标题"
	             width="360">
	           </el-table-column>
	           <el-table-column
	             prop="ArticleType"
	             label="类别"
	             width="120">
	           </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="日期">
	           </el-table-column>
	           <el-table-column
	                 width="130"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == '已发布'" type="text" size="small" style='color: #67C23A'>已发布</el-button>
	                   <el-button v-if="scope.row.status == '待审核'" type="text" size="small" style='color: #F56C6C' >待审核</el-button>
	                 </template>
	            </el-table-column>
               <el-table-column
	             prop="ArticleType"
	             label="推荐"
	             width="80">
	           </el-table-column>
	            <el-table-column
	                 width="220"
	                 label="操作"
	                 >
	                 <template slot-scope="scope">
	                   <el-button type="primary" size="small">查看</el-button>
	                   <el-button type="primary" size="small" v-on:click="edit">编辑</el-button>
	                   <el-button type="danger" size="small">删除</el-button>
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
	          :page-size="20"
	          layout="total, sizes, prev, pager, next, jumper"
	          :total="400">
	        </el-pagination>
	      </div>
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
	  addArticle(){
	  	this.$router.push('/admin/Article/ArticleEdit');
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
 
      //获取文章类型
      requestUserType(){
      	 let self = this;
         self.$request.type.getTypeList('article').then((res)=>{
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

      //添加文章
      requestAddData(data) {
        let self = this;
        self.$request.article.addArticle(data).then((res)=>{
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

      //获取文章列表
      requestData(data) {
        let self = this;
        self.$request.article.getArticleList(self.currentPage,self.pagesize,data).then((res)=>{
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

        //更新文章信息
        updataUser(dic){
        	 let self = this;
             self.$request.article.updateArticle(dic).then((res)=>{
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
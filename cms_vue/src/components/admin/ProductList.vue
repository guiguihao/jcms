<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>产品管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      
	      <el-button type="text" style="color: #606266">类别</el-button>
	      <el-cascader
	          :options="type"
	          v-model="articleType"
	          :props="props"
	          :show-all-levels="false" 
	          change-on-select
	         >
	      </el-cascader>
        <el-button type="text" style="color: #606266">推荐</el-button>
        <el-select v-model="recommend" placeholder="请选择类别">
               <el-option
                      
                       key=""
                       label="所有"
                       value="">
                 </el-option>
              <el-option
                       v-for="item in recommends"
                       :key="item.type._id"
                       :label="item.type.name"
                       :value="item.type._id">
                 </el-option>
         </el-select>
        <el-button v-on:click = "status = 3">已上架</el-button>
        <el-button v-on:click = "status = 2">仓库</el-button>
        <el-button v-on:click = "status = 0">待审核</el-button>
	      <el-button  type="primary" v-on:click = "addArticle">添加产品</el-button>
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
               <template slot-scope="scope">
                                      <img :src=scope.row.imgs[0] width="50" height="50"  style="float: left; margin-right: 15px">
                                     <el-button type="text" style="color: #606266">{{scope.row.title }}</el-button>
                 </template>
	           </el-table-column>
	           <el-table-column
	             prop="type.name"
	             label="类别"
	             width="120">
	           </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="日期">
	           </el-table-column>
	           <el-table-column
	             prop="recommend.name"
	             label="推荐"
	             width="80">
	           </el-table-column>
	           <el-table-column
	                 width="130"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == 3" type="text" size="small" style='color: #67C23A'>已上架</el-button>
                     <el-button v-if="scope.row.status == 2" type="text" size="small" style='color: #E6A23C'>仓库</el-button>
	                   <el-button v-if="scope.row.status == 0" type="text" size="small" style='color: #F56C6C' >待审核</el-button>
	                 </template>
	            </el-table-column>
	            <el-table-column
	                 width="220"
	                 label="操作"
	                 >
	                 <template slot-scope="scope">
	                   <el-button type="primary" size="small">预览</el-button>
	                   <el-button type="primary" size="small" v-on:click="edit(scope.row)">编辑</el-button>
	                   <el-button type="danger" size="small" v-on:click="del(scope.row)">删除</el-button>
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
	          :page-size=pagesize
	          layout="total, sizes, prev, pager, next, jumper"
	          :total=total>
	        </el-pagination>
	      </div>
    </div>
</template>

<script>
  export default {
  	watch:{
  		status: function (val) {
  		      let params = {
            status:val,
          }
          if (this.recommend != '') {
            params.recommend = this.recommend;
          }
           if (this.articleType != '') {
            params.type = this.articleType;
          }
          if (val === '') {
            delete(params['status'])
          }
          this.requestData(params);
  		},
  		articleType: function (val) {

  		    let params = {
  		    	type:val[val.length-1]._id,
  		    }
          if (this.recommend != '') {
            params.recommend = this.recommend;
          }
  		    if (val === '') {
  		    	delete(params['type'])
  		    }
  		    // console.log(params);
  		    this.requestData(params);
  		},
      recommend: function (val) {

          let params = {
            recommend:val,
          }
          if (this.articleType != '') {
            params.type = this.articleType[this.articleType.length-1]._id;
          }
          if (val === '') {
            delete(params['recommend'])
          }
          // console.log(params);
          this.requestData(params);
      },

  		
  	},
  	created(){

      this.requestData();
      this.requestUserType();
      this.requestRecommendType();

  	},
    methods: {
   
	  addArticle(){
	  	this.$router.push('/admin/Product/ProductEdit/0');
	  },
      edit(data){
      	this.$router.push('/admin/Product/ProductEdit/' + data._id);
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
         self.$request.type.getTypeList('shop').then((res)=>{
         	// console.log(JSON.stringify(res.data));
         	  if(res && res.data && res.data.code && res.data.code == 1) {
         	      self.type = res.data.data;
         	     console.log(JSON.stringify(self.type));  
         	  } else {
         	    self.$message(res.data.msg);
         	  }
         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('---article-error--' + JSON.stringify(error));
         });
      }, 


      //获取推荐类型
      requestRecommendType(){
         let self = this;
         self.$request.type.getTypeList('shop_hot').then((res)=>{
          // console.log(JSON.stringify(res.data));
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.recommends = res.data.data;
               // console.log(JSON.stringify(self.type));  
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('--article_hot--error--' + JSON.stringify(error));
         });
      }, 

      //获取产品列表
      requestData(data) {
        let self = this;
        self.$request.product.getProductList(self.currentPage,self.pagesize,data).then((res)=>{
         	if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
             console.log(JSON.stringify(res.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('---产品列表-error--' + JSON.stringify(error));
         });
        },

        //更新文章信息
        updataUser(dic){
        	 let self = this;
             self.$request.product.updateProduct(dic).then((res)=>{
             	console.log(JSON.stringify(res.data));
             	  if(res && res.data && res.data.code && res.data.code == 1) {
             	     self.requestData();
             	     // console.log(JSON.stringify(self.type));  
             	  } else {
             	    self.$message(res.data.msg);
             	  }
             }).catch(function(error){
             	self.$message('请求异常');
             	 console.log('-更新文章信息---error--' + JSON.stringify(error));
             });
        }
    },
    data() {
      return {
        status:-1,
        recommends:[],
        recommend:'',
        articleType:[],
      	status: 0,
      	formLabelWidth:120,
      	dialogFormVisible:false,
      	userType:'',
        total:'',
        type:[],
      	pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        props: {
          value: 'type',
          label: 'title',
          children: 'children'
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
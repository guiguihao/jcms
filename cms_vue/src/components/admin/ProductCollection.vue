<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>收藏管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      
	       <el-input v-model="uid" placeholder="请输入用户id" style="width: 350px; "></el-input>
         <el-button type="primary" icon="el-icon-search" v-on:click="query">搜索</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           >
	           <el-table-column
	             prop="title"
	             label="标题"
	             width="360">
               <template slot-scope="scope">
                                      <img :src="siteInfo.reserved_1 +'/upload/' + scope.row.product.imgs[0]" width="50" height="50"  style="float: left; margin-right: 15px">
                                     <el-button type="text" style="color: #606266">{{scope.row.product.title }}</el-button>
                 </template>
	           </el-table-column>
	           <el-table-column
	             prop="user.name"
	             label="收藏用户"
	             width="120">
	           </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="收藏日期">
	           </el-table-column>
	            <el-table-column
	                 width="220"
	                 label="操作"
	                 >
	                 <template slot-scope="scope">
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
  		uid: function (val) {
  		      let params = {
            userId:val,
          }
         
          if (val === '') {
            delete(params['userId'])
          }
          this.requestData(params);
  		},
  		
  	},
  	created(){
      this.siteInfo =  this.$orther.getSiteInfo();
      this.requestData();

  	},
    methods: {

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
 
      //获取收藏列表
      requestData(data) {
        let self = this;
        self.$request.collection.getCollections(self.currentPage,self.pagesize,data).then((res)=>{
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
             self.$request.collection.updateCollection(dic).then((res)=>{
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
        siteInfo:{},
      	status: 0,
      	formLabelWidth:120,
      	dialogFormVisible:false,
      	uid:'',
        type:[],
      	pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
       
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
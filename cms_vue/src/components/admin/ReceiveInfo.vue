<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>收货地址</el-breadcrumb-item>
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
	             prop="user.name"
	             label="用户name"
	             width="150">
           
	           </el-table-column>
             <el-table-column
               prop="name"
               label="收件人"
               width="150">
           
             </el-table-column>
	           <el-table-column
	             prop="phone"
	             label="电话"
	             width="100">
	           </el-table-column>
             <el-table-column
               prop="mphone"
               label="手机"
               width="150">
             </el-table-column>
             <el-table-column
               prop="province"
               label="省份"
               width="100">
             </el-table-column>
           
             <el-table-column
               prop="city"
               label="城市"
               width="100">
             </el-table-column>
               <el-table-column
               prop="area"
               label="区"
               width="100">
             </el-table-column>
              <el-table-column
               prop="address"
               label="详细地址"
               width="360">
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
 
      //获取收货地址
      requestData(data) {
        let self = this;
        self.$request.receiveInfo.getReceiveInfo(self.currentPage,self.pagesize,data).then((res)=>{
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

        //更新收货地址
        updataUser(dic){
        	 let self = this;
             self.$request.receiveInfo.updateReceiveInfo(dic).then((res)=>{
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
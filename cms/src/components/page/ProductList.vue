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
	      <el-button>已下架</el-button>

	      <el-button type="text" style="color: #606266">类别</el-button>
	      <el-select v-model="productType" placeholder="请选择类别">
	            <el-option label="类别一" value="shanghai"></el-option>
	            <el-option label="类别二" value="beijing"></el-option>
	       </el-select>
	      <el-button>添加产品</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="产品名称"
	             width="360">
	           </el-table-column>
	          
	           <el-table-column
	             prop="Price"
	             width="160"
	             label="价格">
	           </el-table-column>
	           <el-table-column
	                 width="130"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == '已发布'" type="text" size="small" style='color: #67C23A'>已发布</el-button>
	                   <el-button v-if="scope.row.status == '已下架'" type="text" size="small" style='color: #F56C6C' >已下架</el-button>
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
    methods: {
      tableRowClassName({row, rowIndex}) {
        if (row.status == '已下架') {
          return 'warning-row';
        } 
        return '';
      },
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      edit(){
      	this.$router.push({ name: 'ProductEdit', params: 123});
      }
    },
    data() {
      return {
      	productType:'',
      	currentPage: 2,
        tableData2: [{
          status:'已发布',
          ArticleType:'已推荐',
          date: '2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
          Price:'111',

        }, {
          status:'已下架',
          ArticleType:'已推荐',
          date: '2016-05-04',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
          Price:'111'
        }, {
          ArticleType:'已推荐',
          date: '2016-05-01',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
          Price:'111'
        }, {
          ArticleType:'已推荐',
          date: '2016-05-03',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
          Price:'111'
        }]
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
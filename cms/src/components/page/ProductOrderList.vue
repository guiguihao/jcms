<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>活动管理</el-breadcrumb-item>
	          <el-breadcrumb-item>活动列表</el-breadcrumb-item>
	          <el-breadcrumb-item>订单管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button>全部</el-button>
	      <el-button>待付款</el-button>
	      <el-button>待发货</el-button>
	      <el-button>已发货</el-button>
	      <el-button>已完成</el-button>
	      <el-button>退款中</el-button>
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
	             width="120"
	             label="原价">
	           </el-table-column>
	            <el-table-column
	             prop="Price"
	             width="120"
	             label="实付价格">
	           </el-table-column>
	           <el-table-column
	                 width="130"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == '已发布'" type="text" size="small" style='color: #67C23A'>已完成</el-button>
	                   <el-button v-if="scope.row.status == '已下架'" type="text" size="small" style='color: #F56C6C' >待付款</el-button>
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

	     <el-dialog :title=title :visible.sync="dialogFormVisible">
	      <el-form :model="form">
	        <el-form-item label="产品名称" :label-width="formLabelWidth">
	          <el-input v-model="form.name" auto-complete="off" :disabled="true" style="width: 300px;"></el-input>
	        </el-form-item>
	        <el-form-item label="价格" :label-width="formLabelWidth">
	          <el-input v-model="form.sort" auto-complete="off" :disabled="true" style="width: 80px;"></el-input>
	        </el-form-item>
	        <el-form-item label="实付价格"  :label-width="formLabelWidth">
	          <el-input v-model="form.sort" auto-complete="off"  style="width: 80px;"></el-input>
	        </el-form-item>
	        <el-form-item label="优惠嘛" :label-width="formLabelWidth">
	          <el-input v-model="form.sort" auto-complete="off" :disabled="true"  style="width: 80px;"></el-input>
	        </el-form-item>
	        <el-form-item label="参加的活动" :label-width="formLabelWidth">
	          <el-tag type="info">XXX大促</el-tag>
	        </el-form-item>
	        <el-form-item label="状态" :label-width="formLabelWidth">
	         <el-select v-model="form.region" placeholder="请选择活动区域">
	               <el-option label="已发货" value="shanghai"></el-option>
	               <el-option label="已完成" value="beijing"></el-option>
	             </el-select>
	        </el-form-item>
	        <el-form-item label="买家ID" :label-width="formLabelWidth">
	          <el-button type="text">xxxxx</el-button>
	        </el-form-item>
	        <el-form-item label="买家手机" :label-width="formLabelWidth">
	          <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
	        </el-form-item>
	        <el-form-item label="收货地址" :label-width="formLabelWidth">
	          <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
	        </el-form-item>
	      </el-form>
	      <div slot="footer" class="dialog-footer">
	        <el-button @click="dialogFormVisible = false">取 消</el-button>
	        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
	      </div>
	    </el-dialog>
    </div>
</template>

<script>
  export default {
    methods: {
     
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      edit(){
      	this.dialogFormVisible=true;
      }
    },
    data() {
      return {
      	dialogFormVisible: false,
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
        }],
        form: {
          name: '222',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: '',
          sort:1
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
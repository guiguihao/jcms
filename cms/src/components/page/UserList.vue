<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>用户管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button type="text" style="color: #606266">类别</el-button>
	      <el-select v-model="productType" placeholder="请选择类别">
	            <el-option label="类别一" value="shanghai"></el-option>
	            <el-option label="类别二" value="beijing"></el-option>
	       </el-select>

	       <el-input v-model="input" placeholder="请输入用户名或手机号码或邮箱" style="width: 300px; margin-left: 100px"></el-input>
	       <el-button type="primary" icon="el-icon-search">搜索</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="用户名"
	             width="160">
	           </el-table-column>
	           <el-table-column
	             prop="ArticleType"
	             label="级别"
	             width="120">
	           </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="注册日期">
	           </el-table-column>
	           <el-table-column
	                 width="130"
	                 label="状态"
	                 >
	                 <template slot-scope="scope">
	                   <el-button v-if="scope.row.status == '正常'" type="text" size="small" style='color: #67C23A'>正常</el-button>
	                   <el-button v-if="scope.row.status == '禁用'" type="text" size="small" style='color: #F56C6C' >禁用</el-button>
	                 </template>
	            </el-table-column>
	            <el-table-column
	                 width="220"
	                 label="操作"
	                 >
	                 <template slot-scope="scope">
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

	       <el-dialog title='管理用户' :visible.sync="dialogFormVisible">
	        <el-form :model="form" label-width="80px">
	          <el-form-item label="用户名" :label-width="formLabelWidth">
	            <el-input v-model="form.name" style="width: 300px;"></el-input>
	          </el-form-item>
	          <el-form-item label="会员等级" :label-width="formLabelWidth">
	            <el-select v-model="productType" placeholder="请选择类别">
	               <el-option label="等级1" value="shanghai"></el-option>
	               <el-option label="类别二" value="beijing"></el-option>
	             </el-select>
	          </el-form-item>
	          <el-form-item label="手机号码" :label-width="formLabelWidth">
	            <el-input v-model="form.sort"  style="width: 80px;"></el-input>
	          </el-form-item>
	          <el-form-item label="邮箱" :label-width="formLabelWidth">
	            <el-input v-model="form.sort"  style="width: 80px;"></el-input>
	          </el-form-item>
	          <el-form-item label="状态" :label-width="formLabelWidth">
	            <el-select v-model="productType" placeholder="请选择类别">
	              <el-option label="等级1" value="shanghai"></el-option>
	               <el-option label="类别二" value="beijing"></el-option>
	             </el-select>
	          </el-form-item>
	          <el-form-item label="注册时间" :label-width="formLabelWidth">
	            <el-input v-model="form.sort"  style="width: 80px;"></el-input>
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
      	this.dialogFormVisible = true;
      }
    },
    data() {
      return {
      	dialogFormVisible:false,
      	currentPage: 2,
        tableData2: [{
          status:'正常',
          ArticleType:'普通',
          date: '2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'禁用',
          ArticleType:'普通',
          date: '2016-05-04',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          ArticleType:'普通',
          date: '2016-05-01',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          ArticleType:'vip',
          date: '2016-05-03',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
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
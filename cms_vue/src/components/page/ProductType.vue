<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>添加类别</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">添加类别</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="类别名称"
	             width="200">
	           </el-table-column>
              <el-table-column
               prop="sort"
               width="160"
               label="推荐">
             </el-table-column>
	           <el-table-column
	             prop="sort"
	             width="160"
	             label="排序">
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

     
      <el-dialog :title=title :visible.sync="dialogFormVisible">
       <el-form :model="form">
         <el-form-item label="类别名称" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="排序" :label-width="formLabelWidth">
           <el-input v-model="form.sort" auto-complete="off" style="width: 80px;"></el-input>
         </el-form-item>
         <el-form-item label="推荐" :label-width="formLabelWidth">
              <el-radio-group  v-model="form.resource" >
                <el-radio label="级别1"></el-radio>
                <el-radio label="级别2"></el-radio>
                <el-radio label="级别3"></el-radio>
              </el-radio-group>
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
     
      addType(){
        this.title='添加类别';
        this.dialogFormVisible = true;
      },
      edit(){
      	this.title='编辑类别';
        this.dialogFormVisible = true;
      }
    },
    data() {
      return {
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        tableData2: [{
          status:'已发布',
          sort:1,
          source:'转发',
          date: '2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'待审核',
          sort:1,
          source:'转发',
          date: '2016-05-04',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          source:'转发',
          sort:1,
          date: '2016-05-01',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          source:'转发',
          sort:1,
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
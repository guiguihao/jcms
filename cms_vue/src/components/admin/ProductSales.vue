<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>活动管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">添加促销活动</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="名称"
	             width="200">
	           </el-table-column>
             <el-table-column
               prop="date"
               width="220"
               label="日期">
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
         <el-form-item label="活动名称" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="开始时间">
             <el-col :span="7">
               <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 160px;"></el-date-picker>
             </el-col>
             <el-col class="line" :span="2">-</el-col>
             <el-col :span="7">
               <el-time-picker type="fixed-time" placeholder="选择时间" v-model="form.date2" style="width: 160px;"></el-time-picker>
             </el-col>
           </el-form-item>
           <el-form-item label="结束时间">
             <el-col :span="7">
               <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 160px;"></el-date-picker>
             </el-col>
             <el-col class="line" :span="2">-</el-col>
             <el-col :span="7">
               <el-time-picker type="fixed-time" placeholder="选择时间" v-model="form.date2" style="width: 160px;"></el-time-picker>
             </el-col>
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
        this.$router.push({ name: 'ProductSaleEdit', query: {userId: 123}});
      },
      edit(){
      	this.$router.push({ name: 'ProductSaleEdit', query: {userId: 123}});
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
          date: '2016-05-02 --- 2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'待审核',
          sort:1,
          source:'转发',
          date: '2016-05-02 --- 2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          source:'转发',
          sort:1,
          date: '2016-05-02 --- 2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          source:'转发',
          sort:1,
          date: '2016-05-02 --- 2016-05-02',
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
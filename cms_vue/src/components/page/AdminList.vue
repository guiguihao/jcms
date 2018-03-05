<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>管理员列表</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">添加管理员</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="管理员"
	             width="200">
	           </el-table-column>
              <el-table-column
               prop="status"
               width="160"
               label="权限">
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

     
      <el-dialog title='添加管理员' :visible.sync="dialogFormVisible">
       <el-form :model="form">
         <el-form-item label="用户名" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="密码" :label-width="formLabelWidth">
           <el-input v-model="form.sort" auto-complete="off" style="width: 160px;"></el-input> 
         </el-form-item>
         <el-form-item label="权限设置" :label-width="formLabelWidth">
              <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
              </el-checkbox-group>
         </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
         <el-button @click="dialogFormVisible = false">取 消</el-button>
         <el-button type="primary" @click="dialogFormVisible = false">确定</el-button>
       </div>
     </el-dialog>
	  
    </div>

</template>

<script>
  const cityOptions = ['文章模块', '产品模块', '系统设置', '用户模块'];
  export default {
    methods: {
     
      addType(){
        this.title='添加类别';
        this.dialogFormVisible = true;
      },
      edit(){
      	this.title='编辑类别';
        this.dialogFormVisible = true;
      },
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      handleCheckedCitiesChange(value) {
        let checkedCount = value.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
      }
    },
    data() {
      return {
        checkedCities: [],
        cities: cityOptions,
        isIndeterminate: true,
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        tableData2: [{
          status:'文章,产品',
          sort:'20%',
          source:'转发',
          date: '2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'文章',
          sort:1,
          source:'转发',
          date: '2016-05-04',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          status:'文章',
          sort:1,
          date: '2016-05-01',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'产品',
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
          sort:'20'
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
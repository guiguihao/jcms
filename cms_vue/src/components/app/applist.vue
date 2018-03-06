<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>应用列表</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">添加应用</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           >
	           <el-table-column
	             prop="title"
	             label="应用名称"
	             width="200">
	           </el-table-column>
              <el-table-column
               prop="status"
               width="260"
               label="appkey">
             </el-table-column>
              <el-table-column
               prop="status"
               width="260"
               label="appsecret">
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

     
      <el-dialog :title=title :visible.sync="dialogFormVisible">
       <el-form :model="form">
         <el-form-item label="应用名称" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="应用范围" :label-width="formLabelWidth">
              <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
              </el-checkbox-group>
         </el-form-item>
         <el-form-item v-if=domain label="域名" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item v-if=appid label="android包名" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item v-if=appid label="ios Bundle ID" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
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
  const cityOptions = ['web', 'app'];
  export default {
    methods: {
     
      addType(){
        this.title='添加应用';
        this.dialogFormVisible = true;
      },
      edit(){
      	this.title='编辑应用';
        this.dialogFormVisible = true;
      },
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      handleCheckedCitiesChange(value) {
        this.domain = false;
        this.appid = false;
      	for (var i = 0; i < value.length; i++) {
      		let checkValue = value[i];
      		if (checkValue === 'web') {
      			this.domain = true;
      		};
      		if (checkValue === 'app') {
      			this.appid = true;
      		};
      	};
        let checkedCount = value.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
      }
    },
    data() {
      return {
      	domain:false,
      	appid:false,
        checkedCities: [],
        cities: cityOptions,
        isIndeterminate: true,
        formLabelWidth: '120px',
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
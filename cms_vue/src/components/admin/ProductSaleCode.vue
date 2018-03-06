<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>优惠码</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	      <el-button v-on:click="addType">生成优惠码</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           style="width: 100%"
	           :row-class-name="tableRowClassName">
	           <el-table-column
	             prop="title"
	             label="优惠码"
	             width="200">
	           </el-table-column>
              <el-table-column
               prop="status"
               width="160"
               label="状态">
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

     
      <el-dialog title='生成优惠码' :visible.sync="dialogFormVisible">
       <el-form :model="form">
         <el-form-item label="生成数量" :label-width="formLabelWidth">
           <el-input v-model="form.name" auto-complete="off" style="width: 300px;"></el-input>
         </el-form-item>
         <el-form-item label="优惠幅度" :label-width="formLabelWidth">
           <el-input v-model="form.sort" auto-complete="off" style="width: 80px;"></el-input> *例产品原价100 优惠幅度20 实际价格为100*20%
         </el-form-item>
         <el-form-item label="适用产品" :label-width="formLabelWidth">
              <el-table
                    :data="tableData2"
                    style="width: 100%"
                    :row-class-name="tableRowClassName"
                    @selection-change="handleSelectionChange">
                    <el-table-column
                          type="selection"
                          width="55">
                        </el-table-column>
                    <el-table-column
                      prop="title"
                      label="产品名称"
                      width="360">
                    </el-table-column>
              </el-table>
              <div class="mypage">
                  <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[20, 40, 60, 100]"
                    :page-size="20"
                    layout="total, prev, pager, next"
                    :total="400">
                  </el-pagination>
                </div>
         </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
         <el-button @click="dialogFormVisible = false">取 消</el-button>
         <el-button type="primary" @click="dialogFormVisible = false">生成</el-button>
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
      },
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
    },
    data() {
      return {
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        tableData2: [{
          status:'有效',
          sort:'20%',
          source:'转发',
          date: '2016-05-02',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄',
        }, {
          status:'失效',
          sort:1,
          source:'转发',
          date: '2016-05-04',
          title: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          status:'已用',
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
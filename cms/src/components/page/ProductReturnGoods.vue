<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>退货信息</el-breadcrumb-item>
	    </el-breadcrumb>


	    <div class ="mytable">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="退货地址">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="收件人" style="width: 280px">
           <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="手机号码" style="width: 280px">
           <el-input v-model="form.name" ></el-input>
          </el-form-item>
           <el-form-item label="邮编" style="width: 180px">
           <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">保存</el-button>
          </el-form-item>
        </el-form>
      </div>
	  
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
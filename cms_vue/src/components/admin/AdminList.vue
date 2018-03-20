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
	           >
	           <el-table-column
	             prop="name"
	             label="管理员"
	             width="200">
	           </el-table-column>
              <el-table-column
               width="160"
               label="权限">
               <template slot-scope="scope">
                   <span v-for="item in scope.row.permission">
                      {{item}}
                   </span>
                </template>
             </el-table-column>
             <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit" >编辑</el-button>
                     <el-button type="danger" size="small" v-if="scope.row.superadmin==0">删除</el-button>
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
            :page-size='pagesize'
            layout="total, sizes, prev, pager, next"
            :total=total>
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
        this.pagesize = val;
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.currentPage = val;
        this.requestData();
      },
      handleCheckedCitiesChange(value) {
        let checkedCount = value.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
      },
      requestData() {
        let self = this;
        if(process.env.NODE_ENV === 'development') { //TEST
          self.url = '/api/app/admin/list';
        } else {
          self.url = '/app/admin/list';
        }
        //myTest();
        let myToken = self.$token.getToken();
        var params = {
          page: self.currentPage,
          pageSize: self.pagesize,
          token:myToken
        }
        console.log(params);
        self.$axios.post(self.url, params).then((res) => {
          console.log(JSON.stringify(res.data));
          if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
//            self.totalCount = res.data.data.count;
             // console.log(JSON.stringify(res.data));

          } else {
            self.$message(res.data.msg);
          }
        }).catch(function(error) {
          self.$message('请求异常');
          //comJs.handleCommonRequestCallback('rer');
          self.loadingFlag = false;
          console.log('----error--' + JSON.stringify(error));
        
        });
      },

    },
    created(){
      this.requestData();
    },
    data() {
      return {
        checkedCities: [],
        cities: cityOptions,
        isIndeterminate: true,
        formLabelWidth: '80px',
        dialogFormVisible: false,
        title:'111',
        pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
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
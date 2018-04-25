<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>评论管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	       <el-input v-model="oid" placeholder="请输入产品或文章_id" style="width: 350px; "></el-input>
         <el-button type="primary" icon="el-icon-search" v-on:click="query">搜索</el-button>
	     
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           >
	           <el-table-column
	             prop="oid"
	             label="oid"
	             width="260">
              
	           </el-table-column>
	           <el-table-column
	             prop="content"
	             label="内容"
	             width="360">
	           </el-table-column>
             <el-table-column
                   width="260"
                   label="图片"
                   >
                   <template slot-scope="scope">
                        <span v-for = "img in scope.row.imgs">
                           <img :src=img width="50" height="50"  style="float: left; margin-right: 15px">
                        </span>
                   </template>
              </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="日期">
	           </el-table-column>
             <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.row)" >编辑</el-button>
                     <el-button type="danger" size="small" v-on:click="del(scope.row)">删除</el-button>
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
	          :page-size=pagesize
	          layout="total, sizes, prev, pager, next, jumper"
	          :total=total>
	        </el-pagination>
	      </div>

         <el-dialog :title=title :visible.sync="dialogFormVisible">
          <el-form :model="form"  ref="form" label-width="80px">
            <el-form-item label="oid">
              <el-input v-model="form.oid" :disabled="true" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
             <el-form-item label="内容">
              <el-input v-model="form.content" type="textarea" :autosize="{ minRows: 2, maxRows: 6}" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
            <el-form-item label="评分" >
              <el-input v-model.number="form.level" auto-complete="off" style="width: 80px;"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitForm('form')">确 定</el-button>
          </div>
        </el-dialog>
    </div>


</template>

<script>
  export default {
  	watch:{
  		
      oid: function (val) {

          let params = {
            oid:val,
          }
          if (val === '') {
            delete(params['oid'])
          }
          // console.log(params);
          this.requestData(params);
      },

  		
  	},
  	created(){

      this.requestData();
    

  	},
    methods: {
   
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
        this.pagesize = val;
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.currentPage = val;
        this.requestData();
      },
   
      query(){
          let params = {
            oid:this.oid,
          }
          if (this.oid === '') {
            delete(params['oid'])
          }
          // console.log(params);
          this.requestData(params);
      },
      submitForm(){
          this.updataCommnt(this.form);
      },
      edit(data){
        this.form = data;
        this.addOrEdit = false;
        this.title='编辑评论/留言';
        this.dialogFormVisible = true;

      },
      del(data){
        let obj = JSON.parse(JSON.stringify(data));
        obj.del = 1;
        this.updataCommnt(obj);
      },

      //获取评论列表
      requestData(data) {
        let self = this;
        self.$request.comment.getCommenttList(self.currentPage,self.pagesize,data).then((res)=>{
         	if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
             console.log(JSON.stringify(res.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('---产品列表-error--' + JSON.stringify(error));
         });
        },
    //更新评论信息
     updataCommnt(dic){
        let self = this;
          self.$request.comment.updateComment(dic).then((res)=>{
           console.log(JSON.stringify(res.data));
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.requestData();
                // console.log(JSON.stringify(self.type));  
             } else {
               self.$message(res.data.msg);
             }
          }).catch(function(error){
           self.$message('请求异常');
            console.log('-更新文章信息---error--' + JSON.stringify(error));
          });
     }
       
    },
    data() {
      return {
        title:'',
        oid:'',
      	formLabelWidth:120,
      	dialogFormVisible:false,
        total:'',
      	pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        form:{},
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
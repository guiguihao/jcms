<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>促销活动管理</el-breadcrumb-item>
      </el-breadcrumb>

      <div class ="mytable">
        <el-button  type="primary" v-on:click = "addArticle">添加产品</el-button>
      </div>

      <div class ="mytable">
         <template>
           <el-table
             :data="tableData2"
             style="width: 100%"
             >
             <el-table-column
               prop="title"
               label="标题"
               width="250">
             </el-table-column>
             <el-table-column
               prop="type.name"
               label="开始时间"
               format
               width="120">
             </el-table-column>
             <el-table-column
               prop="date"
               width="160"
               label="过期时间">
             </el-table-column>
             <el-table-column
                   width="130"
                   label="状态"
                   >
                   <template slot-scope="scope">
                     <el-button v-if="scope.row.status == 1" type="text" size="small" style='color: #67C23A'>活动进行中...</el-button>
                     <el-button v-if="scope.row.status == 2" type="text" size="small" style='color: #E6A23C'>已过期</el-button>
                     <el-button v-if="scope.row.status == 0" type="text" size="small" style='color: #F56C6C' >未开始</el-button>
                   </template>
              </el-table-column>
              <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.row)">编辑</el-button>
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
        <el-form :model="form">
          <el-form-item label="活动名称" :label-width="formLabelWidth">
            <el-input v-model="form.title" auto-complete="off" style="width: 300px;"></el-input>
          </el-form-item>
          <el-form-item label="活动描述" :label-width="formLabelWidth">
            <el-input v-model="form.describe" auto-complete="off"  style="width: 300px;"></el-input>
          </el-form-item>
          <el-form-item label="开始时间"  :label-width="formLabelWidth">
            <el-date-picker
                 v-model="form.startdate"
                 type="datetime"
                 placeholder="选择日期时间">
               </el-date-picker>
          </el-form-item>
          <el-form-item label="结束时间" :label-width="formLabelWidth">
            <el-date-picker
                 v-model="form.enddate"
                 type="datetime"
                 placeholder="选择日期时间">
               </el-date-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
</template>

<script>
  export default {
    watch:{
     
    },
    created(){
     
      this.requestData();

    },
    methods: {
   
    addArticle(){
      this.title = '添加活动';
      this.dialogFormVisible = true;
    },
    submit(){
      console.log(this.starttime);
      this.addProductSale(this.form);
    },
      edit(data){
        this.title = '编辑活动';
        this.form = data;
        this.dialogFormVisible = true;
      },
      del(data){
         let dic = {_id:data._id,del:1,};
         this.updataUser(dic);
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
 

      //获取活动列表
      requestData(data) {
        let self = this;
        self.$request.productSale.getProductListSale(self.currentPage,self.pagesize,data).then((res)=>{
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
         });
        },

        //更新活动信息
        updataUser(dic){
           let self = this;
             self.$request.productSale.updateProductSale(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {
                   self.requestData();
                   // console.log(JSON.stringify(self.type));  
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
             });
        },
         //添加活动信息
        addProductSale(dic){
           let self = this;
             self.$request.productSale.addProductSale(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {
                   self.requestData();
                   // console.log(JSON.stringify(self.type));  
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
             });
        }
    },
    data() {
      return {
        endtime:'',
        starttime:'',
        title:'',
        status:-1,
        formLabelWidth:'120',
        dialogFormVisible:false,
        total:'',
        pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        form:{},
        rules: {
          name: [
            { required: true, message: '请输入类别名称', trigger: 'blur' },
            { min: 2, max: 16, message: '长度在 2 到 16 个字符', trigger: 'blur' }
          ],
          
          integral: [
            { required: true, message: '请输入积分', trigger: 'blur' },
            { type: 'number', message: '必须为数字值'}
          ],
        }
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
<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>促销活动管理</el-breadcrumb-item>
      </el-breadcrumb>

      <div class ="mytable">
        <el-button  type="primary" v-on:click = "addArticle">添加活动</el-button>
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
               prop="startdate"
               label="开始时间"
               format
               width="160">
             </el-table-column>
             <el-table-column
               prop="enddate"
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
                   width="280"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.$index)">编辑</el-button>
                     <el-button type="primary" size="small" v-on:click="editSale(scope.row)">管理活动产品</el-button>
                     <el-button type="danger" size="small" v-on:click="del(scope.row)">删除</el-button>
                   </template>
              </el-table-column>
           </el-table>
         </template>
      </div>

      <!-- 分页 -->
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


      <!-- 添加编辑活动 -->
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


      <!-- 管理活动产品 -->
       <el-dialog title='管理活动产品' :visible.sync="dialogFormVisible1">
         <el-button  type="primary" v-on:click = "addSaleProduct">添加产品</el-button>
         <el-table
             :data="saleProductForm.products"
             style="width: 100%; margin-top: 50px;"
             >
             <el-table-column
               label="标题"
               width="250">
               <template slot-scope="scope">
                   <img :src=scope.row.oimgs[0] width="50" height="50"  style="float: left;">
                   <el-button type="text">{{scope.row.title }}</el-button>
               </template>
             </el-table-column>
             <el-table-column
               prop="price"
               label="原价"
               width="160">
             </el-table-column>
             <el-table-column
               prop="salePrice"
               width="160"
               label="活动价">
             </el-table-column>
              <el-table-column
                   width="280"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit1(scope.row)">设置活动价格</el-button>
                     <el-button type="danger" size="small" v-on:click="del1(scope.row)">删除</el-button>
                   </template>
              </el-table-column>
           </el-table>
      </el-dialog>


     <!-- 修改促销价格 -->
      <el-dialog :title=title :visible.sync="dialogFormVisible3">
        <el-form :model="form">
          <el-form-item label="产品名称" :label-width="formLabelWidth">
            <el-input v-model="form.title" auto-complete="off" :disabled="true" style="width: 300px;"></el-input>
          </el-form-item>
          <el-form-item label="产品原价" :label-width="formLabelWidth">
            <el-input v-model="form.price" auto-complete="off"  :disabled="true" style="width: 300px;"></el-input>
          </el-form-item>
          <el-form-item label="促销价格" >
                <el-input  v-model.number="form.salePrice" style="width: 220px;"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible3 = false">取 消</el-button>
          <el-button type="primary" @click="submitSale">确 定</el-button>
        </div>
      </el-dialog>


     <!-- 选择参与活动的产品 -->
      <el-dialog title='选择参与活动的产品' :visible.sync="dialogFormVisible2">

         <el-table
             ref="multipleTable"
             :data="products"
             style="width: 100%; "
             @selection-change="handleSelectionChange">
             >
             <el-table-column
               label="标题"
               width="250">
               <template slot-scope="scope">
                   <img :src=scope.row.oimgs[0] width="50" height="50" style="float: left;">
                   <el-button type="text">{{scope.row.title }}</el-button>
               </template>
             </el-table-column>
             <el-table-column
               prop="price"
               label="原价"
               format
               width="160">
             </el-table-column>
             <el-table-column
                   width="130"
                   label="状态"
                   >
                   <template slot-scope="scope">
                     <el-button v-if="scope.row.status == 9" type="text" size="small" style='color: #F56C6C'>已参加活动,选择无效...</el-button>
                     <el-button v-if="scope.row.status != 9" type="text" size="small" style='color: #67C23A' >可参加</el-button>
                   </template>
              </el-table-column>
              <el-table-column
                    type="selection"
                    width="55">
                  </el-table-column>
           </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible2 = false">取 消</el-button>
          <el-button type="primary" @click="submitProducts">确 定</el-button>
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
     
    submitSale(){
         
        if (this.saleProductForm.products) {
           this.saleProductForm.products.forEach(row => {
              if (row._id === this.form._id) {
                row.salePrice =  this.form.salePrice;
                row = this.form;
              }
          });
        }
        let params = {
          _id:this.saleProductForm._id,
          products:this.saleProductForm.products,
        }
        let newDic = JSON.parse(JSON.stringify(this.saleProductForm.products));
        this.saleProductForm.products = newDic;
        this.updataUser(params);
    },
    submitProducts(){

        for(let i in this.multipleSelection){
              let dic = this.multipleSelection[i];
               for (let key in dic) {
                 if (key === 'appkey' || key === 'author' || key === 'buycount' || key === 'collectcount' || key === 'costprice' || key === 'date' || key === 'describe' || key === 'describe_html' || key === 'overview' || key === 'recommend' || key === 'reserved_1' || key === 'reserved_2' || key === 'reserved_3' || key === 'reserved_4' || key === 'type') {
                      console.log(key);
                      delete dic[key];
                 }
              }
              if (9 != dic.status) {
                 dic.salePrice = 0;
                 this.saleProductForm.products.push(dic);    
              }
         }
        let params = {
          _id:this.saleProductForm._id,
          products:this.saleProductForm.products,
        }
        this.updataUser(params);
    },
    toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
     handleSelectionChange(val) {
        this.multipleSelection = val;
      },
    addSaleProduct(){
       this.dialogFormVisible2 = true;
       this.requestProduct();
    },

    addArticle(){
      this.form = {};
      this.title = '添加活动';
      this.dialogFormVisible = true;
      this.tag = 0;
    },
    submit(){
      console.log(this.starttime);
      if (this.tag === 0) {
         this.addProductSale(this.form);
      }
      if (this.tag === 1) {
         this.updataUser(this.form);
      }
     
    },
    edit1(data){
        console.log(data);
        this.title = '设置促销价格';
        this.form = data
        this.dialogFormVisible3 = true;
        this.tag = 1;
        
      },
      del1(data){
         if (this.saleProductForm.products) {
            for (let i in this.saleProductForm.products){
               if (this.saleProductForm.products[i]._id === data._id ) {
                    this.saleProductForm.products.shift(i,0);
               }
            }
        }
        let params = {
          _id:this.saleProductForm._id,
          products:this.saleProductForm.products,
        }
        console.log(params);
        this.updataUser(params);
      },
      edit(index){
         console.log(index);
        this.title = '编辑活动';
        this.form = this.tableData1[index];
        this.dialogFormVisible = true;
        this.tag = 1;
        
      },
      editSale(data){
        this.dialogFormVisible1 = true;
        this.saleProductForm = data;
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
 
     //获取产品列表
      requestProduct(data) {
        let self = this;
        self.$request.product.getProductList(self.currentPage,self.pagesize,data).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
              self.products = res.data.data.data;
              self.producttotal = res.data.data.count;
              
              self.products.forEach(row => {

                 for (let k in self.tableData2) {
                       let saledic = this.tableData2[k];
                       for(let i in saledic.products){
                          let dic = saledic.products[i];
                          if (row._id === dic._id) {
                            row.status = 9; //已参加活动
                          }
                       }
                 }
               
          });
             console.log(JSON.stringify(res.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
          self.$message('请求异常');
           console.log('---产品列表-error--' + JSON.stringify(error));
         });
        },


      //获取活动列表
      requestData(data) {
        let self = this;
        self.$request.productSale.getProductListSale(self.currentPage,self.pagesize,data).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = JSON.parse(JSON.stringify(res.data.data.data));
              self.tableData1 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
              for (let i in self.tableData2) {
                 let dic = self.tableData2[i];
                 dic.startdate = self.$orther.utcToLocalTime(dic.startdate);
                 dic.enddate = self.$orther.utcToLocalTime(dic.enddate);
                
              }
               console.log(JSON.stringify(self.tableData1));  
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
                   this.dialogFormVisible3 = false;
                   this.dialogFormVisible2 = false;
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
        multipleSelection:[],
        products:[],
        producttotal:0,
        tag:0,
        endtime:'',
        starttime:'',
        title:'',
        status:-1,
        formLabelWidth:'120',
        dialogFormVisible:false,
        dialogFormVisible1:false,
        dialogFormVisible2:false,
        dialogFormVisible3:false,
        total:'',
        pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        tableData1: [],
        form:{},
        saleProductForm:{},
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
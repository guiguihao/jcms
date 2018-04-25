<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>促销活动管理</el-breadcrumb-item>
      </el-breadcrumb>

      <div class ="mytable">
        <el-button  type="primary" v-on:click = "addArticle">生成优惠码</el-button>
      </div>

      <div class ="mytable">
         <template>
           <el-table
             :data="tableData2"
             >
             <el-table-column
               prop="code"
               label="优惠码"
               width="250">
             </el-table-column>
              <el-table-column
               prop="usedcount"
               label="优惠幅度\价格"
               format
               width="160">
                <template slot-scope="scope">
                    <el-button v-if="scope.row.salerange > 0" type="text" size="small" >优惠幅度:{{scope.row.salerange}}</el-button>
                    <el-button v-if="scope.row.saleprice > 0" type="text" size="small" >优惠价格:{{scope.row.saleprice}}</el-button>
                    </template>
             </el-table-column>
             <el-table-column
               prop="count"
               label="发行数量"
               format
               width="160">
             </el-table-column>
             <el-table-column
               prop="usedcount"
               label="已使用数量"
               format
               width="160">
             </el-table-column>
             
             <el-table-column
               prop="validdate"
               width="160"
               label="过期时间">
             </el-table-column>
             <el-table-column
                   width="130"
                   label="状态"
                   >
                   <template slot-scope="scope">
                     <el-button v-if="scope.row.status == 1" type="text" size="small" style='color: #67C23A'>正常使用中...</el-button>
                     <el-button v-if="scope.row.status == 0" type="text" size="small" style='color: #E6A23C'>已过期</el-button>
                   </template>
              </el-table-column>
              <el-table-column
                   width="280"
                   label="操作"
                   >
                   <template slot-scope="scope">
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
       <el-dialog title='生成优惠码' :visible.sync="dialogFormVisible">
        <el-form ref="form" :model="form" label-width="80px" >
          <el-form-item label="优惠幅度" >
            <el-input v-model.number="form.salerange" auto-complete="off" style="width: 50px;"></el-input>%  (例:填入的值是80, 使用优惠码后订单价格为:原订单价格*80%)
          </el-form-item>
          <el-form-item label="优惠价格">
            <el-input v-model.number="form.saleprice" auto-complete="off" style="width: 50px;"></el-input>元   (与优惠幅度不可重复填写,如果两者都填,优惠价格优先)
          </el-form-item>
          <el-form-item label="总量" >
            <el-input v-model.number="form.count" auto-complete="off"  style="width: 160px;"></el-input>
          </el-form-item>
          <el-form-item label="有效日期" >
            <el-date-picker
                 v-model="form.validdate"
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
                   <img :src=scope.row.imgs[0] width="50" height="50"  style="float: left;">
                   <el-button type="text">{{scope.row.title }}</el-button>
               </template>
             </el-table-column>
              <el-table-column
                   width="280"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="danger" size="small" v-on:click="del1(scope.row)">删除</el-button>
                   </template>
              </el-table-column>
           </el-table>
      </el-dialog>

     <!-- 选择参与活动的产品 -->
      <el-dialog title='选择参与的产品' :visible.sync="dialogFormVisible2">

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
                   <img :src=scope.row.imgs[0] width="50" height="50" style="float: left;">
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
                     <el-button v-if="scope.row.status == 9" type="text" size="small" style='color: #F56C6C'>已参加优惠,选择无效...</el-button>
                     <el-button v-if="scope.row.status != 9" type="text" size="small" style='color: #67C23A' >可参加</el-button>
                   </template>
              </el-table-column>
              <el-table-column
                    type="selection"
                    width="55">
                  </el-table-column>
           </el-table>

        <!-- 分页 -->
        <div class="mypage">
            <el-pagination
              @size-change="phandleSizeChange"
              @current-change="phandleCurrentChange"
              :current-page="pcurrentPage"
              :page-sizes="[20, 40, 60, 100]"
              :page-size=pagesize
              layout="total, sizes, prev, pager, next, jumper"
              :total=total>
            </el-pagination>
        </div>
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

        let mtList = [];
        for(let i in this.multipleSelection){
              let dic = this.multipleSelection[i];
              let newDic = {
                _id:dic._id,
                title:dic.title,
                imgs:dic.imgs
              }
              mtList.push(newDic);
         }
        let params = {
          _id:this.saleProductForm._id,
          products:mtList,
        }
        this.addProduct(params);

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
         this.addRequestProductSaleCode(this.form);
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
       
      let params = {
        _id:this.saleProductForm._id,
        productId:data._id,
      }
      console.log(params);
      this.delProduct(params);
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
    phandleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.requestProduct = val;
    },
    phandleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
      this.requestProduct();
    },
     //获取产品列表
      requestProduct(data) {
        let self = this;
        self.$request.product.getProductList(self.pcurrentPage,self.pagesize,data).then((res)=>{
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
        self.$request.ProductSaleCode.RequestProductSaleCodeList(self.currentPage,self.pagesize,data).then((res)=>{
           console.log(JSON.stringify(res.data));  
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
             self.$request.ProductSaleCode.updateRequestProductSaleCode(dic).then((res)=>{
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
         //添加参与活动产品
        addProduct(dic){
           let self = this;
             self.$request.ProductSaleCode.addProduct(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {
                   self.requestData();
                   this.dialogFormVisible3 = false;
                   this.dialogFormVisible2 = false;
                   for (let i in dic.products) {
                     let newDic = dic.products[i];
                     console.log("===========")
                     console.log(newDic)
                     this.saleProductForm.products.push(newDic);
                   }
                   
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
             });
        },
         //删除参与活动产品
        delProduct(dic){
           let self = this;
             self.$request.ProductSaleCode.delProduct(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {

                   self.requestData();
                   this.dialogFormVisible3 = false;
                   this.dialogFormVisible2 = false;
                   // console.log(JSON.stringify(self.type));  
                   for (let i =0; i<this.saleProductForm.products.length;i++) {
                       let newdic = this.saleProductForm.products[i];
                      
                       // console.log(newdic)
                       if (newdic._id===dic.productId) {
                          this.saleProductForm.products.splice(i,1);
                       }
                   }
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
             });
        },
         //添加优化码信息
        addRequestProductSaleCode(dic){
           let self = this;
             self.$request.ProductSaleCode.addRequestProductSaleCode(dic).then((res)=>{
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
        pcurrentPage:1,
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
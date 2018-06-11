<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>订单管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	     
	        <el-button v-on:click = "status = 0">待付款</el-button>
	        <el-button v-on:click = "status = 1">待发货</el-button>
	        <el-button v-on:click = "status = 2">已发货</el-button>
	        <el-button v-on:click = "status = 3">已完成</el-button>
	        <el-button v-on:click = "status = 4">已关闭</el-button>
	        <el-button type="primary" v-on:click="requestData()">显示全部</el-button>
	    </div>

	     <div class ="mytable" style="margin-top: 10px">
	       
	        <el-button v-on:click = "refundstatus = 1">处理申请退款</el-button>
	        <el-button v-on:click = "refundstatus = 2">同意退款</el-button>
	        <el-button v-on:click = "refundstatus = 3">拒绝退款</el-button>
	        <el-button v-on:click = "refundstatus = 4">已完成退款</el-button>
	        <el-button v-on:click = "refundstatus = 5">关闭退款</el-button>
	    </div>

	     <div class ="mytable" style="margin-top: 10px">
	       
	       <el-input v-model="orderCode" placeholder="请输入订单编号" style="width: 360px;"></el-input>
	       <el-input v-model="username" placeholder="请输入用户名" style="width: 160px;" ></el-input>
	       <el-input v-model="userphone" placeholder="请输入手机号码" style="width: 160px; "></el-input>
	       <el-button type="primary" icon="el-icon-search" v-on:click="query">搜索</el-button>
	    </div>

	    <div class ="mytable" v-for="item in tableData2">
	       <template > 
	         <el-card class="box-card">
	           <div slot="header" class="clearfix">
	             <span>订单编号:{{item._id}}</span>
	             <span  style="margin-left: 50px">下单日期:{{item.date}}</span>
	             <span style="margin-left: 50px">购买用户:{{item.user.name}}</span>
	             <el-button  style="margin-left: 50px" type="warning" v-if = "item.status == 0" v-on:click = "orderStatus(item)">待付款</el-button>
	             <el-button  style="margin-left: 50px" type="danger" v-if = "item.status == 1" v-on:click = "orderStatus(item)">发货</el-button>
	             <el-button  style="margin-left: 50px" type="primary" v-if = "item.status == 2" v-on:click = "orderStatus(item)">已发货</el-button>
	             <el-button  style="margin-left: 50px" type="success" v-if = "item.status == 3" v-on:click = "orderStatus(item)">交易完成</el-button>
	             <el-button  style="margin-left: 50px" type="info" v-if = "item.status == 4" v-on:click = "orderStatus(item)">交易已关闭</el-button>
	           </div>
               	         <el-table
               	           :data=item.product
               	           style="width: 100%"
               	           :show-header = "false"
               	           >
               	           <el-table-column
               	              prop="_id"
               	             label="订单编号"
               	             width="380">
               	               <template slot-scope="scope" >
                                 <div style=" display: flex;flex-direction: row ">
                                     <img :src=scope.row.lstimgs[0] width="50" height="50">
                                     {{scope.row.title }}
                                 </div>
                                </template>
               	           </el-table-column>
               	           <el-table-column
               	             label="价格"
               	             width="100">
               	              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266">专柜价 :    {{scope.row.price }}</el-button>
                                 </template>
               	           </el-table-column>
               	           <el-table-column
               	             label="促销价"
               	             width="100">
               	              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266" v-if = "scope.row.saleprice>0">活动价 :    {{scope.row.saleprice }}</el-button>

                                 </template>
               	           </el-table-column>

                             <el-table-column
                             label="优惠码"
                             width="100">
                              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266" v-if = "scope.row.saleprice>0">优惠码 :    {{scope.row.saleCode }}</el-button>
                                   
                                 </template>
                           </el-table-column>


               	           <el-table-column
               	             label="颜色"
               	             width="100">
               	              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266" v-if = "scope.row.price.length>0">颜色 :    {{scope.row.colour }}</el-button>
                                 </template>
               	           </el-table-column>
               	           <el-table-column
               	             prop="price"
               	             label="尺寸"
               	             width="100">
               	              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266" v-if = "scope.row.price.length>0">尺寸 :    {{scope.row.size }}</el-button>
                                 </template>
               	           </el-table-column>
               	           <el-table-column
               	             label="购买数量"
               	             width="100">
               	              <template slot-scope="scope">
                                      <el-button type="text"  style="color: #606266" v-if = "scope.row.count>0">购买数量 :    {{scope.row.count }}</el-button>
                                 </template>
               	           </el-table-column>
               	         </el-table>

               	       <div class="bottom">

               	          <el-button v-if="item.refund.status === 1" type="text" style=" float: right; margin-top: 3px; margin-left: 20px; color: #F56C6C" @click="refundInfo(item)">
                              退款申请中
               	          </el-button>
               	           <el-button v-if="item.refund.status === 2" type="text" style=" float: right; margin-top: 3px; margin-left: 20px; color: #F56C6C" @click="refundInfo(item)">
                              同意退款,等待买家退回货物
               	          </el-button>
               	           <el-button v-if="item.refund.status === 3" type="text" style=" float: right; margin-top: 3px; margin-left: 20px; color: #F56C6C" @click="refundInfo(item)">
                              拒绝退款
               	          </el-button>
               	          <el-button v-if="item.refund.status === 4" type="text" style=" float: right; margin-top: 3px; margin-left: 20px; color: #F56C6C" @click="refundInfo(item)">
                              退款完成
               	          </el-button>
               	          <el-button v-if="item.refund.status === 5" type="text" style=" float: right; margin-top: 3px; margin-left: 20px; color: #F56C6C" @click="refundInfo(item)">
                              退款取消
               	          </el-button>
               	          <el-button type="text" style=" float: right; margin-top: 3px;margin-left: 20px" v-if = "item.status > 1 && item.status!=4" @click="expressinfo(item)">物流信息</el-button>  
               	          <el-button type="text" style=" float: right; margin-top: 3px; margin-left: 20px" @click="receiveinfo(item)">收件信息</el-button>     
               	          <span style=" float: right; margin-right: 50px">实际支付:   {{item.price}}  元</span>    
               	       </div>
	         </el-card>
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


        <!-- 等待买家付款 -->
	    <el-dialog
	      title="等待买家付款"
	      :visible.sync="dialogFormVisible0"
	      >
	      <el-form :model="form" :label-width="formLabelWidth" label-position="left">
	          <el-form-item label="实际支付价格" >
	            <el-input v-model.number="form.price" auto-complete="off" style="width: 120px"></el-input>
	            <el-button type="danger" plain  @click="updateOrder('updatePrice')">修改</el-button>
	          </el-form-item>

	          <el-button plain  type="danger"   @click="updateOrder('clodesOrder')">关闭订单</el-button>
	         
	      </el-form>
	      <span slot="footer" class="dialog-footer">
	        <el-button type="primary" @click="dialogFormVisible0 = false">关闭窗口</el-button>
	      </span>
	    </el-dialog>




       <!-- 发货 -->
      <el-dialog title="发货" :visible.sync="dialogFormVisible1">
        <el-form :model="expressform">
          <el-form-item label="快递名称" :label-width="formLabelWidth">
            <el-select v-model="expressform.name" placeholder="请选择活动物流">
                  <el-option label="顺丰快递" value="顺丰快递"></el-option>
                  <el-option label="申通快递" value="申通快递"></el-option>
                  <el-option label="圆通快递" value="圆通快递"></el-option>
                  <el-option label="中通快递" value="中通快递"></el-option>
                  <el-option label="韵达快递" value="韵达快递"></el-option>
                  <el-option label="天天快递" value="天天快递"></el-option>
                  <el-option label="邮政-平邮" value="邮政-平邮"></el-option>
                  <el-option label="邮政-EMS" value="邮政-EMS"></el-option>
             </el-select>
          </el-form-item>
          <el-form-item label="快递单号" :label-width="formLabelWidth">
            <el-input v-model="expressform.code" auto-complete="off" style="width: 300px;"></el-input>
          </el-form-item>
         
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible1 = false">取 消</el-button>
          <el-button type="primary" @click="updateOrder('express')">确 定</el-button>
        </div>
      </el-dialog>



      <!-- 修改订单状态 -->
      <el-dialog title="修改订单状态" :visible.sync="dialogFormVisible2">
        <el-form :model="form">
             <el-button plain  type="danger"   @click="updateOrder('OrderDone')">交易完成</el-button>
        </el-form>
        <div slot="footer" class="dialog-footer">
           <el-button type="primary" @click="dialogFormVisible2 = false">关闭窗口</el-button>
        </div>
      </el-dialog>


       <!-- 修改收货地址 -->
      <el-dialog title="收件信息" :visible.sync="dialogFormVisible3">
        <el-form :model="form"  label-width="80px">
            <el-form-item label="收件姓名:" >
              <el-input v-model="form.name" auto-complete="off"  style="width: 300px;"></el-input>
            </el-form-item>
            <el-form-item label="收件电话" >
              <el-input v-model="form.phone" auto-complete="off"  ></el-input>
            </el-form-item>
            <el-form-item label="收件地址" >
                  <el-input  v-model="form.address" style="width: 220px;"></el-input>
            </el-form-item>
             <el-form-item label="邮编"  >
                  <el-input  type="textarea" v-model="form.code" style="width: 400px;"></el-input>
            </el-form-item>
            <el-form-item label="备注"  >
                  <el-input  type="textarea" v-model="form.remake" style="width: 400px;"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
           <el-button @click="dialogFormVisible3 = false">取 消</el-button>
          <el-button type="primary" @click="submitReceiveinfo">确 定</el-button>
        </div>
      </el-dialog>

       <!-- 退款信息 -->
      <el-dialog title="退款信息" :visible.sync="dialogFormVisible4">
        <el-form :model="refundInfoform"  label-width="80px">
             <el-form-item label="退款状态:">
                  <el-button type="text"  v-if="refundInfoform.status === 1" >退款申请中</el-button>
                  <el-button type="text"  v-if="refundInfoform.status === 2" >已同意退款</el-button>
                  <el-button type="text"  v-if="refundInfoform.status === 3" >已拒绝退款</el-button>
                  <el-button type="text"  v-if="refundInfoform.status === 4" >完成退款</el-button>
             </el-form-item>
             <el-form-item label="退款操作:">
                  <el-button plain  type="danger" v-if="refundInfoform.status === 1 || refundInfoform.status === 2 || refundInfoform.status === 3"   @click="updateOrder('OrderApprove')">同意退款</el-button>
                  <el-button plain  type="danger" v-if="refundInfoform.status === 1 || refundInfoform.status === 2 || refundInfoform.status === 3"   @click="updateOrder('OrderDisapprove')">拒绝退款</el-button>
                   <el-button plain  type="danger" v-if="refundInfoform.status === 2"  @click="updateOrder('OrderDidapprove')">完成退款</el-button>
             </el-form-item>
            <el-form-item label="退款产品" >
              <el-table
               	           :data=refundInfoform.products
               	           style="width: 100%"
               	           :show-header = "false"
               	           >
               	           <el-table-column
               	              prop="_id"
               	             label="订单编号"
               	             width="380">
               	               <template slot-scope="scope">
                                      <img :src=scope.row.imgs[0] width="50" height="50"  style="float: left; margin-right: 15px">
                                     <el-button type="text" style="color: #606266">{{scope.row.title }}</el-button>
                                 </template>
               	           </el-table-column>
               	           <el-table-column
               	             label="数量"
               	             width="150">
               	               <template slot-scope="scope">
                                     <el-button type="text" style="color: #606266">退款数量:{{scope.row.price }}</el-button>
                                 </template>
               	           </el-table-column>
               	          
               	</el-table>

            </el-form-item>
            <el-form-item label="退款金额" >
              <el-input v-model="refundInfoform.price" auto-complete="off"  style="width: 80px;"></el-input>
            </el-form-item>
            <el-form-item label="物流名称" >
                  <el-input  v-model="refundInfoform.express.name" style="width: 220px;"></el-input>
            </el-form-item>
            <el-form-item label="物流单号" >
                  <el-input  v-model="refundInfoform.express.code" style="width: 220px;"></el-input>
            </el-form-item>
            <el-form-item label="留言详情" >
                  <div  v-for="item in refundInfoform.remake">
                      <el-tag type="danger">{{item.user}}  :  {{item.msg}}</el-tag>
                  </div>
            </el-form-item>
            <el-form-item label="说明"  >
                  <el-input  type="textarea" v-model="refundInfoform.nextremake" style="width: 400px;"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
           <el-button @click="dialogFormVisible4 = false">取 消</el-button>
          <el-button type="primary" @click="submitrefundInfo">确 定</el-button>
        </div>
      </el-dialog>

    </div>
</template>

<script>
  export default {
  	watch:{
  		status: function (val) {
  		      let params = {
            status:val,
          }
          this.requestData(params);
  		},
  		refundstatus: function (val) {
  		 let params = {
            'refund.status':val,
          }
          console.log(params);
          this.requestData(params);
  		},
  		orderCode: function (val) {
  		      let params = {
             _id:val,
          }
          this.requestData(params);
  		},
  		username: function (val) {
  		      let params = {
             name:val,
          }
          this.requestUserData(params);
  		},
  		userphone: function (val) {
  		      let params = {
             phone:val,
          }
          this.requestUserData(params);
  		},
  		
  	},
  	created(){

      this.requestData();

  	},
    methods: {

      query(){
        
      
      },
      orderStatus(data){
         
         this.form = JSON.parse(JSON.stringify(data));
         console.log(this.form);
 
      	// 待付款状态
      	if (data.status === 0) {
          this.dialogFormVisible0=true;
          
      	}   

      	// 待发货状态
      	if (data.status === 1) {
          this.dialogFormVisible1=true;
          this.expressform = JSON.parse(JSON.stringify(this.form.express));
      	}

      	// 已发货
      	if (data.status === 2) {
          this.dialogFormVisible2=true;
      	}

      },
       
       updateOrder(data){
       	  
       	  let params = {
             _id:this.form._id,
       	  }
       	  if (data === 'updatePrice') {
              params.price = this.form.price;
       	  }
       	  if (data === 'clodesOrder') {
              params.status = 4;
       	  }
       	  if (data === 'express') {
              params.status = 2;
              params.express=this.expressform;
       	  }
       	  if (data === 'OrderDone') {
              params.status = 3;
       	  }
       	   if (data === 'OrderApprove') {
       	   	  this.refundInfoform.status = 2;
       	   	  params._id=this.refundInfoform._id,
              params.refund = this.refundInfoform;
       	  }
       	  if (data === 'OrderDisapprove') {
       	  	 this.refundInfoform.status = 3;
       	  	 params._id=this.refundInfoform._id,
              params.refund = this.refundInfoform;
              
       	  }
         if (data === 'OrderDidapprove') {
       	  	 this.refundInfoform.status = 4;
       	  	 params._id=this.refundInfoform._id,
              params.refund = this.refundInfoform;
              
       	  }

       	  this.updataUser(params);
          
       },
      receiveinfo(data){
        this.form = JSON.parse(JSON.stringify(data.receiveinfo));
        this.form._id = data._id;
        this.dialogFormVisible3 = true;
       

       },
       submitReceiveinfo(){
       		let params = {
       	      _id:this.form._id,
              receiveinfo:{},
       		  }
       		 for (let k in this.form){
       	     params.receiveinfo[k] = this.form[k];
       	   }
       	    this.updataUser(params);
       },
       expressinfo(data){

            this.expressform = JSON.parse(JSON.stringify(data.express));
            this.expressform._id = data._id;
            this.dialogFormVisible1 = true;
       },
       refundInfo(data){
        this.refundInfoform = JSON.parse(JSON.stringify(data.refund));
        this.refundInfoform._id = data._id;
        this.dialogFormVisible4 = true;   
       },
       submitrefundInfo(){
       			let params = {
       		      _id:this.refundInfoform._id,
       	          refund:{
                     remake:{},
       	          },
       			  }
       			 for (let k in this.refundInfoform){
       			 	if (k != 'remake') {
       		            params.refund[k] = this.refundInfoform[k];
       			 	}
       		   }
       		    let userData = localStorage.getItem('userData');
				let user = JSON.parse(userData);
				let name = user.name;
       		    params.refund.remake.msg = this.refundInfoform.nextremake,
       		    params.refund.remake.user = name,
       		    this.updataUser(params);
       },
      getSummaries(param) {
        const { columns, data } = param;
        const sums = [];

        columns.forEach((column, index) => {
          if (index === 0) {
            sums[index] = '总价';
            return;
          }
          const values = data.map(item => Number(item[column.property]));
          if (!values.every(value => isNaN(value)) && index === 1) {
            sums[index] = values.reduce((prev, curr) => {
              const value = Number(curr);
              if (!isNaN(value)) {
              	      	console.log('======dddddddddddddddddddddddd' + prev);
                return prev + curr;
              } else {
                return prev;
              }
            }, 0);
            console.log('======aaaaaaaaaaaaaa' + JSON.stringify(param));
            console.log('========================');
            sums[index] += ' 元';
          } else {
            sums[index] = 'N/A';
          }
        });

        return sums;
      },


	  addArticle(){
	  	this.$router.push('/admin/Article/ArticleEdit/0');
	  },
      edit(data){
      	this.$router.push('/admin/Article/ArticleEdit/' + data._id);
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
 

     //获取用户列表
      requestUserData(data) {
        let self = this;
        self.$request.user.getUserList(self.currentPage,self.pagesize,data).then((res)=>{
        	console.log(JSON.stringify(res)); 
         	if(res && res.data && res.data.code && res.data.code == 1) {
         		if (res.data.data.data.length>0) {
         			let _id = {user:res.data.data.data[0]._id};
         			this.requestData(_id);
         		}else{
         			self.tableData2 = [];
         		}
             
              
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('----error--' + JSON.stringify(error));
         });
        },


      //获取订单列表
      requestData(data) {
        let self = this;
        self.$request.order.getOrderList(self.currentPage,self.pagesize,data).then((res)=>{
         	if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
              self.dialogFormVisible0 = false;
              self.dialogFormVisible1 = false;
              self.dialogFormVisible2 = false;
              self.dialogFormVisible3 = false;
              self.dialogFormVisible4 = false;
             console.log(JSON.stringify(res.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
         	 console.log('----error--' + JSON.stringify(error));
         });
        },

        //更新订单信息
        updataUser(dic){
        	 let self = this;
             self.$request.order.updateOrder(dic).then((res)=>{
             	console.log(JSON.stringify(res.data));
             	  if(res && res.data && res.data.code && res.data.code == 1) {
             	     self.requestData();
             	      self.$message('修改成功');
             	     // console.log(JSON.stringify(self.type));  
             	  } else {
             	    self.$message(res.data.msg);
             	  }
             }).catch(function(error){
             	self.$message('请求异常');
             	 console.log('----error--' + JSON.stringify(error));
             });
        }
    },
    data() {
      return {
      	refundInfoform:{
           express:{
           	name:'',
           	code:'',
           }
      	},
      	expressform:{},
      	dialogFormVisible0:false,
      	dialogFormVisible1:false,
      	dialogFormVisible2:false,
      	dialogFormVisible3:false,
      	dialogFormVisible4:false,
        status:-1,
        refundstatus:-1,
        orderCode:'',
        username:'',
        userphone:'',
      	formLabelWidth:"120",
      	dialogFormVisible:false,
      	userType:'',
        total:'',
        type:'',
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
    .bottom{
    	height: 30px;
    	line-height: 48px;
    }
	.mytable{

        margin-top: 40px;
        width: 960px;
     
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
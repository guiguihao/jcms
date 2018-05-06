<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>资源管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
         <el-button plain v-on:click = "pf = 'zip'">.zip</el-button>
         <el-button plain v-on:click = "pf = 'doc'">.doc</el-button>
         <el-button plain v-on:click = "pf = 'docx'">.docx</el-button>
         <el-button plain v-on:click = "pf = 'rar'">.rar</el-button>
         <el-button plain v-on:click = "pf = 'txt'">.txt</el-button>
         <el-button type="primary" icon="el-icon-plus" v-on:click="addImgClick">添加资源</el-button>
	    </div>

	    <div class ="mytable">
	       <template>
	         <el-table
	           :data="tableData2"
	           >
	           <el-table-column
               prop="name"
	             label="title"
	             width="360">
                
	           </el-table-column>
              <el-table-column
                   width="100"
                   prop="size"
                   label="size"
                   >
                  
              </el-table-column>
	           <el-table-column
	             prop="pf"
	             label="格式"
	             width="80">
	           </el-table-column>
            
              <el-table-column
               prop="ourl"
               label="url"
               width="360">
             </el-table-column>
	           <el-table-column
	             prop="date"
	             width="160"
	             label="更新日期">
	           </el-table-column>
             <el-table-column
                   width="220"
                   label="操作"
                   >
                   <template slot-scope="scope">
                     <el-button type="primary" size="small" v-on:click="edit(scope.row)" >替换</el-button>
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

         <el-dialog :title=title :visible.sync="dialogFormVisible"  width="500px" style="padding:100px;">
           <el-upload
             class="upload-demo"
             drag
             action="/imgapi/upload/saveImg.php"
             :data="imgdata"
             :on-success="handleAvatarSuccess1"
             :before-upload="beforeAvatarUpload"
             multiple>
             <i class="el-icon-upload"></i>
             <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
             <div class="el-upload__tip" slot="tip">图片有缓存,替换成功后需要等待一段时间图片才会更新,或者尝试清除浏览器缓存</div>
           </el-upload>
        </el-dialog>
    </div>


</template>

<script>
  export default {
  	watch:{
  		
      pf: function (val) {

          let data = {
            pf:val,
          }
          this.requestData(data);
      },

  		
  	},
  	created(){

     this.initdata();
  	},
    methods: {

      initdata(){

        let data = {
              pf:{'$nin':['png','jpg','gif','jpeg']},
            }
        this.requestData(data);
      },

       handleAvatarSuccess1(res, file) {
        if (res.code === 1) {
           this.initdata();
           this.$message.success(res.msg);
        }else{
              this.$message.error(res.msg);
        }
      },

      beforeAvatarUpload(file) {
        
        return true;
      },
   
       handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
        this.pagesize = val;
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
        this.currentPage = val;
        this.initdata();
      },
   
     addImgClick(){
        this.imgdata.operation = 'add';
        this.addOrEdit = false;
        this.title='添加';
        this.dialogFormVisible = true;
      },

      edit(data){
        this.imgdata.path =  data.url;
        this.imgdata.operation = 'update';
        this.addOrEdit = false;
        this.title='替换';
        this.dialogFormVisible = true;

      },
      del(data){
        this.imgdata.path =  data.url;
        this.imgdata.operation = 'del';
        this.updataImg2(this.imgdata);
      },


      //获取图片列表
      requestData(data) {
        let self = this;
        self.$request.img2.getImg2tList(self.currentPage,self.pagesize,data).then((res)=>{
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
    //更新图片信息
     updataImg2(dic){
        let self = this;
          self.$request.img2.updateImg2(dic).then((res)=>{
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.$message.success(res.data.msg);
                self.initdata();
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
        imgdata:{token:this.$token.getToken(),operation:'update',path:''}, 
        title:'',
        pf:'',
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
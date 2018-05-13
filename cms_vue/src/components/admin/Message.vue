<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>留言管理</el-breadcrumb-item>
	    </el-breadcrumb>

	    <div class ="mytable">
	       <el-input v-model="oid" placeholder="请输入产品或文章_id" style="width: 350px; "></el-input>
         <el-button type="primary" icon="el-icon-search" v-on:click="query">搜索</el-button>
	       <el-button icon="el-icon-plus" v-on:click="addClick()">添加</el-button>
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
               prop="answer"
               label="回复"
               width="360">
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
                     <el-button type="primary" size="small" v-on:click="answerClick(scope.row)" >回复</el-button>
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
              <el-input v-model="form.oid" :disabled="!isAdd" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
             <el-form-item label="内容">
              <el-input v-model="form.content" type="textarea" :autosize="{ minRows: 2, maxRows: 6}" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
           <!--  <el-form-item label="图片">
              <el-upload
                class="upload-demo"
                action="/imgapi/upload/saveImg.php"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :on-success = "handlerSuccess"
                :file-list="fileList2"
                :before-upload ="handlerBeforeUpload"
                :data="imgdata"
                list-type="picture-card">
                 <i class="el-icon-plus"></i>
                <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
              </el-upload>
            </el-form-item>
            <el-form-item label="评分" >
              <el-input v-model.number="form.level" auto-complete="off" style="width: 80px;"></el-input>
            </el-form-item> -->
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitForm('form')">确 定</el-button>
          </div>
        </el-dialog>



        <el-dialog title='回复' :visible.sync="dialogFormVisible1">
          <el-form :model="form"  ref="form" label-width="80px">
             <el-form-item label="内容">
              <el-input v-model="form.content" :disabled=true  type="textarea" :autosize="{ minRows: 2, maxRows: 6}" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
            <el-form-item label="回复">
              <el-input v-model="form.answer" type="textarea" :autosize="{ minRows: 2, maxRows: 6}" auto-complete="off" style="width: 300px;"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible1 = false">取 消</el-button>
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

      handlerBeforeUpload(file){
         this.imgdata.operation = 'add';
      },
      handleRemove(file, fileList) {
           let self = this;
           let url = file.url;
           let xUrls = url.split("/");
           if (xUrls.length>0) {
            url = xUrls[xUrls.length-1];
           }
           let fileName = url;
           let fns = fileName.split(".");
           if (fns.length>0) {
            let hz = fns[fns.length-1];
            let url = hz + '/' + fileName;
            console.log(url)
            this.imgdata.path =  url;
            this.imgdata.operation = 'del';
            this.updataImg2(this.imgdata);
           }
           
           
      },
      handlerSuccess(response, file, fileList){
        if (response.code === 1) {
          this.$message.success(response.msg);
          this.fileList2.push({'url':response.data.url});
        }else{
          this.$message.error(response.msg);
        }
      },
      handlePreview(file) {
           console.log('11111111');
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
        this.form.imgs = [];
        for (let index in this.fileList2) {
           let url = this.fileList2[index].url;
           this.form.imgs.push(url);
        }
        if (this.isAdd) {
          this.addCommnt(this.form);
        }else{
          this.updataCommnt(this.form);

        }
      },
      edit(data){
        this.fileList2=[];
        this.form = data;
        this.addOrEdit = false;
        this.title='编辑评论';
        this.dialogFormVisible = true;
        for (let key in data.imgs) {
           let imgUrl =  data.imgs[key];
           this.fileList2.push({'url':imgUrl});
        }
        this.isAdd = false;

      },
      del(data){
        let obj = JSON.parse(JSON.stringify(data));
        obj.del = 1;
        this.updataCommnt(obj);
      },
      answerClick(data){
         this.dialogFormVisible1=true;
         this.form = data;
         this.isAdd = false;
      },
      addClick(){
         this.dialogFormVisible = true;
         this.fileList2=[];
         this.form = {type:0};
         this.title='添加评论';
         this.isAdd = true;

      },
      addcomment(){
        let self = this;
        self.$request.comment.addComment(data).then((res)=>{
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
      updataImg2(dic){
          let self = this;
          self.$request.img2.updateImg2(dic).then((res)=>{
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.$message.success(res.data.msg);
                let cpfileList2 = this.fileList2;
                for (let index in cpfileList2) {
                    let imgUrl = cpfileList2[index].url;
                    if (imgUrl.indexOf(dic.path)>0) {
                       this.fileList2.pop({'url':imgUrl});
                       break;
                    }
                }
                // console.log(JSON.stringify(self.type));  
             } else {
               self.$message.error(res.data.msg);
             }
          }).catch(function(error){
            self.$message.error('请求异常');
            console.log('-更新文章信息---error--' + JSON.stringify(error));
          });
      },
      //获取评论列表
      requestData(data) {
        let self = this;
        if (data) {
          data.type = 0;
        }else{
          data = {type:0}
        };
        self.$request.comment.getCommenttList(self.currentPage,self.pagesize,data).then((res)=>{
         	if(res && res.data && res.data.code && res.data.code == 1) {
              self.tableData2 = res.data.data.data;
              self.total = res.data.data.count;
              self.dialogFormVisible = false;
              self.dialogFormVisible1 = false;
             console.log(JSON.stringify(res.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
         	self.$message('请求异常');
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
          });
     },

     //添加评论信息
     addCommnt(dic){
          let self = this;
          let userData = localStorage.getItem('userData');
          let user = JSON.parse(userData);
          dic.userId = user._id;
          self.$request.comment.addComment(dic).then((res)=>{
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
        imgdata:{token:this.$token.getToken(),operation:'add',path:''}, 
        fileList2:[],
        title:'',
        oid:'',
      	formLabelWidth:120,
      	dialogFormVisible:false,
        dialogFormVisible1:false,
        total:'',
      	pagesize:20,
        currentPage:1,
        total:0,
        tableData2: [],
        form:{},
        isAdd:true,
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
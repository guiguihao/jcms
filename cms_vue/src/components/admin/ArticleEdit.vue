<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>文章列表</el-breadcrumb-item>
	          <el-breadcrumb-item>{{nav_title}}</el-breadcrumb-item>
	    </el-breadcrumb>
        
        <div class = "myform">
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="title" prop="title">
              <el-input v-model="ruleForm.title"></el-input>
            </el-form-item>
            <el-form-item label="简介">
                <el-input type="textarea" v-model="ruleForm.overview"></el-input>
            </el-form-item>
            <el-form-item label="作者" style="width: 350px;">
              <el-input v-model="author" :disabled="true" ></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="type">
             <el-select v-model="ruleForm.type" placeholder="请选择">
              <el-option
                       v-for="item in type"
                       :key="item.type._id"
                       :label="item.type.name"
                       :value="item.type._id">
                 </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期" style="width: 350px;">
              <el-input v-model="ruleForm.date"  :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="来源">
              <el-radio-group v-model="ruleForm.source">
                <el-radio :label='0'>转发</el-radio>
                <el-radio :label='1'>原创</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="推荐" >
              <el-select v-model="ruleForm.recommend" placeholder="请选择">
              <el-option
                       v-for="item in typeHot"
                       :key="item.type._id"
                       :label="item.type.name"
                       :value="item.type._id">
                 </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="内容" prop="content">
               <div style= "height: 500px; ">
                  <mavon-editor v-model="ruleForm.content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel" :ishljs = "true" @change="$htmlvalue"  placeholder = "开始编写..." style="height: 100%"/>
               </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" v-if = "isadmin == 1 && id != 0 && ruleForm.status == 0" @click="submitForm_SH('ruleForm')">审核</el-button>
              <el-button type="primary" @click="submitForm_BC('ruleForm')">保存</el-button>
              <el-button type="primary" @click="submitForm_FB('ruleForm')">发布</el-button>
              <!-- <el-button @click="resetForm('ruleForm')">重置</el-button> -->
            </el-form-item>
          </el-form>
        </div> 
    </div>
</template>

<script>
  export default {
  
    data() {
      return {
        author:'',
        id:'',
        region:'',
      	tjvalue:'',
        type:[],
        typeHot:[],
        isadmin:0,
      	ruleForm: {
          title: '',
          overview: '',
          author: '',
          date: '',
          type: '',
          source: 0,
          recommend: '',
          content:'',
          htmlcontent:'',
          status:'',

        },
        rules: {
          title: [
            { required: true, message: '请输入活动名称', trigger: 'blur' },
            { min: 3, max: 65, message: '长度在 3 到 65 个字符', trigger: 'blur' }
          ],
          type: [
            { required: true, message: '请选择类别', trigger: 'change' }
          ],
          date1: [
            { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
          ],
          date2: [
            { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
          ],
          resource: [
            { required: true, message: '请选择活动资源', trigger: 'change' }
          ],
          desc: [
            { required: true, message: '请填写活动形式', trigger: 'blur' }
          ]
        },

      }
    },

     methods: {

       submitForm_SH(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
             this.ruleForm.status = 3;
             if (this.id === '0') {
                this.requestAddData(this.ruleForm);
             }else{
               this.updataUser(this.ruleForm);
             }
            
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
       submitForm_BC(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.ruleForm.status = 2;
             if (this.id === '0') {
                this.requestAddData(this.ruleForm);
             }else{
               this.updataUser(this.ruleForm);
             }
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
       submitForm_FB(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.ruleForm.status = 3;
             if (this.id === '0') {
                this.requestAddData(this.ruleForm);
             }else{
               this.updataUser(this.ruleForm);
             }
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },


      resetForm(formName) {
        this.$refs[formName].resetFields();
      },

      //获取文章类型
      requestUserType(){
         let self = this;
         self.$request.type.getTypeList('article').then((res)=>{
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.type = res.data.data;
               // console.log(JSON.stringify(self.type));  
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('----error--' + JSON.stringify(error));
         });
      },   

      //获取推荐类型
      requestTypeHot(){
         let self = this;
         self.$request.type.getTypeList('article_hot').then((res)=>{
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.typeHot = res.data.data;
               // console.log(JSON.stringify(self.type));  
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('----error--' + JSON.stringify(error));
         });
      },           
       
       //添加文章
       requestAddData(data) {
         let self = this;
         data.author = this.authorID;
         self.$request.article.addArticle(data).then((res)=>{
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.$message('添加文章成功');
                this.$router.push('/admin/Article/ArticleList');
             } else {
               self.$message(res.data.msg);
             }
          }).catch(function(error){
            self.$message('请求异常');
            console.log('----error--' + JSON.stringify(error));
          });
         
       },


       $imgAdd(pos, $file){
          
            // 第一步.将图片上传到服务器.
           let self = this;
           self.$request.img.saveImg($file).then((res)=>{
            console.log('----xxx--' + JSON.stringify(res.data));
               if(res && res.data && res.data.code && res.data.code == 1) {
                  
                  this.$refs.md.$imgAddByUrl(pos,res.data.data.url);
                  this.$refs.md.$img2Url(pos,res.data.data.url);
                  this.$refs.md.$imgUpdateByUrl(pos,res.data.data.url);
                  this.$refs.md.$refs.toolbar_left.$imgDelByFilename(pos);
                  self.$message('图片上传成功');
               } else {
                 self.$message(res.data.msg);
               }
            }).catch(function(error){
              self.$message('请求异常');
              console.log('----error--' + JSON.stringify(error));
            });
        },
        $imgDel(filename){
            // 第一步.将图片上传到服务器.
            console.log('======' + filename);

           // let self = this;
           // self.$request.img.delImg(filename).then((res)=>{
           //     if(res && res.data && res.data.code && res.data.code == 1) {
           //        console.log('----xxx--' + JSON.stringify(res.data));
           //        self.$message('删除成功');
           //     } else {
           //       self.$message(res.data.msg);
           //     }
           //  }).catch(function(error){
           //    self.$message('请求异常');
           //    console.log('----error--' + JSON.stringify(error));
           //  });
        }, 

       $htmlvalue(val,render){
          this.ruleForm.htmlcontent = render;
       },

      getUser(){
         let userData = localStorage.getItem('userData');
         let user = JSON.parse(userData);
         console.log(userData);
         for(let key in user){ 
             if (key === 'superadmin') {
                 this.isadmin = 1;
             }
         }
         this.author = user.name;
         this.authorID= user._id;
      },



      //获取文章列表
      requestData() {
        let self = this;
        if (this.id === '0') {
          return;
        }
        let filter = {
           _id:this.id,
        };
        self.$request.article.getArticleList(1,20,filter).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
              self.ruleForm = res.data.data.data[0];
              self.author = self.ruleForm.author.name;
              self.ruleForm.author = self.ruleForm.author._id;
              self.ruleForm.type = self.ruleForm.type._id;
              // self.total = res.data.data.count;
              // self.dialogFormVisible = false;
             console.log('=======' + JSON.stringify(res.data.data.data));  
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
          self.$message('请求异常');
           console.log('----error--' + JSON.stringify(error));
         });
        },

        //更新文章信息
        updataUser(dic){
           let self = this;
             self.$request.article.updateArticle(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {
                   // self.requestData();
                   // console.log(JSON.stringify(self.type));  
                   self.$message('更新文章成功');
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
               console.log('----error--' + JSON.stringify(error));
             });
        }

    },

    created(){
      this.id = this.$route.params.id;
      if (this.id === '0') {
        this.nav_title = '添加文章';
      }else{
        this.nav_title = '编辑文章';
      }
      this.requestUserType();
      this.requestTypeHot();
      this.getUser();
      this.requestData();

    },
    computed: {
       
    },
    watch:{
       ruleForm:{
            handler(val){
               this.region = val.type;
               console.log(this.region);
            },
            deep:true
        }
    },

  }
</script>


<style >
	.myform{
        margin-top: 40px;
        width: 900px;


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
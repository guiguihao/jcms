<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>产品列表</el-breadcrumb-item>
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
            <el-form-item label="价格" style="width: 220px;">
                <el-input  v-model.number="ruleForm.price"></el-input>
            </el-form-item>
            <el-form-item label="成本价"  style="width: 220px;">
                <el-input v-model.number="ruleForm.costprice"></el-input>
                <el-button type="text">用于计算分销分成</el-button>
            </el-form-item>
            <el-form-item label="作者" style="width: 350px;">
              <el-input v-model="author" :disabled="true" ></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="type">
              <el-cascader
                        :options="type"
                        v-model="articleType"
                        :props="props"
                        :show-all-levels="false" 
                        change-on-select
                       >
              </el-cascader>
            </el-form-item>
            <el-form-item label="日期" style="width: 350px;">
              <el-input v-model="ruleForm.date"  :disabled="true"></el-input>
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
            <el-form-item label="主图" >
               <el-upload
                 class="avatar-uploader"
                 action="/api/app/save/img2"
                 :show-file-list="false"
                 :data="imgdata"
                 :on-success="handleAvatarSuccess1"
                 :before-upload="beforeAvatarUpload">
                 <img v-if="imageUrl1" :src="imageUrl1" class="avatar">
                 <i v-else class="el-icon-plus avatar-uploader-icon"></i>
               </el-upload>
               <el-upload
                 class="avatar-uploader"
                 action="/api/app/save/img2"
                 :show-file-list="false"
                 :data="imgdata"
                 :on-success="handleAvatarSuccess2"
                 :before-upload="beforeAvatarUpload">
                 <img v-if="imageUrl2" :src="imageUrl2" class="avatar">
                 <i v-else class="el-icon-plus avatar-uploader-icon"></i>
               </el-upload>
                <el-upload
                 class="avatar-uploader"
                 action="/api/app/save/img2"
                 :show-file-list="false"
                 :data="imgdata"
                 :on-success="handleAvatarSuccess3"
                 :before-upload="beforeAvatarUpload">
                 <img v-if="imageUrl3" :src="imageUrl3" class="avatar">
                 <i v-else class="el-icon-plus avatar-uploader-icon"></i>
               </el-upload>
                <el-upload
                 class="avatar-uploader"
                 action="/api/app/save/img2"
                 :show-file-list="false"
                 :data="imgdata"
                 :on-success="handleAvatarSuccess4"
                 :before-upload="beforeAvatarUpload">
                 <img v-if="imageUrl4" :src="imageUrl4" class="avatar">
                 <i v-else class="el-icon-plus avatar-uploader-icon"></i>
               </el-upload>
                <el-upload
                 class="avatar-uploader"
                 action="/api/app/save/img2"
                 :show-file-list="false"
                 :data="imgdata"
                 :on-success="handleAvatarSuccess5"
                 :before-upload="beforeAvatarUpload">
                 <img v-if="imageUrl5" :src="imageUrl5" class="avatar">
                 <i v-else class="el-icon-plus avatar-uploader-icon"></i>
               </el-upload>
            </el-form-item>
            <el-form-item label="内容" prop="describe">
               <div style= "height: 500px; ">
                  <mavon-editor v-model="ruleForm.describe" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel" :ishljs = "true" @change="$htmlvalue"  placeholder = "开始编写..." style="height: 100%"/>
               </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" v-if = "isadmin == 1 && id != 0 && ruleForm.status == 0" @click="submitForm_SH('ruleForm')">审核</el-button>
              <el-button type="primary" @click="submitForm_BC('ruleForm')">保存到仓库</el-button>
              <el-button type="primary" @click="submitForm_FB('ruleForm')">立即上架</el-button>
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
        imgdata:{token:this.$token.getToken()}, 
        imageUrl1: '',
        imageUrl2: '',
        imageUrl3: '',
        imageUrl4: '',
        imageUrl5: '',
        author:'',
        id:'',
        region:'',
        tjvalue:'',
        type:[],
        typeHot:[],
        isadmin:0,
        articleType:[],
        ruleForm: {
         imgs:[],

        },
        props: {
          value: 'type',
          label: 'title',
          children: 'children'
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

      handleAvatarSuccess1(res, file) {
        console.log(JSON.stringify(res));
        if (res.code === 1) {
            this.imageUrl1 = URL.createObjectURL(file.raw);
            this.ruleForm.imgs[0] = res.data.url;
        }else{
              this.$message.error(res.msg);
        }
      },
      handleAvatarSuccess2(res, file) {
        console.log(JSON.stringify(res));
        if (res.code === 1) {
            this.imageUrl2 = URL.createObjectURL(file.raw);
            this.ruleForm.imgs[1] = res.data.url;
        }else{
              this.$message.error(res.msg);
        }
      },
      handleAvatarSuccess3(res, file) {
        console.log(JSON.stringify(res));
        if (res.code === 1) {
            this.imageUrl3 = URL.createObjectURL(file.raw);
            this.ruleForm.imgs[2] = res.data.url;
        }else{
              this.$message.error(res.msg);
        }
      },
      handleAvatarSuccess4(res, file) {
        console.log(JSON.stringify(res));
        if (res.code === 1) {
            this.imageUrl4 = URL.createObjectURL(file.raw);
            this.ruleForm.imgs[3] = res.data.url;
        }else{
              this.$message.error(res.msg);
        }
      },
      handleAvatarSuccess5(res, file) {
        console.log(JSON.stringify(res));
        if (res.code === 1) {
            this.imageUrl5 = URL.createObjectURL(file.raw);
            this.ruleForm.imgs[4] = res.data.url;
        }else{
              this.$message.error(res.msg);
        }
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'  || file.type === 'image/gif';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
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

      //获取产品类型
      requestUserType(){
         let self = this;
         self.$request.type.getTypeList('shop').then((res)=>{
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.type = res.data.data;
               // console.log(JSON.stringify(self.type));  
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('--获取产品类型--error--' + JSON.stringify(error));
         });
      },   

      //获取推荐类型
      requestTypeHot(){
         let self = this;
         self.$request.type.getTypeList('shop_hot').then((res)=>{
            if(res && res.data && res.data.code && res.data.code == 1) {
                self.typeHot = res.data.data;
               // console.log(JSON.stringify(self.type));  
            } else {
              self.$message(res.data.msg);
            }
         }).catch(function(error){
          self.$message('请求异常');
           console.log('--获取推荐类型--error--' + JSON.stringify(error));
         });
      },           
       
       //添加产品
       requestAddData(data) {
         let self = this;
         data.author = this.authorID;
         self.$request.product.addProduct(data).then((res)=>{
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.$message('添加产品成功');
                this.$router.push('/admin/Product/ProductList');
             } else {
               self.$message(res.data.msg);
             }
          }).catch(function(error){
            self.$message('请求异常');
            console.log('--添加产品--error--' + JSON.stringify(error));
          });
         
       },


       $imgAdd(pos, $file){
          
            // 第一步.将图片上传到服务器.
           let self = this;
           self.$request.img.saveImg($file).then((res)=>{
            console.log('----xxx--' + JSON.stringify(res.data));
               if(res && res.data && res.data.code && res.data.code == 1) {
                  self.$message('图片上传成功');
                  this.$refs.md.$imgAddByUrl(pos,res.data.data.url);
                  this.$refs.md.$img2Url(pos,res.data.data.url);
                  this.$refs.md.$imgUpdateByUrl(pos,res.data.data.url);
                  this.$refs.md.$refs.toolbar_left.$imgDelByFilename(pos);
               } else {
                 self.$message.error(res.data.msg);
               }
            }).catch(function(error){
              self.$message.error('请求异常');
              console.log('---图片上传到服务器.-error--' + JSON.stringify(error));
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
          this.ruleForm.describe_html = render;
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

      //子节点寻找父节点
      computeParent(id,Original,list,returnList){
        for (let i in list) {
          let type = list[i];
          if (type.type._id === id) {
              returnList.unshift(type.type);
              console.log(returnList);
              if (type.type.parentID.length>1) {
                this.computeParent(type.type.parentID,Original,Original,returnList);
              }
          }else{
            if (type.children) {
              this.computeParent(id,Original,type.children,returnList);
            }
          }
        }
      },

       //寻找节点
      computeNode(id,list){
        for (let i in list) {
          let type = list[i];
          if (type.type._id === id) {
              return type.type;
          }else{
            if (type.children) {
              return this.computeNode(id,type.children);
            }
          }
        }
      },
   
      //获取产品列表
      requestData() {
        let self = this;
        if (this.id === '0') {
          return;
        }
        let filter = {
           _id:this.id,
        };
        self.$request.product.getProductList(1,20,filter).then((res)=>{
          if(res && res.data && res.data.code && res.data.code == 1) {
               console.log('===产品列表====' + JSON.stringify(res.data.data.data));  
              self.ruleForm = res.data.data.data[0];
              if (self.ruleForm.author) {
                  self.author = self.ruleForm.author.name;
                  self.ruleForm.author = self.ruleForm.author._id;
              }
              if (self.ruleForm.recommend) {
                  self.ruleForm.recommend = self.ruleForm.recommend._id;
              }
              if (self.ruleForm.type) {
                let mlist = [];
                let cptype =JSON.parse(JSON.stringify(self.ruleForm.type));
                setTimeout(function(){
                  let selfnode =self.computeNode(cptype._id,self.type);
                  mlist.push(selfnode);
                  console.log('----111111-----' + JSON.stringify(selfnode));
                  self.computeParent(cptype.parentID,self.type,self.type,mlist);
                  console.log('---------');
                  console.log(mlist);
                  self.articleType = mlist;
                },1000);
                self.ruleForm.type = self.ruleForm.type._id;
                
              }
              if(self.ruleForm.imgs){

                setTimeout(function(){
                    self.imageUrl1 = self.ruleForm.imgs[0];
                    self.imageUrl2 = self.ruleForm.imgs[1];
                    self.imageUrl3 = self.ruleForm.imgs[2];
                    self.imageUrl4 = self.ruleForm.imgs[3];
                    self.imageUrl5 = self.ruleForm.imgs[4];
                },1000);
                  
              }
              // self.total = res.data.data.count;
              // self.dialogFormVisible = false;
          } else {
            self.$message(res.data.msg);
          }

         }).catch(function(error){
          self.$message('请求异常');
           console.log('--产品列表--error--' + JSON.stringify(error));
         });
        },

        //更新产品信息
        updataUser(dic){
           let self = this;
             self.$request.product.updateProduct(dic).then((res)=>{
              console.log(JSON.stringify(res.data));
                if(res && res.data && res.data.code && res.data.code == 1) {
                   // self.requestData();
                   // console.log(JSON.stringify(self.type));  
                   self.$message('更新产品成功');
                } else {
                  self.$message(res.data.msg);
                }
             }).catch(function(error){
              self.$message('请求异常');
               console.log('---更新产品信息-error--' + JSON.stringify(error));
             });
        }

    },

    created(){
      this.id = this.$route.params.id;
      if (this.id === '0') {
        this.nav_title = '添加产品';
      }else{
        this.nav_title = '编辑产品';
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
        },
        articleType: function (val) {
          console.log('ddddddddddd' +JSON.stringify(val) );
           if (val.length>0) {
               if ((typeof val[0]) === 'string') {

               }else{
                  this.ruleForm.type = val[val.length-1]._id;
               }
           }
          // console.log(params);
      },
     
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
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    float: left;
    margin-left: 10px
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
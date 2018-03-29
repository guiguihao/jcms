<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>文章列表</el-breadcrumb-item>
	          <el-breadcrumb-item>编辑文章</el-breadcrumb-item>
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
              <el-input v-model="ruleForm.author" ></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="region">
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
              <el-input v-model="ruleForm.date" ></el-input>
            </el-form-item>
            <el-form-item label="来源">
              <el-radio-group v-model="ruleForm.source">
                <el-radio label="转发"></el-radio>
                <el-radio label="原创"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="推荐" >
              <el-radio-group v-model="ruleForm.recommend">
                <el-radio label="级别1"></el-radio>
                <el-radio label="级别2"></el-radio>
                <el-radio label="级别3"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="内容" prop="content">
               <div style= "height: 500px; ">
                  <mavon-editor v-model="ruleForm.content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel" :ishljs = "true" @change="$htmlvalue"  placeholder = "开始编写..." style="height: 100%"/>
               </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">审核</el-button>
              <el-button type="primary" @click="requestAddData(ruleForm)">保存</el-button>
              <el-button type="primary" @click="submitForm('ruleForm')">发布</el-button>
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
      	value:'',
        type:[],
      	ruleForm: {
          title: '',
          overview: '',
          author: '',
          date: '',
          type: '',
          source: 0,
          recommend: [],
          content:'',
          htmlcode:'',
          review:'',
          push:'',

        },
        rules: {
          title: [
            { required: true, message: '请输入活动名称', trigger: 'blur' },
            { min: 3, max: 65, message: '长度在 3 到 65 个字符', trigger: 'blur' }
          ],
          region: [
            { required: true, message: '请选择活动区域', trigger: 'change' }
          ],
          date1: [
            { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
          ],
          date2: [
            { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
          ],
          type: [
            { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }
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

       submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
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
          console.log(JSON.stringify(res.data));
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
       
       //添加文章
       requestAddData(data) {
         let self = this;
         self.$request.article.addArticle(data).then((res)=>{
             if(res && res.data && res.data.code && res.data.code == 1) {
                self.$message('添加文章成功');
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
               if(res && res.data && res.data.code && res.data.code == 1) {
                  self.$message('添加成功');
               } else {
                 self.$message(res.data.msg);
               }
            }).catch(function(error){
              self.$message('请求异常');
              console.log('----error--' + JSON.stringify(error));
            });
        },

       $htmlvalue(val,render){
          this.ruleForm.htmlcode = render;
          // console.log('====' + this.ruleForm.htmlcode);
       }

    },

    created(){

      this.requestUserType();

    },
    watch:{
     
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
<template>
	<div>
		<el-breadcrumb separator-class="el-icon-arrow-right">
	          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
	          <el-breadcrumb-item>文章列表</el-breadcrumb-item>
	          <el-breadcrumb-item>编辑文章</el-breadcrumb-item>
	    </el-breadcrumb>
        
        <div class = "myform">
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="文章title" prop="name">
              <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="作者" prop="name" style="width: 350px;">
              <el-input v-model="ruleForm.name" ></el-input>
            </el-form-item>
            <el-form-item label="类别" prop="region">
              <el-select v-model="ruleForm.region" placeholder="请选择类别">
                <el-option label="类别一" value="shanghai"></el-option>
                <el-option label="类别二" value="beijing"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期" prop="name" style="width: 350px;">
              <el-input v-model="ruleForm.name" ></el-input>
            </el-form-item>
            <el-form-item label="来源" prop="resource">
              <el-radio-group v-model="ruleForm.resource">
                <el-radio label="转发"></el-radio>
                <el-radio label="原创"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="推荐" prop="resource">
              <el-radio-group v-model="ruleForm.resource">
                <el-radio label="级别1"></el-radio>
                <el-radio label="级别2"></el-radio>
                <el-radio label="级别3"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="内容" prop="desc">
               <div style= "height: 500px; ">
                  <mavon-editor v-model="value" placeholder = "开始编写..." style="height: 100%"/>
               </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">审核</el-button>
              <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
              <el-button type="primary" @click="submitForm('ruleForm')">发布</el-button>
              <!-- <el-button @click="resetForm('ruleForm')">重置</el-button> -->
            </el-form-item>
          </el-form>
        </div> 
    </div>
</template>

<script>
  export default {
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
      }
    },
    data() {
      return {
      	value:'',
      	ruleForm: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入活动名称', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
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
        }
      	
      }
    }
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
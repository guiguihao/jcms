<?php
// post form参数 1.token 2.userId  
header("Content-Type: text/html;charset=utf-8"); 
// 指定允许其他域名访问    
header('Access-Control-Allow-Origin:*');    
// 响应类型    
header('Access-Control-Allow-Methods:POST');    
// 响应头设置    
header('Access-Control-Allow-Headers:x-requested-with,content-type,Authorization');    

$httpFix   = 'http://img.weiyunbuy.com';     //图片空间地址
$tokenUrl  = 'http://api.weiyunbuy.com/app/checktoken/' . $_POST["token"];  //获取token
$addImgUrl  = 'http://api.weiyunbuy.com/app/img2/add';  
$updateImgUrl  = 'http://api.weiyunbuy.com/app/img2/del';
$userId = $_POST["userId"];
$operation = $_POST["operation"];
$originalPath = $_POST["path"];
$type = $_POST["type"];
if ($type) {
  # code...
}else{
  $type = "RSC";
}
if ($reserved_1) {
  # code...
}else{
  $reserved_1 = "";
}
if ($reserved_2) {
  # code...
}else{
  $reserved_2 = "";
}
if ($reserved_3) {
  # code...
}else{
  $reserved_3 = "";
}
if ($reserved_4) {
  # code...
}else{
  $reserved_4 = "";
}

$raw_fail  = array('code' => 2, 'msg' => '上传失败'); 
$raw_fail1 = array('code' => 3, 'msg' => '上传失败,不支持此格式或大小超出限制');   
$raw_fail2 = array('code' => 4, 'msg' => '创建文件夹失败'); 
$raw_fail3 = array('code' => 5, 'msg' => '保存文件失败'); 
$raw_fail4 = array('code' => 6, 'msg' => 'token错误'); 
$raw_del_success  = array('code' => 1, 'msg' => '删除成功'); 
$raw_del_fail  = array('code' => 2, 'msg' => '删除失败'); 
 

$res_fail  = json_encode($raw_fail); 
$raw_fail1 = json_encode($raw_fail1); 
$raw_fail2 = json_encode($raw_fail2); 
$raw_fail3 = json_encode($raw_fail3); 
$raw_fail4 = json_encode($raw_fail4); 
$raw_del_success = json_encode($raw_del_success); 
$raw_del_fail = json_encode($raw_del_fail); 

//校验token
$tokenResult = file_get_contents($tokenUrl);  
$jsonToken   = json_decode($tokenResult, true);
if ($jsonToken['code'] != 1) {
      echo $raw_fail4;
      exit;
}

if ($operation == "del") {
   if (unlink ($originalPath)) {
     //提交服务器
     $post_data = array(
       'token' => $_POST["token"],
       'url'   =>  $originalPath,
       'del'   =>  1,
     );
     $addImgResult  = send_post($updateImgUrl, $post_data);
     $json = json_decode($addImgResult, true);
     // echo $addImgResult;
     if ($json['code'] == 1) {
           echo $raw_del_success;
           exit;
     }
      echo $raw_del_fail;
      exit;
   }else{
      echo $raw_del_fail;
      exit;
   }
}

$name = md5(uniqid());
if ((($_FILES["file"]["type"] == "image/gif")
|| ($_FILES["file"]["type"] == "application/octet-stream")
|| ($_FILES["file"]["type"] == "image/jpeg")
|| ($_FILES["file"]["type"] == "image/png")
|| ($_FILES["file"]["type"] == "text/plain")
|| ($_FILES["file"]["type"] == "application/zip")
|| ($_FILES["file"]["type"] == "image/pjpeg"))
  ){
    if ($_FILES["file"]["error"] > 0)
      {
      echo $res_fail;
      exit;
      }
    else
    {
          // echo "Upload: " . $_FILES["file"]["name"] . "<br />";
          // echo "Type: " . $_FILES["file"]["type"] . "<br />";
          // echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
          // echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";
          
          $arr=explode(".", $_FILES["file"]["name"]);  
          $hz=$arr[count($arr)-1]; 
          if (!file_exists($hz))
            {
               if (!mkdir ($hz,0777,1)) {
                  echo $raw_fail2;
                  exit;
               }
            }
          $path = '';
          if ($hz == 'gif' || $hz == 'jpg' || $hz == 'png' || $hz == 'jpeg') {
             $path = $hz . "/" . $name ."." .$hz;
          }else{
              
             $path = $hz . "/" .$_FILES["file"]["name"];
             $name = $_FILES["file"]["name"];
          }
          //如果替换图片
          if ($operation == "update") {
             $path = $originalPath;
          }
          if (move_uploaded_file($_FILES["file"]["tmp_name"],$path)) {
              //提交服务器
              $post_data = array(
                'token' => $_POST["token"],
                'url'   =>   $path,
                'name'   =>  $name,
                'size'  =>  round($_FILES["file"]["size"] / 1024,2) . " Kb",
                'pf'   =>  $hz,
                'type'   =>  $type,
                'userid'   =>  '',
              );
              $addImgResult  = send_post($addImgUrl, $post_data);
              $json = json_decode($addImgResult, true);
              // echo $addImgResult;
              if ($json['code'] != 1) {
                    echo $raw_fail3;
                    exit;
              }
              $raw_success = array('code' => 1, 'msg' => '上传成功', 'data'=>array('hz' => $hz, 'Size' => round($_FILES["file"]["size"] / 1024,2) . " Kb", 'url' =>$httpFix . '/upload/'. $path, 'ourl' => $path));
              $res_success = json_encode($raw_success);  
              echo $res_success;
              exit;
          }else{
            echo $raw_fail3;
            exit;
          }
      }
    }
else
  {
  echo $raw_fail1;
  exit;
  }


/**
 * 发送post请求
 * @param string $url 请求地址
 * @param array $post_data post键值对数据
 * @return string
 */
function send_post($url, $post_data) {
 
  $postdata = http_build_query($post_data);
  $options = array(
    'http' => array(
      'method' => 'POST',
      'header' => 'Content-type:application/x-www-form-urlencoded',
      'content' => $postdata,
      'timeout' => 15 * 60 // 超时时间（单位:s）
    )
  );
  $context = stream_context_create($options);
  $result = file_get_contents($url, false, $context);
 
  return $result;
}
?>
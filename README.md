# ProblemUploader-Hydro
向HydroOJ上传题目的工具 | A tool for uploading questions to HydroOJ

## 用途：

HydroOJ可以通过FPS文件导入题目，但是往往FPS文件中会包含大量测试数据，导致文件过大，从而无法成功上传。

这个工具的作用是：

+ 1.浏览`data/`目录下的所有xml格式的FPS文件

+ 2.在`res/`目录中给每个题目创建一个文件夹，里面包含题目描述`problem.md`和若干组`xx.in` `xx.out`组成的测试数据（如果测试数据不是`数字.in`或`数字.out`）那么会在上传的时候将它重命名
+ 3.将 去掉测试数据的FPS文件 存储在项目根目录 然后尝试向Hydro发送post请求
+ 4.按照题目编号遍历OJ中的所有题目，从response中解析题目名称
+ 5.将题目对应的测试数据post到Hydro

## 配置：

配置`uploader.py`中的`cookies`和`url`



## 注：

`data/`中包含一个来自usaco的样例

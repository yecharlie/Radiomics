负责切割出肺结节图像
=====================
各模块及其接口的说明
--------------------

### 1.simpleITKCheck.py
  检查SimpleITK是否安装成功

### 2.relatedPackagesCheck.py
  检查一些常用包是否安装

### 3.fileReader.py
  def find_images_data(case_path):</br>
  读取一个序列中所有的DICOM文件

  def find_xml_file(case_path):</br>
  返回一个文件夹（序列）里的XML文件

  def print_image_info(image):</br>
  打印一张simpleITK图像的所有信息

  def show_image(image_array_path):</br>
  读取一张已保存的切割好的图像（以npy格式存储），并显示它。前提是已经有Fiji等科学图像查看器，见[SimpleITK Notebooks](http://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/).

### 4.dataGenerator.py

  DNN_INPUT_SIDE_LEN</br>
  切割出的图像（正方形）的边长

  def gen_roi_images(case_path,output_path):</br>
  产生一个序列中切割好的肺结节数据（包括小于3毫米和大于3毫米大小的肺结节），同时可以产生成比例的非肺结节数据（非肺结节：肺结节 = 2 ： 1）。最后将他们保存在Numpy的npy格式文件中。

### 5.dataSetup.py
  def prepare_all_data(raw_data_root,intermedia_data_root):</br>
  从下载好的数据("LIDC-IDRI")产生肺结节图像以及非肺结节图像数据，此时图像按照序列放在不同的文件夹中。

### 6.dataOrganize.py
  def organize_data(train_data_ratio,intermedia_data_root,output_data_root):</br>
  进一步整理数据，将它们按照训练、测试分为两大部分

简单用法
--------------
####  1.调用simpleITKCheck模块以及relatedPackagesCheck模块检查相关的包是否正常安装，否则需要另行安装
####  2.下载好数据("LIDC-IDRI")
####  3.使用dataSetup模块产生图像。
####  4.使用dataOrganize模块整理图像。
最终产生切割好的肺结节图像和非肺结节图像，按1比2比例配置。所有图像按训练和测试两部分分类放置。有几个细节需要注意：一是这里把大小小于3毫米和大于3毫米的肺结节归为一类；
二是非肺结节图像是在原图像中随机找点切割出来的，并不能保证不会把部分肺结节图像切进去，但出现这种情况的概率其实很小。




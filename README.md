# Radiomics
*******************一个切割肺结节数据的小工具**************************

1.肺结节数据来源为公开数据集：
https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI#f89bac21cfe947749d5143843535089e

2.功能
上面的数据集包含1000+患者的肺结节数据，以DICOM文件存储，有CT、DX两种模型。此外，在每个序列（CT/DX）中都有一个XML文件.
在CT序列中的XML文件里存放着这个属于这个序列的肺结节定位信息。我们做的就是利用定位信息找到并切出对应肺结节的图像。

3.使用的工具
3.1语言
PYTHON 3.6.1

3.2处理DICOME文件
SimpleITK 1.0.0

3.3处理XML文件
minidom

参考
【1】simpleITK官网
http://www.simpleitk.org/SimpleITK/help/documentation.html
【2】simeleITK notebookds
http://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/
【3】python下解析xml
http://www.runoob.com/python/python-xml.html
【4】】minidom的一些用法
http://www.cnblogs.com/fnng/p/3581433.html

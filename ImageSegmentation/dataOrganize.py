import os
import numpy as np 

from shutil import copyfile

def organize_data(train_data_ratio,intermedia_data_root,output_data_root):
	
	input_roi_dir = os.path.join(intermedia_data_root,"roi")

	number_of_series = len(os.listdir(input_roi_dir))
	series_indices = np.arange(number_of_series)

	#ransomly chosse train/test data
	np.random.shuffle(series_indices)

	train_series_number = int(number_of_series * train_data_ratio)
	input_plain_dir = os.path.join(intermedia_data_root,"plain")

	#orgainize train data
	print("Copy train-roi-data:")
	output_train_roi_dir = os.path.join(output_data_root,"train","roi")
	copy_to_one_dir(series_indices[0:train_series_number],input_roi_dir,output_train_roi_dir)
	
	print("Copy train-plain-data:")
	output_train_plain_dir = os.path.join(output_data_root,"train","plain")
	copy_to_one_dir(series_indices[0:train_series_number],input_plain_dir,output_train_plain_dir)

	#orginize test_data
	print("Copy test-roi-data:")
	output_test_roi_dir = os.path.join(output_data_root,"test","roi")
	copy_to_one_dir(series_indices[train_series_number:],input_roi_dir,output_test_roi_dir)
	
	print("Copy test-plain-data:")
	output_test_plain_dir = os.path.join(output_data_root,"test","plain")
	copy_to_one_dir(series_indices[train_series_number:],input_plain_dir,output_test_plain_dir)

		
def path_check(path):
	'''Create a new path if not existed
	'''
	if not os.path.exists(path):
		os.makedirs(path)

def copy_to_one_dir(series_indices,src_dir,dst_dir):
	'''Copy all these files in sepicified sub-series directories to one directory.
	
	If path dst_dir not existed, a new path will be created.
	'''
	path_check(dst_dir)

	print("Copy files from ",src_dir,"\n to ",dst_dir)
	print("Related series: ",series_indices)

	series_names = os.listdir(src_dir)
	img_id = 0
	for index in series_indices:
		tmp_series_dir = os.path.join(src_dir,series_names[index])
		
		for filename in os.listdir(tmp_series_dir):
			src_fp = os.path.join(tmp_series_dir,filename)

			#use img_id as the uniform filename and align it to the right
			#with a fill char '0' 
			dst_fp = os.path.join(dst_dir,"{:0>4}".format(img_id)+ ".npy")
			copyfile(src_fp,dst_fp)

			img_id +=1 
'''
intermedia_data_root = "/media/charles/study/Nodules"
output_data_root = "/media/charles/study/Organized_Nodules"

organize_data(0.9,intermedia_data_root,output_data_root)
'''
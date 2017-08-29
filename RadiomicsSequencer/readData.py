import os

import numpy as np 

current_read_roi_number = 0
current_read_plain_number = 0

'''Data root
'''
data_root = None

'''Test data 

Saved as a tuple:(images,labals)
It is requried to call read_data_sets functuib
before user can access to the train and test data.
'''
test_data = None

def read_data_sets(path):
	'''Read data sets.

	It is requried to call this funtion before pne 
	can get any train/test data.
	'''
	global data_root,test_data

	#record the path for next_batch function
	data_root = path

	#store a list of (image,label) tuples
	#here we do not extract two lists --one for images,anather for labels -- directly
	#because we need a sequence with a random permutation. 
	tmp_test_data = []

	#get roi images
	test_roi_dir = os.path.join(path,"test","roi")
	for filename in os.listdir(test_roi_dir):
		fp = os.path.join(test_roi_dir,filename)
		#print("Test_roi:",fp)
		#images are saved as Numpy 's npy file
		img_array = np.load(fp)

		#label '1' stands for region of interest (roi) image
		tmp_test_data.append((img_array,np.float32(1)))

	#the same for getting plain images
	test_plain_dir = os.path.join(path,"test","plain")
	for filename in os.listdir(test_plain_dir):
		fp = os.path.join(test_plain_dir,filename)
		#print("Test_plain:",fp)
		img_array = np.load(fp)

		#label '0' stands for plain image
		tmp_test_data.append((img_array,np.float32(0)))

	#shuffle the sequence with a random permutation
	np.random.shuffle(tmp_test_data)

	#Convert the data type from int32 to float32 (to meet tensorflow 's requirement')
	imgs = [ np.reshape(data[0],-1).astype("float32") for data in tmp_test_data]
	lbls = [ data[1] for data in tmp_test_data]
	lbls = np.reshape(lbls,(-1,1))

	test_data = imgs,lbls


def next_batch(batch_num):
	global current_read_roi_number,current_read_plain_number,data_root

	tmp_train_data = []

	#In every call, number of roi images is half of plain images
	#batch_roi_num = batch_num / 3
	batch_roi_num = np.random.randint(1,batch_num)

	#get roi images
	train_roi_dir = os.path.join(data_root,"train","roi")
	roi_arr_filenames = os.listdir(train_roi_dir)

	#Note that once a traverse upon train images data is over
	#it will restart anather traverse from the begining. 
	batch_roi_filenames = []
	if current_read_roi_number + batch_roi_num <= len(roi_arr_filenames):
		batch_roi_filenames += roi_arr_filenames[current_read_roi_number:current_read_roi_number + batch_roi_num]
	else:
		batch_roi_filenames += roi_arr_filenames[current_read_roi_number:] + roi_arr_filenames[:batch_roi_num - len(roi_arr_filenames) + current_read_roi_number ]

	for filename in batch_roi_filenames:
		fp = os.path.join(train_roi_dir,filename)

		#print("Train_roi:",fp)

		#read a image from Numpy npy file
		img_array = np.load(fp)
		tmp_train_data.append((img_array,np.float32(1)))

	#move the traverse pointer forward
	current_read_roi_number = (current_read_roi_number + batch_roi_num) % len(roi_arr_filenames)

	#the same for getting plain images
	batch_plain_num = batch_num - batch_roi_num

	train_plain_dir = os.path.join(data_root,"train","plain")
	plain_arr_filenames = os.listdir(train_plain_dir)
	batch_plain_filenames = []
	if current_read_plain_number + batch_plain_num <= len(plain_arr_filenames):
		batch_plain_filenames += plain_arr_filenames[current_read_plain_number:current_read_plain_number + batch_plain_num]
	else:
		batch_plain_filenames += plain_arr_filenames[current_read_plain_number:] + plain_arr_filenames[:batch_plain_num - len(plain_arr_filenames) + current_read_plain_number ]

	for filename in batch_plain_filenames:
		fp = os.path.join(train_plain_dir,filename)
		#print("Train_plain:",fp)
		img_array = np.load(fp)
		tmp_train_data.append((img_array,np.float32(0)))

	current_read_plain_number = (current_read_plain_number + batch_plain_num) % len(plain_arr_filenames)

	#a random re-permutation
	np.random.shuffle(tmp_train_data)

	#Convert the data type from int32 to float32 (to meet tensorflow 's requirement')
	imgs = [np.reshape(data[0],-1).astype("float32") for data in tmp_train_data]
	
	lbls = [data[1] for data in tmp_train_data]
	lbls = np.reshape(lbls,(batch_num,1))

	#print("First data in this batch",imgs[0],lbls[0])
	return imgs,lbls

'''
path = "/media/charles/study/Organized_Nodules"
print("Test_data")
read_data_sets(path)

for i in range(3):
	print("Next batch",i)
	next_batch(12)
'''
import tensorflow as tf 

import readData
readData.read_data_sets("/media/charles/study/Organized_Nodules")

def weight_variable(shape):
	initial = tf.truncated_normal(shape,stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1,shape = shape)
	return tf.Variable(initial)

def conv2d(x,W):		
	return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding = 'VALID')

#Note that it has a  ifferent pooling scheme in the original LeNet-5 
def max_pool_2x2(x):
	return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
x = tf.placeholder(tf.float32,shape=[None,34 * 34])
y = tf.placeholder(tf.float32,shape=[None,1])

#We temmporarily assume that the input CTs has 1 charnel
W_conv1 = weight_variable([3,3,1,32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x,[-1,34,34,1])

h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1) + b_conv1)# 32 *32 bitmap
h_pool1 = max_pool_2x2(h_conv1)#16 * 16 bitmap

#Note that in LeNet-5 different filter use di fferent conbination of the last level filters
#while we have NOT adopted this scheme
W_conv2 = weight_variable([5,5,32,32])
b_conv2 = bias_variable([32])

h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2) + b_conv2)#12 * 12 bitmap
h_pool2 = max_pool_2x2(h_conv2)# 6 * 6 bitmap

W_conv3 = weight_variable([3,3,32,64])
b_conv3 = bias_variable([64])

#4 * 4 bitmap
h_conv3 = tf.nn.relu(conv2d(h_pool2,W_conv3) + b_conv3)

W_fc1 = weight_variable([4 * 4 * 64,64])
b_fc1 = bias_variable([64])

h_conv3_flat = tf.reshape(h_conv3,[-1,4*4*64])

h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat,W_fc1) + b_fc1)

#dropout omitted

W_fc2 = weight_variable([64,1])
b_fc2 = bias_variable([1])

y_conv = tf.nn.relu(tf.matmul(h_fc1,W_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(#Note: implicit line joining
	tf.nn.softmax_cross_entropy_with_logits(labels = y,logits = y_conv))
train_step = tf.train.AdamOptimizer(0.00001).minimize(cross_entropy)
correct_prediction = tf.equal(y_conv,y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

print("Lung Nodule Classification Experiment")

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	for i in range(2000):
		batch = readData.next_batch(36)
		if i % 100 == 0:

			train_accuracy = accuracy.eval(feed_dict = {
				x : batch[0],y : batch[1]})
			print("step %d, training_accuracy %g" % (i,train_accuracy))
		train_step.run(feed_dict = {x : batch[0],y : batch[1]})

	print("test accuracy %g" % accuracy.eval(feed_dict={
		x : readData.test_data[0],y : readData.test_data[1]}))
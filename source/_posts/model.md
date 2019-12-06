---
layout: poster
title: 卷积神经网络预测危险车辆模型
date: 2018-06-07 21:24:52
tags: [CNN,TensorFlow,python]
---
<!-- TOC -->

- [卷积神经网络预测危险车辆](#卷积神经网络预测危险车辆)
        - [卷积神经网络模型概述](#卷积神经网络模型概述)
        - [图片预处理](#图片预处理)
        - [模型结构](#模型结构)
        - [模型优化与调参](#模型优化与调参)
        - [GUI图形界面](#gui图形界面)

<!-- /TOC -->

## 卷积神经网络预测危险车辆

#### 卷积神经网络模型概述

在各种深度神经网络结构中，卷积神经网络是应用最广泛的一种，它由LeCun在1989年提出。卷积神经网络在早期被成功应用于手写字符图像识别。2012年更深层次的AlexNet网络取得成功，此后卷积神经网络蓬勃发展，被广泛用于各个领域，在很多问题上都取得了当前最好的性能。卷积神经网络通过卷积和池化操作自动学习图像在各个层次上的特征，这符合我们理解图像的常识。人在认知图像时是分层抽象的，首先理解的是颜色和亮度，然后是边缘、角点、直线等局部细节特征，接下来是纹理、几何形状等更复杂的信息和结构，最后形成整个物体的概念。
<!--more-->
#### 图片预处理

   从网上下载的图片质量参差不齐，对其进行如下操作：

   1. 去掉格式受损图片。图片下载到本地时，存在一些格式受损的图片，将其从训练集中删除。

   2. 统一图片格式。下载图片格式类型有jpeg,png,jpg等，编写一个自动脚本，将其全部规整为Jpg格式

3. 去掉文字干扰信息。许多网络车辆图片存在如下文字广告信息，对其进行裁剪处理，减少对模型训练的干扰性
4. 图片size统一为 100 *100。
5. 从所有图集随机选取若干张图片，作为验证集，剩下的作为数据集。每次训练时，将数据集随机打乱顺序，按设定的比例 $\alpha$ 划分为训练集与测试集

#### 模型结构

![png.png](https://i.loli.net/2018/06/07/5b192c73183b7.png)

一共 11层结构：初始输入（100×100×3)$\to$ 第1卷积层(100×100×32) $\to$ 第1 最大池化层(50×50×32-) $\to$ 第2卷积层(50×50×64) $\to$ 第2最大池化层(25×25×64) $\to$ 第3卷积层(25×25×128)$\to$  第3最大池化层(12×12×128) $\to$ 第4卷积层(12×12×128)$\to$  第4最大池化层(6×6×128)$\to$ 全连接层(1024) $\to$ 全连接层(512) $\to$ 全连接层(2)

*  **模型尺寸分析**：卷积层全都采用了补0，所以经过卷积层长和宽不变，只有深度加深。池化层全都没有补0，所以经过池化层长和宽均减小，深度不变。

* **模型尺寸变化**：100×100×3->100×100×32->50×50×32->50×50×64->25×25×64->25×25×128->12×12×128->12×12×128->6×6×128
![m_1.png](https://i.loli.net/2018/06/07/5b192faf41d5b.png)
![m_2.png](https://i.loli.net/2018/06/07/5b192fe28a928.png)
![pred_acc.png](https://i.loli.net/2018/06/07/5b192d641c7d6.png)​

在测试集上准确率为83%，其实是过拟合的。一是因为图片数据太少，训练集中图片共计才1400张。将其进行镜像翻转扩充，也才2800张，这点训练量应该是不够的。二是直接可以从Loss损失中看出来，训练集中准确度无限逼近100%，loss值也接近于零。而测试集上的损失在 `n_batch = 0~30`上是减少的，后来却不断增加至50左右，然后不断波动。

去问了沈复民老师，和我想的差不多，说是这应该一个开放性分类问题，而不是一个二分类问题。不仅应该检测出是否为危险类别，还应检测危险车辆的具体类别，比如油罐车，厢型危险品运输车等。所以在代码中，其实是用来`Softmax`分类器的，在多分类时，不需要修改`Sigmoid`l了。然而，因为指导老师貌似不太懂深度学习，数据集也不太够，对危险车辆分类之后，发现每一类可用的图片数据实在是比较少，有些甚至没有超过百张，而且时间确实也不够进行折腾，所以就直接套了个二分类输出上去。

#### 模型优化与调参

这一段没什么好说的，按部就班的调整一下混弄过去就是了。不过发现，对数据进行扩充效果还不错。如本文的对图像进行镜像翻转操作，最后预测率上升了6%。不过可能 只是数据量增大使得过拟合程度更高了，因为Loss值图像还是不太好看。

```python
from skimage import io,transform
import glob
import os
import tensorflow as tf
import numpy as np
import time
import pickle

#数据集地址
#path='D:/Data/File/flower_photos/flower_photos/'
path='D:/Code/Python/Anaconda/dataset/'
#模型保存地址
model_path='D:/Code/Python/Anaconda/dataset/Model/'
log_dir='D:/Code/Python/Anaconda/model/'
#将所有的图片resize成100*100
w=100
h=100
c=3

cate=[path+x for x in os.listdir(path) if os.path.isdir(path+x)]
print(cate)
imgs=[]
labels=[]
for idx,folder in enumerate(cate):
     print(idx)
     print(folder)




#读取图片
def read_img(path):
    cate=[path+x for x in os.listdir(path) if os.path.isdir(path+x)]
    #print(cate)
    imgs=[]
    labels=[]
    for idx,folder in enumerate(cate):
      #  print(idx)
       # print(folder)
        for im in glob.glob(folder+'/*.jpg'):
            #print('reading the images:%s'%(im))
            try:
                img=io.imread(im)
                img=transform.resize(img,(w,h))
                if(img.size != 30000):
                    print('the %s is not 30000'% im)
                imgs.append(img)
                labels.append(idx) 
            except:
                print('somerrp %s'%(im))
    return np.asarray(imgs,np.float32),np.asarray(labels,np.int32)


#把数据暂存至本地
data,label=read_img(path)
output = open('data.pkl', 'wb')
Slabel=open('label.pkl','wb')
# Pickle dictionary using protocol 0.
pickle.dump(data, output,-1)

# Pickle the list using the highest protocol available. 保存数据至本地，减少加载时间贼好用
pickle.dump(label,Slabel ,-1)
Slabel.close()
output.close()

#加载数据
data=pickle.load(open('data.pkl','rb'))
label=pickle.load(open('label.pkl','rb'))


#-----------------构建网络----------------------
#占位符
x=tf.placeholder(tf.float32,shape=[None,w,h,c],name='x')
y_=tf.placeholder(tf.int32,shape=[None,],name='y_')


def inference(input_tensor, train, regularizer):
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable("weight",[5,5,3,32],initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable("bias", [32], initializer=tf.constant_initializer(0.0))
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))
        variable_summaries(conv1_weights)
        #variable_summaries(conv1_biases)

    with tf.name_scope("layer2-pool1"):
        pool1 = tf.nn.max_pool(relu1, ksize = [1,2,2,1],strides=[1,2,2,1],padding="VALID")

    with tf.variable_scope("layer3-conv2"):
        conv2_weights = tf.get_variable("weight",[5,5,32,64],initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable("bias", [64], initializer=tf.constant_initializer(0.0))
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biases))
       # variable_summaries(conv2)

    with tf.name_scope("layer4-pool2"):
        pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    with tf.variable_scope("layer5-conv3"):
        conv3_weights = tf.get_variable("weight",[3,3,64,128],initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv3_biases = tf.get_variable("bias", [128], initializer=tf.constant_initializer(0.0))
        conv3 = tf.nn.conv2d(pool2, conv3_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu3 = tf.nn.relu(tf.nn.bias_add(conv3, conv3_biases))

    with tf.name_scope("layer6-pool3"):
        pool3 = tf.nn.max_pool(relu3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    with tf.variable_scope("layer7-conv4"):
        conv4_weights = tf.get_variable("weight",[3,3,128,128],initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv4_biases = tf.get_variable("bias", [128], initializer=tf.constant_initializer(0.0))
        conv4 = tf.nn.conv2d(pool3, conv4_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu4 = tf.nn.relu(tf.nn.bias_add(conv4, conv4_biases))

    with tf.name_scope("layer8-pool4"):
        pool4 = tf.nn.max_pool(relu4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')
        nodes = 6*6*128
        reshaped = tf.reshape(pool4,[-1,nodes])

    with tf.variable_scope('layer9-fc1'):
        fc1_weights = tf.get_variable("weight", [nodes, 1024],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None: tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1_biases = tf.get_variable("bias", [1024], initializer=tf.constant_initializer(0.1))

        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weights) + fc1_biases)
        if train: fc1 = tf.nn.dropout(fc1, 0.5)

    with tf.variable_scope('layer10-fc2'):
        fc2_weights = tf.get_variable("weight", [1024, 512],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None: tf.add_to_collection('losses', regularizer(fc2_weights))
        fc2_biases = tf.get_variable("bias", [512], initializer=tf.constant_initializer(0.1))

        fc2 = tf.nn.relu(tf.matmul(fc1, fc2_weights) + fc2_biases)
        if train: fc2 = tf.nn.dropout(fc2, 0.5)

    with tf.variable_scope('layer11-fc3'):
        fc3_weights = tf.get_variable("weight", [512, 2],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None: tf.add_to_collection('losses', regularizer(fc3_weights))
        fc3_biases = tf.get_variable("bias", [2], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc2, fc3_weights) + fc3_biases
        #logit=tf.nn.softmax(logit)
        variable_summaries(tf.nn.softmax(logit))
    return logit

#---------------------------网络结束---------------------------
regularizer = tf.contrib.layers.l2_regularizer(0.0001)
logits = inference(x,False,regularizer)

#(小处理)将logits乘以1赋值给logits_eval，定义name，方便在后续调用模型时通过tensor名字调用输出tensor
b = tf.constant(value=1,dtype=tf.float32)
logits_eval = tf.multiply(logits,b,name='logits_eval') 

loss=tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=y_)
train_op=tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)
correct_prediction = tf.equal(tf.cast(tf.argmax(logits,1),tf.int32), y_)    
acc= tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#tf.summary.scalar('loss',loss)
tf.summary.scalar('acc',acc)
merged=tf.summary.merge_all()

#定义一个函数，按批次取数据
def minibatches(inputs=None, targets=None, batch_size=None, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batch_size]
        else:
            excerpt = slice(start_idx, start_idx + batch_size)
        yield inputs[excerpt], targets[excerpt]

#训练和测试数据，可将n_epoch设置更大一些

n_epoch=18      
train_lost=np.zeros(n_epoch)
test_lost=np.zeros(n_epoch)
test_acc=np.zeros(n_epoch)
batch_size=64
#saver=tf.train.Saver()
sess=tf.Session()  
#train_writer = tf.summary.FileWriter(log_dir + '/train', sess.graph)
#test_writer = tf.summary.FileWriter(log_dir + '/test')
sess.run(tf.global_variables_initializer())
# 写到指定的磁盘路径中
i=0
for epoch in range(n_epoch):
    start_time = time.time()
    #training
    train_loss, train_acc, n_batch = 0, 0, 0
    for x_train_a, y_train_a in minibatches(x_train, y_train, batch_size, shuffle=True):
        #i+=1
        summary,op,err,ac=sess.run([merged,train_op,loss,acc], feed_dict={x: x_train_a, y_: y_train_a})
        train_loss += err; train_acc += ac; n_batch += 1
        #print(summary)
 #       train_writer.add_summary(summary, i)  
    
    print("   train loss: %f" % (np.sum(train_loss)/ n_batch))
    print("   train acc: %f" % (np.sum(train_acc)/ n_batch))
    train_lost[i]=np.sum(train_loss)/ n_batch
    
   
    #validation
    val_loss, val_acc, n_batch = 0, 0, 0
    for x_val_a, y_val_a in minibatches(x_val, y_val, batch_size, shuffle=False):
        err,ac = sess.run([loss,acc], feed_dict={x: x_val_a, y_: y_val_a})
        val_loss += err; val_acc += ac; n_batch += 1 
    print("   validation loss: %f" % (np.sum(val_loss)/ n_batch))
    print("   validation acc: %f" % (np.sum(val_acc)/ n_batch))
    test_acc[i]=np.sum(val_acc)/ n_batch
    test_lost[i]=(np.sum(val_loss)/ n_batch)
    i+=1
#saver.save(sess,model_path)

#train_writer.close()
#test_writer.close()

sess.close()



#加载模型数据，调用模型
from skimage import io,transform
import tensorflow as tf
import numpy as np
#logdir='D:/Data/File/flower_photos/flower_photos/'
logdir='D:/Code/Python/Anaconda/dataset/'
suffix='.jpg'
path1 = logdir+"badCar/A_2"+suffix
path2 = logdir+"badCar/A_276"+suffix
path3 = logdir+"badCar/A_286"+suffix
path4 = logdir+"goodCar/B_32"+suffix
path5 = logdir+"goodCar/B_91"+suffix

#flower_dict = {0:'dasiy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}
car_dict={0:'dangerous',1:'norm car'}
w=100
h=100
c=3

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    data2 = read_one_image(path2)
    data3 = read_one_image(path3)
    data4 = read_one_image(path4)
    data5 = read_one_image(path5)
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
    data.append(data5)

    saver = tf.train.import_meta_graph('D:/Code/Python/Anaconda/dataset/Model/.meta')
    saver.restore(sess,tf.train.latest_checkpoint('D:/Code/Python/Anaconda/dataset/Model/'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)
    classification_result=tf.nn.softmax(classification_result)
    classification_result=classification_result.eval()
    #打印出预测矩阵
    #with np.set_printoptions(precision=5):
    print(classification_result)

    
    
    #打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    #根据索引通过字典对应花的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        print("第",i+1,"辆车预测:"+car_dict[output[i]])

```

#### GUI图形界面

最后老师还提了个要求，写个图形界面处理，然后就花了一晚上入门了`PyQt`,其实还是没有入门的，，就是写了一个很简单框框界面，不过比起以前控制台的黑框框，还是有进步的了。

![2.gif](https://i.loli.net/2018/06/07/5b19318907628.gif)

这个界面的代码很简单，就不贴出来了。不过给出一个加载本地保存好的`TensorFlow`模型，然后预测类别的代码。
```python
from skimage import io,transform
import tensorflow as tf
import numpy as np

#logdir='D:/Data/File/flower_photos/flower_photos/'
logdir='D:/Code/Python/Anaconda/dataset/'
suffix='.jpg'
path1 = logdir+"badCar/A_2"+suffix
path2 = logdir+"badCar/A_276"+suffix
path3 = logdir+"badCar/A_286"+suffix
path4 = logdir+"goodCar/B_32"+suffix
path5 = logdir+"goodCar/B_91"+suffix

#flower_dict = {0:'dasiy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}
car_dict={0:'dangerous',1:'norm car'}
w=100
h=100
c=3

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    data2 = read_one_image(path2)
    data3 = read_one_image(path3)
    data4 = read_one_image(path4)
    data5 = read_one_image(path5)
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
    data.append(data5)


saver = tf.train.import_meta_graph('D:/Code/Python/Anaconda/dataset/Model/.meta')
saver.restore(sess,tf.train.latest_checkpoint('D:/Code/Python/Anaconda/dataset/Model/'))

graph = tf.get_default_graph()
x = graph.get_tensor_by_name("x:0")
feed_dict = {x:data}

logits = graph.get_tensor_by_name("logits_eval:0")

classification_result = sess.run(logits,feed_dict)
classification_result=tf.nn.softmax(classification_result)
classification_result=classification_result.eval()
#打印出预测矩阵
#with np.set_printoptions(precision=5):
print(classification_result)



#打印出预测矩阵每一行最大值的索引
print(tf.argmax(classification_result,1).eval())
#根据索引通过字典对应花的分类
output = []
output = tf.argmax(classification_result,1).eval()
for i in range(len(output)):
    print("第",i+1,"辆车预测:"+car_dict[output[i]])
```
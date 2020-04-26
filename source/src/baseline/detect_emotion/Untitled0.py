#!/usr/bin/env python
# coding: utf-8

# In[1]:


from google.colab import drive
drive.mount('/content/drive')


# In[ ]:


pwd


# In[2]:


cd drive/My\ Drive


# In[5]:


get_ipython().system('apt install caffe-cpu')


# In[ ]:


get_ipython().system('wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \'https://docs.google.com/uc?export=download&id=0BydFau0VP3XSYk9ZVnVNd0ZvVk0\' -O- | sed -rn \'s/.*confirm=([0-9A-Za-z_]+).*/\\1\\n/p\')&id=0BydFau0VP3XSYk9ZVnVNd0ZvVk0" -O DemoDir.zip && rm -rf /tmp/cookies.txt')


# In[ ]:


get_ipython().system('unzip DemoDir.zip')


# In[6]:


cd DemoDir/


# In[10]:


import os
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import skimage

caffe_root = get_ipython().getoutput('cd caffe/python && pwd')
print(caffe_root)
import sys
sys.path.insert(0, caffe_root[0])  

import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


DEMO_DIR = '.'

categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']


# In[ ]:


def showimage(im):
    if im.ndim == 3:
        im = im[:, :, ::-1]
    plt.set_cmap('jet')
    plt.imshow(im,vmin=0, vmax=0.2)
    

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    showimage(data)


# In[7]:


cur_net_dir = 'VGG_S_rgb'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                      mean=mean,
                      channel_swap=(2,1,0),
                      raw_scale=255,
                      image_dims=(256, 256))

#input_image = caffe.io.load_image(os.path.join(DEMO_DIR,cur_net_dir,'demo_image.png'))
input_image = skimage.img_as_float(skimage.io.imread(os.path.join(DEMO_DIR,cur_net_dir,'kim_woo_bin.jpg'))).astype(np.float32)
prediction = VGG_S_Net.predict([input_image],oversample=False)
print (('predicted category is {0}').format(categories[prediction.argmax()]))


# In[ ]:


_ = plt.imshow(input_image)


# In[ ]:


filters = VGG_S_Net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# In[ ]:


feat = VGG_S_Net.blobs['conv1'].data[0]
vis_square(feat)


# In[ ]:


cur_net_dir = 'VGG_S_lbp'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

# mean = None #Only for better visualization

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

input_image = skimage.img_as_float(skimage.io.imread(os.path.join(DEMO_DIR,cur_net_dir,'demo_image.png'))).astype(np.float32)
prediction = VGG_S_Net.predict([input_image],oversample=False)
print (('predicted category is {0}').format(categories[prediction.argmax()]))


# In[ ]:


_ = plt.imshow(input_image)


# In[ ]:


filters = VGG_S_Net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# In[ ]:


feat = VGG_S_Net.blobs['conv1'].data[0]
vis_square(feat)


# In[ ]:


cur_net_dir = 'VGG_S_cyclic_lbp'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

# mean = None #Only for better visualization

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

input_image = skimage.img_as_float(skimage.io.imread(os.path.join(DEMO_DIR,cur_net_dir,'demo_image.png'))).astype(np.float32)
prediction = VGG_S_Net.predict([input_image],oversample=False)
print (('predicted category is {0}').format(categories[prediction.argmax()]))


# In[ ]:


_ = plt.imshow(input_image)


# In[ ]:


filters = VGG_S_Net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# In[ ]:


feat = VGG_S_Net.blobs['conv1'].data[0]
vis_square(feat)


# In[ ]:


cur_net_dir = 'VGG_S_cyclic_lbp_5'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

# mean = None #Only for better visualization

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

input_image = skimage.img_as_float(skimage.io.imread(os.path.join(DEMO_DIR,cur_net_dir,'demo_image.png'))).astype(np.float32)
prediction = VGG_S_Net.predict([input_image],oversample=False)
print (('predicted category is {0}').format(categories[prediction.argmax()]))


# In[ ]:


_ = plt.imshow(input_image)


# In[ ]:


filters = VGG_S_Net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# In[ ]:


feat = VGG_S_Net.blobs['conv1'].data[0]
vis_square(feat)


# In[ ]:


cur_net_dir = 'VGG_S_cyclic_lbp_10'

mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

# mean = None #Only for better visualization

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

input_image = skimage.img_as_float(skimage.io.imread(os.path.join(DEMO_DIR,cur_net_dir,'demo_image.png'))).astype(np.float32)
prediction = VGG_S_Net.predict([input_image],oversample=False)
print (('predicted category is {0}').format(categories[prediction.argmax()]))


# In[ ]:


_ = plt.imshow(input_image)


# In[ ]:


filters = VGG_S_Net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# In[ ]:


feat = VGG_S_Net.blobs['conv1'].data[0]
vis_square(feat)


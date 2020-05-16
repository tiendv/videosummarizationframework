# CNN.py (Convolutional Neural Network Feature Extractor)
__Version__: 1.0
## Requirements
The main library
``` bash
tensorflow
tensorflow-gpu
keras
torch
torchvision
opencv-python
and more . . . 
````
___
## Usage on another script
Four class ``ExtractFeatureVideo``, ``ExtractFeatureDataSet``, ``ExtractFeatureFolderImages``, ``ExtractFeatureImages``

Import to use

``` bash
from CNN import ExtractFeatureVideo, ExtractFeatureDataSet, ExtractFeatureFolderImages, ExtractFeatureImages
```
### Extract Feature Video

`` module = ExtractFeatureVideo(video_path,sampling_rate=int,device_name='str')
``

`` feature = module.VGG16(output_layer='str')
``

`` feature.save(path_to_save)
``

This code support VGG16, VGG19, ResNet50, ResNet152, InceptionV1, InceptionV3. To use anoher architecture read tutorial below.

--

### Extract Feature DataSet

This class is inheritance of ExtractFeatureVideo. 

`` module = ExtractFeatureDataSet(dataset_name,output_path,from_id=int,to_id=int,sampling_rate=int,device_name='str'):
``

``module.VGG19(output_layer='str')
``

### Extract Feature Folder Images
This class is inheritance of ExtractFeatureVideo.

`` module = ExtractFeatureFolderImages(folder_images,sampling_rate=int,device_name='str')
``

`` feature = module.VGG16(output_layer='str')
``

`` feature.save(path_to_save)
``

### Extract Feature Folder Images
This class is inheritance of ExtractFeatureVideo.

`` module = ExtractFeatureImages(list_image,name_of_file,sampling_rate=int,device_name='str')
``

`` feature = module.VGG16(output_layer='str')
``

`` feature.save(path_to_save)
``
---

## Usage CNN.py script

### There are two ways to use this script

#### The Fisrt Way: Load info from config file

Modify file config_extractfeature.py from ``videosummarizationframework/source/config/config_extractfeature.py``

Dataset: Modify variable has prefix DATASET_*

Video: Modify variable has prefix VIDEO_*

Images: Modify variable has prefix IMAGES_*

Use command ``python CNN.py video`` or ``python CNN.py dataset`` or ``python CNN.py images`` to run

#### The Second Way: Run by command

Use command ``python CNN.py --help`` or ``python CNN.py -h``  for see full arguments

### Positional arguments

``python CNN.py datatype -uts
``

``datatype`` is name of datatype. Support: dataset, video, images (folder images)

``-uts`` : is stand for "Use This Script". Boolean Flag

#### Example

``python CNN.py video -uts``  |    ``python CNN.py dataset -uts`` |    ``python CNN.py images -uts``

``python CNN.py v -uts``  |    ``python CNN.py d -uts`` |    ``python CNN.py i -uts``

### Optional arguments

Include positional arguments, and have three optional ``+Video`` and ``+Dataset`` and ``+Images``

``+Video``

+ __*Method**__ : Name of CNN

+ __*VideoPath**__ : Path to video

+ __*-sr or --samplingRate*__: Sampling rate, default = 1.

+ __*-l or --layer*__: Name of hiden layer on CNN architecture, default=None.

+ __*-d or --device*__: Device use to run, default='0'.

+ __*-s or --save*__: Path to save feature data to file, default=None.
    + Example: ``python CNN.py video -uts +Video resnet152 /path/to/video.mp4 -sr 2 -d 1 -s path/to/folder/save/ -l fc1``

``+DataSet``

+ _*Method*_ : Name of CNN

+ __*DataSetName**__ : Name of Dataset. Support three dataset: _*BBC EastEnders, TVSum50, SumMe*_. To use on another dataset, read tutorial below.

+ _*OutputPath*_ : Path to folder save feature data file. 

+ __*-f or --fromid*__ : ID begin-th video, default=None.

+ __*-e or --endid*__ : ID end-th video. Two args use for big dataset. Run from video begin-th to video end-th, default=None.

+ __*-sr or --samplingRate*__: Sampling rate, default = 1.

+ __*-d or --device*__: Device use to run, default='0'.
    
    + Example: ``python CNN.py dataset -uts +DataSet resnet152 bbc /path/folder/out -f 12 -e 35 -sr 2 -d 2``

_*To use on another dataset. Try to use file utilities/make_csv_from_dataset.py with command*_

``python make_csv_from_dataset.py +newdataset dataset_name /path/to/folder/video /path/to/folder/out``


``+Images``

+ __*Method**__ : Name of CNN

+ __*DataFolder**__ : Folder storage images

+ __*-sr or --samplingRate*__: Sampling rate, default = 1.

+ __*-l or --layer*__: Name of hiden layer on CNN architecture, default=None.

+ __*-d or --device*__: Device use to run, default='0'.

+ __*-s or --save*__: Path to save feature data to file, default=None.

    + Example: ``python CNN.py images -uts +Images inceptionv1 /path/to/folder -sr 2 -d 1 -s path/to/folder/save/ -l fc1``

---

## Add new CNN architector

There are two famous frameworks used for extract feature is ``tensorflow`` and ``pytorch``. I make two template for them.

### Tensorflow 

[Read this template code.](https://github.com/PhamThinh31/src-for-videosummarization/blob/master/template-tensorflow.py)

Brief code:

```
def NAME_OF_CNN_HERE(self,output_layer=OUTPUT_LAYER_HERE):
    ...
    base_model = tensorflow_model_here.TENSORFLOW_MODEL_HERE(weights='imagenet')
    ...
    self.imageSize = (XXX_HERE,YYY_HERE) #size of image
    ... 
```
Change the content of the lines that have the words *HERE. Read comment on template code

### Pytorch 

[Read this template code.](https://github.com/PhamThinh31/src-for-videosummarization/blob/master/template-pytorch.py)

Brief code:

```
class NAME_OF_CNN_HERE(nn.Module):
        ---
        change_pytorch_model_here = models.CHANGE_PYTORCH_MODE_HERE(pretrained=True)
        ...
        change_pytorch_model_here.float()
        change_pytorch_model_here.cuda()
        change_pytorch_model_here.eval()
        module_list = list(CHANGE_PYTORCH_MODEL_HERE.children())
        self.conv5 = nn.Sequential(*module_list[: -XXX_HERE]) 
    ---
```
Change the content of the lines that have the words *HERE. Read comment on template code
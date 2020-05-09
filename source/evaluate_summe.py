import scipy.io
import warnings
import numpy as np
import os ,sys,glob
import datetime
import time
import json
import cv2

def time2sec(times):
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() +float(times.split(".")[1])/10000)

def evaluateSummary(summary_selection,videoName,HOMEDATA):
     '''Evaluates a summary for video videoName (where HOMEDATA points to the ground truth file)   
     f_measure is the mean pairwise f-measure used in Gygli et al. ECCV 2013 
     NOTE: This is only a minimal version of the matlab script'''
     # Load GT file
     gt_file=HOMEDATA+'/'+videoName+'.mat'
     gt_data = scipy.io.loadmat(gt_file)
     
     user_score=gt_data.get('user_score')
     nFrames=user_score.shape[0];
     nbOfUsers=user_score.shape[1];
    
     # Check inputs
     if len(summary_selection) < nFrames:
          warnings.warn('Pad selection with %d zeros!' % (nFrames-len(summary_selection)))
          summary_selection.extend(np.zeros(nFrames-len(summary_selection)))

     elif len(summary_selection) > nFrames:
          warnings.warn('Crop selection (%d frames) to GT length' %(len(summary_selection)-nFrames))       
          summary_selection=summary_selection[0:nFrames];
             
     
     # Compute pairwise f-measure, summary length and recall
     summary_indicator=np.array(map(lambda x: (1 if x>0 else 0),summary_selection));  
     user_intersection=np.zeros((nbOfUsers,1));
     user_union=np.zeros((nbOfUsers,1));
     user_length=np.zeros((nbOfUsers,1));
     for userIdx in range(0,nbOfUsers):
         gt_indicator=np.array(map(lambda x: (1 if x>0 else 0),user_score[:,userIdx]))
         
         user_intersection[userIdx]=np.sum(gt_indicator*summary_indicator);
         user_union[userIdx]=sum(np.array(map(lambda x: (1 if x>0 else 0),gt_indicator + summary_indicator)));         
                  
         user_length[userIdx]=sum(gt_indicator)
    
     recall=user_intersection/user_length;
     p=user_intersection/np.sum(summary_indicator);

     f_measure=[]
     for idx in range(0,len(p)):
          if p[idx]>0 or recall[idx]>0:
               f_measure.append(2*recall[idx]*p[idx]/(recall[idx]+p[idx]))
          else:
               f_measure.append(0)
     nn_f_meas=np.max(f_measure);
     f_measure=np.mean(f_measure);
    
     nnz_idx=np.nonzero(summary_selection)
     nbNNZ=len(nnz_idx[0])
         
     summary_length=float(nbNNZ)/float(len(summary_selection));

     recall=np.mean(recall);
     pre =np.mean(p);

     return pre , recall ,f_measure

if __name__ == '__main__':
     ''' PATHS ''' 
     HOMEDATA='/mmlabstorage/datasets/SumMe/GT/'
     path_video = '/mmlabstorage/datasets/SumMe/videos'
     data ="/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_segment/dsf_kts_vgg16"
     path_save = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/SumMe/KTS_DSF_VGG16_Kmedoids/KTS_DSF_VGG16_Kmedoids.json"
     json_summe = {}
     videos = glob.glob(os.path.join(HOMEDATA,"*"))
     for i in range (len(videos)):
          videos[i]=(videos[i].split("/")[-1]).replace(".mat","")
     p = []
     r = []
     f1 = []
     for videoName in videos:
          seg = []
          print videoName
          gt_file=HOMEDATA+'/'+videoName+'.mat'
          gt_data = scipy.io.loadmat(gt_file)
          fps=gt_data.get('FPS')[0][0]
          fps_video = 0
          video =  cv2.VideoCapture(os.path.join(path_video,videoName+".mp4"))
            ###
          total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            #print total_frames
        #    video.set(cv2.CAP_PROP_POS_AVI_RATIO,total_frames)
        #    duration=video.get(cv2.CAP_PROP_POS_MSEC)
          (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
          if int(major_ver)  < 3 :
               fps_video = video.get(cv2.cv.CV_CAP_PROP_FPS)
                #print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
          else :
               fps_video = video.get(cv2.CAP_PROP_FPS)
          user_score=gt_data.get('user_score')
          nFrames=user_score.shape[0]
          data_file = data + '/' + videoName+ '/' + videoName + ".txt" 
          with open(data_file,"r") as f:
               lines = list(f)
               for line in lines :
                    seg.append(int(time2sec(line.split(" ")[0])*fps+0.5))
                    seg.append(int(time2sec(line.split(" ")[1])*fps+0.5))
          in_seg = False
          summary_selection = [0]*nFrames
          for i in range(int(len(seg)/2)):
               start = seg[i*2]
               end = seg[i*2+1]
               for j in range(end-start):
                    idx = start+j
                    if start+j >= nFrames :
                        idx = nFrames -1
                    summary_selection[idx] = 1
          pre , recall ,f_measure = evaluateSummary(summary_selection,videoName,HOMEDATA)
          p.append(pre)
          r.append(recall)
          f1.append(f_measure)
          print pre , recall , f_measure
     data_json= {}
     for i in range(len(videos)):
          temp = {}
          temp["pre"] = "{:.2f}".format(p[i])
          temp["rc"] = "{:.2f}".format(r[i])
          temp["f1"] = "{:.2f}".format(float(f1[i]))
          data_json[videos[i]] = temp
     temp = {}
     temp["pre"] = "{:.2f}".format(float(sum(p)/len(p)))
     temp["rc"] = "{:.2f}".format(float(sum(r)/len(r)))
     temp["f1"] = "{:.2f}".format(float(sum(f1)/len(f1)))
     print "***MEAN*** Pre:",temp["pre"],"Recall:",temp["rc"],"F1:",temp["f1"]
     data_json["mean"] = temp
     json_summe["result"] = data_json
     json_summe["thres"] = 0.5
     with open(path_save, 'w') as outfile:
         json.dump(json_summe, outfile)




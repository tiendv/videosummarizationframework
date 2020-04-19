import os,json
import xml.etree.cElementTree as ET
from config.config import cfg
from utilities.get_data_ref_bbc import get_data_ref_bbc
from utilities.convert_time import time2sec

def getSelectedBBCShot(selected_shot_path,vid_id,ref_id, time_shots):
    shot_list = []
    name_vid = ref_id[str(vid_id)]
    print(name_vid)
    input()
    with open(os.path.join(selected_shot_path,"{n}/{n}.json".format(n=name_vid)),'r') as f:
        data = json.load(f)

    #get data shots
    shot_data = data["localisation"][0]["sublocalisations"]["localisation"]

    i = 1
    for shot in shot_data:
        st = time2sec(shot['tcin'])
        en = time2sec(shot['tcout'])
        while True:
            shot_id = 'shot{}_{}'.format(vid_id,i)
            try:
                t = time2sec(time_shots[shot_id][0])
            except Exception as e:
                return shot_list
            if st<=t<=en:
                shot_list.append(shot_id)
            if t>en:
                break
            i=i+1
    return shot_list


def gen_video_sum(file_name,shot_list,bbc_video_path,save_path):
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    with open('temp.txt','w') as f:
        for shot in shot_list:
            id = shot.split("_")[0].replace("shot","")
            path_save = os.path.join(bbc_video_path,'video{}'.format(id))
            f.write('file {}.mp4\n'.format(os.path.join(path_save,shot.rstrip())))

    os.system("ffmpeg -f concat -safe 0 -i temp.txt -c copy {}".format(os.path.join(save_path,file_name)))
    os.system("rm temp.txt")
    print("the result video be saved at"+os.path.join(save_path,file_name))

def create_submission_vsum(shot_list,char,summTime,method,team_name,prior,name_xml_file='temp.xml'):
    mp4_name = '{}_{}_{}'.format(team_name, prior,char)
    root = ET.parse('../result/submission_template.xml').getroot()
    info = root.find("videoSummarizationRunResult")
    info.set("pid",team_name)
    info.set("priority",str(prior))
    info.set("desc",method)

    result = ET.SubElement(info, "videoSummarizationTopicResult")
    result.set("target",char)
    result.set("summTime",str(summTime))
    result.tail = '\n'
    for i,shot in enumerate(shot_list):
        ET.SubElement(result, "item", seqNum=str(i),shotId=shot).tail='\n'


    with open("../result/{}".format(name_xml_file), 'wb') as f:
        f.write('<!-- Example video summarization results for a vsum run  -->\n<!DOCTYPE videoSummarizationResults SYSTEM "https://www-nlpir.nist.gov/projects/tv2020/dtds/videoSummarizationResults.dtd">\n'.encode('utf8'))
        tree = ET.ElementTree(root)
        tree.write(f,'utf-8')

if __name__ == '__main__':
    vid_id = 1
    method = "dsf_seg_vsum_rgb"
    ref_id, time_shots = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)

    shot_list = getSelectedBBCShot(cfg.PATH_JSON_SHOT_RGB_SUM_DSF_BBC,vid_id,ref_id, time_shots)

    file_name = "{n}_{m}.mp4".format(m=method,n=ref_id[str(vid_id)])
    gen_video_sum(file_name,shot_list,cfg.PATH_SHOT_BBC,cfg.PATH_RESULT_VSUM_BBC)
    # create_submission_vsum(shot_list,'heather',2.14,'this method','uitnii',3)

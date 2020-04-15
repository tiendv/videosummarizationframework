import os
import xml.etree.cElementTree as ET
from config.config import cfg
def gen_video_sum(bbc_video_path,shot_list,save_path):
    with open('temp.txt','w') as f:
        for shot in shot_list:
            id = shot.split("_")[0].replace("shot","")
            path_save = os.path.join(bbc_video_path,'video{}'.format(id))
            f.write('file {}.mp4\n'.format(os.path.join(path_save,shot.rstrip())))
    os.system("ffmpeg -f concat -safe 0 -i temp.txt -c copy {}".format(save_path))
    os.system("rm temp.txt")
    print("the result video be saved at"+save_path)

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
    shot_list = ['shot1_1790','shot1_15','shot1_17','shot1_19','shot1_154']
    # create_submission_vsum(shot_list,'heather',2.14,'this method','uitnii',3)
    gen_video_sum(cfg.PATH_SHOT_BBC,shot_list,'../result/vsum.mp4')

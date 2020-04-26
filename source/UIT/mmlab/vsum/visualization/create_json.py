from src.baseline.segmentation.create_shot_json import create_json4shots

def create_shot_json(path_json, name_vid,list_begin,list_score=None,id="shot_gt"):
    create_json4shots(path_json, name_vid,list_begin,list_score,id)
    print("The result file is saved at " + path_json + "/"+name_vid)

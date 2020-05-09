from src.baseline.segmentation.create_shot_json import create_json4shots,create_json4shots_file
from src.baseline.selection.get_data_selection import create_json_selections

def create_shot_json(json_path, vid_name,begin_list,score_list=None,json_id="shot_gt"):
    create_json4shots(json_path, vid_name,begin_list,score_list,json_id)
    print("The result file is saved at " + json_path + "/"+vid_name)

def create_shot_json_from_file(file_path,json_path,vid_name,json_id="shot_gt"):
    create_json4shots_file(file_path,json_path,vid_name,json_id)

sys.path.append("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/baseline/selection/")
from select_shot import selection_shot_knapsack,create_selection_file

def do_knapsack(vid_name,begin_list,end_list,score_list,selected_shot_file_path):
    result = selection_shot_knapsack(begin_list,end_list,score_list)
    create_selection_file(vid_name,begin_list,end_list,result,selected_shot_file_path)
    print("Done selection for video{}".format(name_video))

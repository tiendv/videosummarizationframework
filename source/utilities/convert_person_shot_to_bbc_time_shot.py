import glob,os
from get_data_ref_bbc import get_data_ref_bbc

def convert_to_bbc_time_shot(person_shot_path,bbc_time_shot_path):
    ref_id, time_shots = get_data_ref_bbc("../../data/BBC_processed_data/reference_bbc/master_shot_reference.txt")
    paths = glob.glob(person_shot_path+"/*/*.txt")
    for p in paths:
        vid_name = p.split("/")[-2][5:]
        vid_name = ref_id[vid_name]
        file_name = os.path.basename(p)
        saved_path = os.path.join(bbc_time_shot_path,vid_name)

        if not os.path.isdir(saved_path):
              os.makedirs(saved_path)
        with open(p,'r') as f:
            shots = f.read().splitlines()
        shots.sort(key=lambda x: int(x.replace('shot','')))
        with open(os.path.join(saved_path,file_name),'w') as f:
            for s in shots:
                f.write('{} {} {}\n'.format(s,time_shots[s][0],time_shots[s][1]))

if __name__ == '__main__':
    convert_to_bbc_time_shot("../../data/BBC_processed_data/VSUM_TRECVID/vsum_shots","../../data/BBC_processed_data/VSUM_TRECVID/bbc_person_segment")

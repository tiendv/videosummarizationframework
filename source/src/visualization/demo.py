from flask import Flask, render_template , request, session
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import glob
import numpy as np, h5py
app = Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'dungmn'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'mmlabsum'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

path_thumbnails_tvsum = "TVSum50/ydata-tvsum50-v1_1/thumbnail"
static_folder = "static"
path_matlab_gt='static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['mp4','webm'])
filename= ''
tvsum50_temp = []
bbc_temp = []

def create_dictionary_tvsum50(path_thumbnails,link_path,matlab_gt):
    f = h5py.File(matlab_gt,'r')
    title_gt = f.get('tvsum50/title')
    data_name = f.get('tvsum50/video')
    list_name = []
    for i in range(data_name.shape[0]):
        name= ''.join(map(chr,f[data_name[i][0]]))
        list_name.append(name)
    list_title = {}
    for i in range(title_gt.shape[0]):
        title= ''.join(map(chr,f[title_gt[i][0]]))
        list_title[list_name[i]]=title
    path_thumbnails = glob.glob(static_folder+"/"+path_thumbnails+"/*")
    path_thumbnails = [file[(len(static_folder)+1):] for file in path_thumbnails]
    data_list = []
    link_video = []
    for i in path_thumbnails :
        link = link_path + i.split("/")[len(i.split("/"))-1].replace('jpg','mp4') + "&para_title=Title:" + ((((list_title[i.split("/")[len(i.split("/"))-1].replace('.jpg','')]).replace(" ","_")).replace("&","and")).replace("+","")).replace("#","")
        link_video.append(link)
    for i in range(len(path_thumbnails)):
        dict_temp = {}
        dict_temp['video'] = link_video[i]
        dict_temp['thumbnail'] = path_thumbnails[i]
        data_list.append(dict_temp)
    return data_list

def create_dictionary_bbc(path_videos,link_path):
    path_videos = glob.glob(static_folder+"/"+path_videos+"/*.mp4")
    path_videos = [file[(len(static_folder)+1):] for file in path_videos]
    data_list = []
    link_video = []
    for i in path_videos :
        link = link_path + i.split("/")[len(i.split("/"))-1]
        link_video.append(link)
    for i in range(len(path_videos)):
        dict_temp = {}
        dict_temp['video'] = link_video[i]
        dict_temp['thumbnail'] = path_videos[i]
        data_list.append(dict_temp)
    return data_list

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route for handling the login page logic
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'mmlab' or request.form['password'] != 'mmlab19':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('homepage'))
#     return render_template('index.html', error=error)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/',methods=['GET','POST'])
def homepage():
    return render_template('homepage.html' )


@app.route('/TVSum50',methods=['GET','POST'])
def TVSum50():
    return render_template('TVSum50.html',data_list = tvsum50_temp )


@app.route('/TRECVID_BBC_EastEnders',methods=['GET','POST'])
def TRECVID_BBC_EastEnders():
    return render_template('TRECVID_BBC_EastEnders.html',data_list = bbc_temp )


@app.route('/visualTVSum50',methods=['GET','POST'])
def visual_TVSum50():
    return render_template('TVSum50_video.html')

@app.route('/visualTRECVID_BBC_EastEnders',methods=['GET','POST'])
def visual_TRECVID_BBC_EastEnders():
    return render_template('TRECVID_BBC_EastEnders_video.html')

if __name__ == "__main__":
    tvsum50_temp = create_dictionary_tvsum50(path_thumbnails_tvsum,"/visualTVSum50?file_id=",path_matlab_gt)
    bbc_temp = create_dictionary_bbc("TRECVID_BBC_EastEnders/videos/","/visualTRECVID_BBC_EastEnders?file_id=")
    app.run(host="192.168.28.13",port=5000, debug=True)

from flask import Flask, render_template , request, session
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename
from datetime import timedelta
from preprocessing import *
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/code')
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/code/tools')
from frame_work import sum_video

app = Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'dungmn'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'mmlabsum'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['mp4','webm'])
app.config['UPLOAD_FOLDER'] = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/video'
filename= ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/',methods=['GET','POST'])
def homepage():
    return render_template('homepage.html' )

@app.route('/TVSum50',methods=['GET','POST'])
def TVSum50():
    return render_template('TVSum/TVSum50.html',data_list = tvsum50_temp )

@app.route('/evaluation',methods=['GET','POST'])
def evaluation():
    return render_template('evaluation.html')

@app.route('/demokltn',methods=['GET','POST'])
def demokltn():
    #return render_template('Demo/thinh_test.html')
    if request.method == 'POST':
        segment = request.form.get('segment')
        score = request.form.get('score')
        selection = request.form.get('selection')
        len_sum = int(request.form.get('lentgh_sum'))
        len_sum = (len_sum)/100
        print("Thinhplg", segment,score,selection,len_sum)
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(((((f.filename).replace(' ','_')).replace("&","and")).replace("+","")).replace("#",""))))
        if ((((f.filename).replace(' ','_')).replace("&","and")).replace("+","")).replace("#","").split('.')[-1] != 'webm':
            import moviepy.editor as mp
            clip = mp.VideoFileClip('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/video/'+((((f.filename).replace(' ','_')).replace("&","and")).replace("+","")).replace("#",""))
            clip.write_videofile('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/video/'+(((((f.filename).replace((f.filename).split('.')[-1],'webm')).replace(' ','_')).replace("&","and")).replace("+","")).replace("#",""))
        with open('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/Demo/temp.txt', 'w') as file_temp:
            file_temp.write((((((f.filename).replace((f.filename).split('.')[-1],'webm')).replace(' ','_')).replace("&","and")).replace("+","")).replace("#",""))
        sum_video(segment,score,len_sum)
        list_demo = []
        dict_demo = {}
        dict_demo['video'] = '/visualdemo?file_id='+(((((f.filename).replace((f.filename).split('.')[-1],'webm')).replace(' ','_')).replace("&","and")).replace("+","")).replace("#","")
        list_demo.append(dict_demo)
        return render_template('Demo/thinh_test.html',data_list=list_demo)
    return render_template('Demo/thinh_test.html')


@app.route('/visualdemo',methods=['GET','POST'])
def visual_demo():
    return render_template('Demo/kltn_video.html')


@app.route('/evaluation_chart',methods=['GET','POST'])
def evaluation_chart():
    return render_template('evaluation_chart.html')

@app.route('/eval_summary',methods=['GET','POST'])
def eval_summary():
    if request.method == 'POST':
        data = {}
        data['dataset'] = request.form['dataset']
        data['method'] = request.form['method']
    return render_template('TVSum/evaluateTVSum50.html', data_config = data)

@app.route('/result_BBC',methods=['GET','POST'])
def result_BBC():
    return render_template('BBC/sum_result_BBC.html')

@app.route('/result_BBC_video',methods=['GET','POST'])
def result_BBC_video():
    data = {}
    data['vid_name'] = request.args.get('vid_name')
    return render_template('BBC/sum_result_BBC_video.html', data_config = data)

@app.route('/TRECVID_BBC_EastEnders',methods=['GET','POST'])
def TRECVID_BBC_EastEnders():
    return render_template('BBC/TRECVID_BBC_EastEnders.html',data_list = bbc_temp )

@app.route('/BBC_TRECVID',methods=['GET','POST'])
def BBC_TRECVID():
    return render_template('BBC_TRECVID/BBC_TRECVID.html',data_list = bbc_trecvid )

@app.route('/SumMe',methods=['GET','POST'])
def SumMe():
    return render_template('Summe/SumMe.html',data_list = summe_temp )

@app.route('/visualTVSum50',methods=['GET','POST'])
def visual_TVSum50():
    return render_template('TVSum/TVSum50_video.html')

@app.route('/visualTRECVID_BBC_EastEnders',methods=['GET','POST'])
def visual_TRECVID_BBC_EastEnders():
    return render_template('BBC/TRECVID_BBC_EastEnders_video.html')

@app.route('/visual_BBC_TRECVID',methods=['GET','POST'])
def visual_BBC_TRECVID():
    return render_template('BBC_TRECVID/BBC_TRECVID_video.html')

@app.route('/visualSumMe',methods=['GET','POST'])
def visual_SumMe():
    return render_template('Summe/SumMe_video.html')

@app.route('/result_175',methods=['GET','POST'])
def result_175():
    return render_template('BBC/BBC_TRECVID_video175.html')

@app.route('/result_video175',methods=['GET','POST'])
def result_video175():
    return render_template('BBC/BBC_TRECVID_result_video175.html')

if __name__ == "__main__":
    path_thumbnails_tvsum = "TVSum50/ydata-tvsum50-v1_1/thumbnail"
    path_matlab_gt='static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat'

    tvsum50_temp = create_dictionary_tvsum50(path_thumbnails_tvsum,"/visualTVSum50?file_id=",path_matlab_gt)
    bbc_temp = create_dictionary_bbc("TRECVID_BBC_EastEnders/videos/","thumbnails_BBC/","/visualTRECVID_BBC_EastEnders?file_id=")
    summe_temp = create_dictionary_summe("SumMe/videos/","thumbnails_SumMe/","/visualSumMe?file_id=")
    bbc_trecvid = create_bbc_trecvid_dict("thumbnails_BBC/","/visual_BBC_TRECVID?file_id=")
    app.run(host="0.0.0.0", port=5000,debug=True)

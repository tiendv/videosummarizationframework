from flask import Flask, render_template , request, session
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename
from datetime import timedelta
from preprocessing import *
app = Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'dungmn'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'mmlabsum'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['mp4','webm'])
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

if __name__ == "__main__":
    path_thumbnails_tvsum = "TVSum50/ydata-tvsum50-v1_1/thumbnail"
    path_matlab_gt='static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat'

    tvsum50_temp = create_dictionary_tvsum50(path_thumbnails_tvsum,"/visualTVSum50?file_id=",path_matlab_gt)
    bbc_temp = create_dictionary_bbc("TRECVID_BBC_EastEnders/videos/","thumbnails_BBC/","/visualTRECVID_BBC_EastEnders?file_id=")
    summe_temp = create_dictionary_summe("SumMe/videos/","thumbnails_SumMe/","/visualSumMe?file_id=")
    bbc_trecvid = create_bbc_trecvid_dict("thumbnails_BBC/","/visual_BBC_TRECVID?file_id=")
    app.run(host="0.0.0.0", port=80,debug=True)

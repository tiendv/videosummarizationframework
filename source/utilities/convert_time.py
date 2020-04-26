import datetime
import time

def sec2time(sec, n_msec=4):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)
def time2sec(times):
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    range_mili = 1
    mili = 0
    if len(times.split(".")) == 2 :
        if times.split(".")[1] != '':
            for i in range(len(times.split(".")[1])):
                range_mili = 10*range_mili
            mili = float(times.split(".")[1])/range_mili
        else:
            mili =0
    else:
        mili = 0
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() + mili)


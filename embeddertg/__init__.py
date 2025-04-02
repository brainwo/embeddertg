def no_long_video(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration > 600:
        raise Exception('The video is too long (>10 mins)')


YDL_OPTS = {
    'outtmpl': '/tmp/output.mp4',
    # Sets video to maximum 480p to saves bandwidth
    'format': '(mp4)[height<=480]',
    'overwrites': True,
    'match_filter': no_long_video,
}

__version__ = "0.2.0"
__license__ = "MIT"

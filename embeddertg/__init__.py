YDL_OPTS = {
    'outtmpl': 'output',
    # Sets video to maximum 480p to saves bandwidth
    'format': 'bv[height<=480]+ba/b[height<=480]',
    'overwrites': True
}

__version__ = "0.1.0"
__license__ = "MIT"

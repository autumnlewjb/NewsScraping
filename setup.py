import io
from PIL import ImageTk
from notify_run import Notify
from pyqrcode import QRCode


def register_notify():
    reg = Notify()
    print('Register at {}'.format(reg.register().endpoint))

    input('Press Enter after registration')

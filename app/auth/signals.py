from blinker import Namespace
from .subscribers import signup_subscriber

signals = Namespace()
signup = signals.signal('signup')
signup.connect(signup_subscriber)
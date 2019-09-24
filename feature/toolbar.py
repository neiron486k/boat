from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension()


def toolbar_feature(app):
    toolbar.init_app(app)

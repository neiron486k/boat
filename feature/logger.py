from logging import FileHandler, WARNING
import logging
import os


def logging_feature(app):
    target = os.getcwd() + '/logs'

    if not app.debug:
        os.makedirs(target, exist_ok=True)
        file_handler = FileHandler(target + '/' + os.environ.get('FLASK_ENV') + '.txt')
        file_handler.setLevel(WARNING)

        for logger in (
                app.logger,
                logging.getLogger('sqlalchemy'),
        ):
            logger.addHandler(file_handler)

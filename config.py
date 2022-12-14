import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    # # 把错误通过电子邮件发送给管理员
    # import logging
    # from logging.handlers import SMTPHandler
    # credentials = None
    # secure = None
    # if getattr(cls, 'MAIL_USERNAME', None) is not None:
    #     credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
    # if getattr(cls, 'MAIL_USE_TLS', None):
    #     secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
    #         fromaddr=cls.FLASKY_MAIL_SENDER,
    #         toaddrs=[cls.FLASKY_ADMIN],
    #         subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
    #         credentials=credentials,
    #         secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)


config = {
 'development': DevelopmentConfig,
 'testing': TestingConfig,
 'production': ProductionConfig,
 'default': DevelopmentConfig
}

# config.py
# written by STan


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """


# Enable Flask's debugging features. Should be False in production
DEBUG = True
SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}



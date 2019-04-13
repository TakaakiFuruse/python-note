class Config:
    """Base config"""


class ProdConfig(Config):
    """Production Config"""

    ENV = "production"
    DEBUG = False


class DevConfig(Config):
    """Dev Config"""

    ENV = "development"
    DEBUG = True


class TestConfig(Config):
    """Test config"""

    ENV = "test"
    TESTING = True
    DEBUG = True

import os
import yaml
import logging
import coloredlogs
import logging.config

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath("account"))

# 日志配置文件
LOG_CONF_FILE = os.path.join(BASE_DIR, "resource", 'logging.yaml')


def setup_logging(default_path=LOG_CONF_FILE, default_level=logging.DEBUG, env_key='LOG_CFG'):
    """
    配置项目日志信息
    :param default_path: 日志文件默认路径
    :param default_level: 日志默认等级
    :param env_key: 系统环境变量名
    :return:
    """
    path = default_path

    value = os.getenv(env_key, None)  # 获取对应的环境变量值
    if value is not None:
        path = value

    if os.path.exists(path):
        with open(path, mode='r', encoding='utf-8') as f:
            try:
                logging_yaml = yaml.safe_load(f.read())
                logging.config.dictConfig(logging_yaml)
                coloredlogs.install(level='DEBUG')
            except Exception as e:
                print(e)
                print('无法加载日志配置文件, 请检查日志目录是否创建, 使用默认的日志配置')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('日志配置文件不存在, 使用默认的日志配置')

# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import argparse
import logging

from .crawler_util import *
from .slider_util import *
from .time_util import *


def init_loging_config():
    # level = logging.ERROR
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _logger = logging.getLogger("MediaCrawler")
    _logger.setLevel(level)
    return _logger


logger = init_loging_config()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

async def set_config(crawler, config, kwargs, platform):
    new_kwargs = dict()
    for key, value in kwargs.items():
        if key == 'C': key = 'CRAWLER_MAX_NOTES_COUNT'
        if key == 'P': continue
        key = key.replace(f'{platform}_', '')
        if not hasattr(config, key):
            continue
        new_kwargs[key] = value
        old_value = getattr(config, key)
        if isinstance(old_value, bool):
            if value == 'True':
                setattr(config, key, True)
            else:
                setattr(config, key, False)
        elif isinstance(old_value, int):
            setattr(config, key, int(value))
        else:
            setattr(config, key, value)
    
    if 'HEADLESS' not in new_kwargs:
        config.HEADLESS = True
    
    if 'LOGIN_TYPE' not in new_kwargs:
        config.LOGIN_TYPE = 'cookie'

    if 'COOKIES' in new_kwargs:
        await crawler.close()
        await crawler.start()
    

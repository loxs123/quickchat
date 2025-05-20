# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


# 基础配置
PLATFORM = "xhs" # 平台名称，支持：xhs、dy、ks、bili、wb、tieba、zhihu
KEYWORDS = "足球"  # 关键词搜索配置，以英文逗号分隔
LOGIN_TYPE = "cookie"  # qrcode or phone or cookie
COOKIES = "x-user-id-creator.xiaohongshu.com=5e95337a0000000001005851; gid=yYfWYjfjjKi8yYfWYjfYi8yId4jWC1u3A4jYdqEV8ExT0J280FuDSY888JjYJqJ82iyqj48q; abRequestId=76b634c650413aa67b645ef8f90476b7; customerClientId=473594761764599; a1=194fa7b5de267699iksw72j8prqgr41u1h6339euf50000837707; webId=4800a89d2df28af40822dbe40c37074b; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517498911671060903518ddm1hcl9wf7qiosz; galaxy_creator_session_id=NU0qxcBrMVJIaSBG9N3j4T4DOkRaN272VjVe; galaxy.creator.beaker.session.id=1745976431573034709606; xsecappid=xhs-pc-web; acw_tc=0a00dd8917476634438266630e1a719a5752c57e44f078761f7f32e7a06a3c; webBuild=4.62.3; loadts=1747663440335; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=d31e3071-2670-4dec-a7d8-76374e850e33; web_session=0400698fe17032560807db721e3a4b185efee4; unread={%22ub%22:%22682a1ba300000000210097b3%22%2C%22ue%22:%22682a99d0000000002300002a%22%2C%22uc%22:26}"
# COOKIES = "buvid4=5EDF2BBB-77CB-0707-F959-E2615F1DDF8C20576-023012722-BpftfWdbUwTSaxivXiug7Q%3D%3D; buvid_fp_plain=undefined; DedeUserID=381513858; DedeUserID__ckMd5=445a7cd327968e3c; CURRENT_BLACKGAP=0; header_theme_version=CLOSE; enable_web_push=DISABLE; bntyh_content4=2024-8-20; fingerprint=61169110d97a18850155ae5b4445ab63; buvid_fp=61169110d97a18850155ae5b4445ab63; _uuid=53BB7C66-1BAC-7D56-9B43-433ED271D57680040infoc; is-2022-channel=1; CURRENT_QUALITY=64; buvid3=7BB52E30-1519-D094-BCA4-32EBCFE033B262257infoc; b_nut=1741091462; enable_feed_channel=ENABLE; rpdid=|(k||)|kJJlu0J'u~RRYJkRYk; PVID=1; home_feed_column=4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDc4MTUyNzgsImlhdCI6MTc0NzU1NjAxOCwicGx0IjotMX0.ySc5ijVH5uUAPsfbWkhYXZIMdXHiEdeuKo3BdleKT54; bili_ticket_expires=1747815218; bmg_af_switch=1; b_lsid=13CE88101_196E66BEC89; CURRENT_FNVAL=2000; bmg_src_def_domain=i2.hdslb.com; SESSDATA=11bb78f7%2C1763174661%2C4d1fe%2A52CjA3Yyjpz5W3HXYUbAvektDATnRalylqtMaoFkqHd7Btz6tScxTBKMgAfGsHWqqYlIASVkdNVGlKTjRqNHN4MlR6WFBVUi01alRSVFBVYWEwTEdrWDlndUo5cG9TaVp1b2JnUG5KcGVyQVF4SU9BTWZldmVnbE9QU2JyNVV1VWpUTWZqdDV3TGFnIIEC; bili_jct=fabefcbe015df032477ec354a3668d78; sid=6dxjeil6; bp_t_offset_381513858=1068520286229364736; browser_resolution=283-591" # bili
# 具体值参见media_platform.xxx.field下的枚举值，暂时只支持小红书
SORT_TYPE = "popularity_descending"
# 具体值参见media_platform.xxx.field下的枚举值，暂时只支持抖音
PUBLISH_TIME_TYPE = 0
CRAWLER_TYPE = (
    "search"  # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据)
)
# 自定义User Agent（暂时仅对XHS有效）
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

# 是否开启 IP 代理
ENABLE_IP_PROXY = False

# 未启用代理时的最大爬取间隔，单位秒（暂时仅对XHS有效）
CRAWLER_MAX_SLEEP_SEC = 2

# 代理IP池数量
IP_PROXY_POOL_COUNT = 2

# 代理IP提供商名称
IP_PROXY_PROVIDER_NAME = "kuaidaili"

# 设置为True不会打开浏览器（无头浏览器）
# 设置False会打开一个浏览器
# 小红书如果一直扫码登录不通过，打开浏览器手动过一下滑动验证码
# 抖音如果一直提示失败，打开浏览器看下是否扫码登录之后出现了手机号验证，如果出现了手动过一下再试。
HEADLESS = True

# 
STEALTH_PATH = 'crawler/libs/stealth.min.js'

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# 数据保存类型选项配置,支持三种类型：csv、db、json, 最好保存到DB，有排重的功能。
SAVE_DATA_OPTION = "json"  # csv or db or json

# 用户浏览器缓存的浏览器文件配置
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# 爬取开始页数 默认从第一页开始
START_PAGE = 1

# 爬取视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = 1

# 并发爬虫数量控制
MAX_CONCURRENCY_NUM = 1

# 是否开启爬图片模式, 默认不开启爬图片
ENABLE_GET_IMAGES = False

# 是否开启爬评论模式, 默认开启爬评论
ENABLE_GET_COMMENTS = False

# 爬取一级评论的数量控制(单视频/帖子)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 10

# 是否开启爬二级评论模式, 默认不开启爬二级评论
# 老版本项目使用了 db, 则需参考 schema/tables.sql line 287 增加表字段
ENABLE_GET_SUB_COMMENTS = False

# 已废弃⚠️⚠️⚠️指定小红书需要爬虫的笔记ID列表
# 已废弃⚠️⚠️⚠️ 指定笔记ID笔记列表会因为缺少xsec_token和xsec_source参数导致爬取失败
# XHS_SPECIFIED_ID_LIST = [
#     "66fad51c000000001b0224b8",
#     # ........................
# ]

# 指定小红书需要爬虫的笔记URL列表, 目前要携带xsec_token和xsec_source参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    # "https://www.xiaohongshu.com/explore/66fad51c000000001b0224b8?xsec_token=AB3rO-QopW5sgrJ41GwN01WCXh6yWPxjSoFI9D5JIMgKw=&xsec_source=pc_search"
    # ........................
]

# 指定抖音需要爬取的ID列表
DY_SPECIFIED_ID_LIST = [
    # "7280854932641664319",
    # "7202432992642387233",
    # ........................
]

# 指定快手平台需要爬取的ID列表
KS_SPECIFIED_ID_LIST = [
    # "3xf8enb8dbj6uig", "3x6zz972bchmvqe"
]

# 指定B站平台需要爬取的视频bvid列表
BILI_SPECIFIED_ID_LIST = [
    # "BV1d54y1g7db",
    # "BV1Sz4y1U77N",
    # "BV14Q4y1n7jz",
    # ........................
]

# 指定微博平台需要爬取的帖子列表
WEIBO_SPECIFIED_ID_LIST = [
    # "4982041758140155",
    # ........................
]

# 指定weibo创作者ID列表
WEIBO_CREATOR_ID_LIST = [
    # "5533390220",
    # ........................
]

# 指定贴吧需要爬取的帖子列表
TIEBA_SPECIFIED_ID_LIST = []

# 指定贴吧名称列表，爬取该贴吧下的帖子
TIEBA_NAME_LIST = [
    # "盗墓笔记"
]

# 指定贴吧创作者URL列表
TIEBA_CREATOR_URL_LIST = [
    # "https://tieba.baidu.com/home/main/?id=tb.1.7f139e2e.6CyEwxu3VJruH_-QqpCi6g&fr=frs",
    # ........................
]

# 指定小红书创作者ID列表
XHS_CREATOR_ID_LIST = [
    # "63e36c9a000000002703502b",
    # ........................
]

# 指定Dy创作者ID列表(sec_id)
DY_CREATOR_ID_LIST = [
    # "MS4wLjABAAAATJPY7LAlaa5X-c8uNdWkvz0jUGgpw4eeXIwu_8BhvqE",
    # ........................
]

# 指定bili创作者ID列表(sec_id)
BILI_CREATOR_ID_LIST = [
    # "20813884",
    # ........................
]

# 指定快手创作者ID列表
KS_CREATOR_ID_LIST = [
    # "3x4sm73aye7jq7i",
    # ........................
]


# 指定知乎创作者主页url列表
ZHIHU_CREATOR_URL_LIST = [
    # "https://www.zhihu.com/people/yd1234567",
    # ........................
]

# 指定知乎需要爬取的帖子ID列表
ZHIHU_SPECIFIED_ID_LIST = [
    # "https://www.zhihu.com/question/826896610/answer/4885821440", # 回答
    # "https://zhuanlan.zhihu.com/p/673461588", # 文章
    # "https://www.zhihu.com/zvideo/1539542068422144000" # 视频
]

# 词云相关
# 是否开启生成评论词云图
ENABLE_GET_WORDCLOUD = False
# 自定义词语及其分组
# 添加规则：xx:yy 其中xx为自定义添加的词组，yy为将xx该词组分到的组名。
CUSTOM_WORDS = {
    "零几": "年份",  # 将“零几”识别为一个整体
    "高频词": "专业术语",  # 示例自定义词
}

# 停用(禁用)词文件路径
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# 中文字体文件路径
FONT_PATH = "./docs/STZHONGS.TTF"

# 爬取开始的天数，仅支持 bilibili 关键字搜索，YYYY-MM-DD 格式，若为 None 则表示不设置时间范围，按照默认关键字最多返回 1000 条视频的结果处理
START_DAY = '2024-01-01'

# 爬取结束的天数，仅支持 bilibili 关键字搜索，YYYY-MM-DD 格式，若为 None 则表示不设置时间范围，按照默认关键字最多返回 1000 条视频的结果处理
END_DAY = '2024-01-01'

# 是否开启按每一天进行爬取的选项，仅支持 bilibili 关键字搜索
# 若为 False，则忽略 START_DAY 与 END_DAY 设置的值
# 若为 True，则按照 START_DAY 至 END_DAY 按照每一天进行筛选，这样能够突破 1000 条视频的限制，最大程度爬取该关键词下的所有视频
ALL_DAY = False
# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 21:34
# @Desc    :

import re
from typing import List

from var import source_keyword_var

from .weibo_store_image import *
from .weibo_store_impl import *


class WeibostoreFactory:
    STORES = {
        "csv": WeiboCsvStoreImplement,
        "db": WeiboDbStoreImplement,
        "json": WeiboJsonStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = WeibostoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[WeibotoreFactory.create_store] Invalid save option only supported csv or db or json ...")
        return store_class()


async def batch_update_weibo_notes(note_list: List[Dict]):
    """
    Batch update weibo notes
    Args:
        note_list:

    Returns:

    """
    if not note_list:
        return
    for note_item in note_list:
        await update_weibo_note(note_item)


async def update_weibo_note(note_item: Dict, info: Dict):
    """
    Update weibo note
    Args:
        note_item:

    Returns:

    """
    if not note_item:
        return

    mblog: Dict = note_item.get("mblog")
    user_info: Dict = mblog.get("user")
    note_id = mblog.get("id")
    content_text = mblog.get("text")
    clean_text = re.sub(r"<.*?>", "", content_text)
    save_content_item = {
        # 微博信息
        "note_id": note_id,
        "content": clean_text,
        "create_time": utils.rfc2822_to_timestamp(mblog.get("created_at")),
        "create_date_time": str(utils.rfc2822_to_china_datetime(mblog.get("created_at"))),
        "liked_count": str(mblog.get("attitudes_count", 0)),
        "comments_count": str(mblog.get("comments_count", 0)),
        "shared_count": str(mblog.get("reposts_count", 0)),
        "last_modify_ts": utils.get_current_timestamp(),
        "note_url": f"https://m.weibo.cn/detail/{note_id}",
        "ip_location": mblog.get("region_name", "").replace("发布于 ", ""),

        # 用户信息
        "user_id": str(user_info.get("id")),
        "nickname": user_info.get("screen_name", ""),
        "gender": user_info.get("gender", ""),
        "profile_url": user_info.get("profile_url", ""),
        "avatar": user_info.get("profile_image_url", ""),

        "source_keyword": source_keyword_var.get(),
    }
    utils.logger.info(
        f"[store.weibo.update_weibo_note] weibo note id:{note_id}, title:{save_content_item.get('content')[:24]} ...")
    await WeibostoreFactory.create_store().store_content(content_item=save_content_item)
    markdown = f"""### 📝 [{save_content_item['content'][:10]}]({save_content_item['note_url']})

<div>
    {info['mblog']['text']}
</div>
    
```text

**👤 用户：** [{save_content_item['nickname']}]({save_content_item['profile_url']})  
**📅 发布时间：** {save_content_item['create_date_time']}  
**📍 IP归属地：** {save_content_item['ip_location']}  
**🔍 来源关键词：** {save_content_item['source_keyword']}
**👍 点赞：** {save_content_item['liked_count']}  **💬 评论：** {save_content_item['comments_count']}  **🔁 转发：** {save_content_item['shared_count']}
```
"""
    return markdown

async def batch_update_weibo_note_comments(note_id: str, comments: List[Dict]):
    """
    Batch update weibo note comments
    Args:
        note_id:
        comments:

    Returns:

    """
    if not comments:
        return
    for comment_item in comments:
        await update_weibo_note_comment(note_id, comment_item)


async def update_weibo_note_comment(note_id: str, comment_item: Dict):
    """
    Update weibo note comment
    Args:
        note_id: weibo note id
        comment_item: weibo comment item

    Returns:

    """
    if not comment_item or not note_id:
        return
    comment_id = str(comment_item.get("id"))
    user_info: Dict = comment_item.get("user")
    content_text = comment_item.get("text")
    clean_text = re.sub(r"<.*?>", "", content_text)
    save_comment_item = {
        "comment_id": comment_id,
        "create_time": utils.rfc2822_to_timestamp(comment_item.get("created_at")),
        "create_date_time": str(utils.rfc2822_to_china_datetime(comment_item.get("created_at"))),
        "note_id": note_id,
        "content": clean_text,
        "sub_comment_count": str(comment_item.get("total_number", 0)),
        "comment_like_count": str(comment_item.get("like_count", 0)),
        "last_modify_ts": utils.get_current_timestamp(),
        "ip_location": comment_item.get("source", "").replace("来自", ""),
        "parent_comment_id": comment_item.get("rootid", ""),

        # 用户信息
        "user_id": str(user_info.get("id")),
        "nickname": user_info.get("screen_name", ""),
        "gender": user_info.get("gender", ""),
        "profile_url": user_info.get("profile_url", ""),
        "avatar": user_info.get("profile_image_url", ""),
    }
    utils.logger.info(
        f"[store.weibo.update_weibo_note_comment] Weibo note comment: {comment_id}, content: {save_comment_item.get('content', '')[:24]} ...")
    await WeibostoreFactory.create_store().store_comment(comment_item=save_comment_item)


async def update_weibo_note_image(picid: str, pic_content, extension_file_name):
    """
    Save weibo note image to local
    Args:
        picid:
        pic_content:
        extension_file_name:

    Returns:

    """
    await WeiboStoreImage().store_image(
        {"pic_id": picid, "pic_content": pic_content, "extension_file_name": extension_file_name})


async def save_creator(user_id: str, user_info: Dict):
    """
    Save creator information to local
    Args:
        user_id:
        user_info:

    Returns:

    """
    local_db_item = {
        'user_id': user_id,
        'nickname': user_info.get('screen_name'),
        'gender': '女' if user_info.get('gender') == "f" else '男',
        'avatar': user_info.get('avatar_hd'),
        'desc': user_info.get('description'),
        'ip_location': user_info.get("source", "").replace("来自", ""),
        'follows': user_info.get('follow_count', ''),
        'fans': user_info.get('followers_count', ''),
        'tag_list': '',
        "last_modify_ts": utils.get_current_timestamp(),
    }
    utils.logger.info(f"[store.weibo.save_creator] creator:{local_db_item}")
    await WeibostoreFactory.create_store().store_creator(local_db_item)

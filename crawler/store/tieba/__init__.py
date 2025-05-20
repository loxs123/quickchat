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
from typing import List

from model.m_baidu_tieba import TiebaComment, TiebaCreator, TiebaNote
from var import source_keyword_var

from . import tieba_store_impl
from .tieba_store_impl import *


class TieBaStoreFactory:
    STORES = {
        "csv": TieBaCsvStoreImplement,
        "db": TieBaDbStoreImplement,
        "json": TieBaJsonStoreImplement
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = TieBaStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[TieBaStoreFactory.create_store] Invalid save option only supported csv or db or json ...")
        return store_class()


async def batch_update_tieba_notes(note_list: List[TiebaNote]):
    """
    Batch update tieba notes
    Args:
        note_list:

    Returns:

    """
    if not note_list:
        return
    for note_item in note_list:
        await update_tieba_note(note_item)


async def update_tieba_note(note_item: TiebaNote):
    """
    Add or Update tieba note
    Args:
        note_item:

    Returns:

    """
    note_item.source_keyword = source_keyword_var.get()
    save_note_item = note_item.model_dump()
    save_note_item.update({"last_modify_ts": utils.get_current_timestamp()})
    utils.logger.info(f"[store.tieba.update_tieba_note] tieba note: {save_note_item}")

    await TieBaStoreFactory.create_store().store_content(save_note_item)

    markdown = f"""### 📌 [{save_note_item['title']}]({save_note_item['note_url']})
```text
{save_note_item['desc']}

**🔍 来源关键词：** {save_note_item['source_keyword']}
**👤 用户：** [{save_note_item['user_nickname']}]({save_note_item['user_link']})  
**📅 发布时间：** {save_note_item['publish_time']}  
**🏷 所属贴吧：** [{save_note_item['tieba_name']}]({save_note_item['tieba_link']})  
**💬 评论数：** {save_note_item['total_replay_num']}
```
"""
    return markdown



async def batch_update_tieba_note_comments(note_id: str, comments: List[TiebaComment]):
    """
    Batch update tieba note comments
    Args:
        note_id:
        comments:

    Returns:

    """
    if not comments:
        return
    for comment_item in comments:
        await update_tieba_note_comment(note_id, comment_item)


async def update_tieba_note_comment(note_id: str, comment_item: TiebaComment):
    """
    Update tieba note comment
    Args:
        note_id:
        comment_item:

    Returns:

    """
    save_comment_item = comment_item.model_dump()
    save_comment_item.update({"last_modify_ts": utils.get_current_timestamp()})
    utils.logger.info(f"[store.tieba.update_tieba_note_comment] tieba note id: {note_id} comment:{save_comment_item}")
    await TieBaStoreFactory.create_store().store_comment(save_comment_item)


async def save_creator(user_info: TiebaCreator):
    """
    Save creator information to local
    Args:
        user_info:

    Returns:

    """
    local_db_item = user_info.model_dump()
    local_db_item["last_modify_ts"] = utils.get_current_timestamp()
    utils.logger.info(f"[store.tieba.save_creator] creator:{local_db_item}")
    await TieBaStoreFactory.create_store().store_creator(local_db_item)

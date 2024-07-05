import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *
from .quark import QURAK
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any
import time
import logging
from datetime import datetime

@plugins.register(
    name="METASO",
    desire_priority=88,
    hidden=False,
    desc="A plugin to handle quark",
    version="0.1",
    author="小AI",
)
class METASO(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.config = super().load_config()
            logger.info("[METASO] inited")
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        except Exception as e:
            logger.error(f"[METASO]初始化异常：{e}")
            raise "[METASO] init failed, ignore "

    def create_reply(self, reply_type, content):
        reply = Reply()
        reply.type = reply_type
        reply.content = content
        return reply

    def merge_qry_data(self, qry_key: str):
        def fetch_data(method_name: str, qry_key: str) -> Any:
            quark = QURAK()
            method = getattr(quark, method_name, None)
            if method is not None:
                return method(qry_key)
            return None

        logging.info('查询关键字:' + qry_key)
        msg = '【' + qry_key + '】外部资源搜索结果：\n'
        start_time = time.time()

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(fetch_data, method_name, qry_key)
                for method_name in [
                    'qry_kkkob',
                    'get_qry_external',
                    'get_qry_external_2',
                    'get_qry_external_3',
                    'get_qry_external_4',
                    'get_qry_external_5'
                ]
            ]

        # 使用列表推导式来获取每个 Future 的结果
        seen_url = set()
        # 创建一个新的列表来存储去重后的数据
        unique_data = []

        i = 1
        # 遍历合并后的数据，按链接去重
        for future in futures:
            future_data = future.result()
            if future_data is not None:
                for item in future_data:
                    if i > 5:
                        break
                    url = item['url']
                    if url not in seen_url:
                        item['sno'] = i
                        seen_url.add(url)
                        unique_data.append(item)

                        msg += '========== \n'
                        msg += str(item['sno']) + '.' + item['title'] + '\n' + item['url'] + '\n'

                        i += 1
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"查询执行耗时: {execution_time:.6f} seconds")
        logging.info(f"查询结果: {unique_data}")

        return msg

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        content = e_context["context"].content.strip()
        logger.debug("[metaso] on_handle_context. content: %s" % content)

        if content.startswith("外部搜索"):
            keyword = content[4:].strip()  # 提取关键词后面的文字
            search_result = self.merge_qry_data(keyword)
            reply_type = ReplyType.TEXT
            reply = self.create_reply(reply_type, search_result)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return
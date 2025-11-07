from ncatbot.plugin_system import (
    NcatBotPlugin, 
    admin_group_filter, 
    command_registry, 
    option, 
    param
)
from ncatbot.plugin_system.builtin_plugin.unified_registry.command_system.registry.help_system import HelpGenerator
from ncatbot.utils import get_log
from ncatbot.core import GroupMessageEvent, MessageArray, Reply
from typing import Optional
from .utils import require_subscription, require_group_admin, at_check_support

import time

class EssenceManager(NcatBotPlugin):

    name = "EssenceManager"
    version = "1.0.1"
    author = "Sparrived"
    description = "一个用于管理群组精华消息的插件，支持随机播送精华消息，添加/删除精华消息。"

    log = get_log(name)

    def init_config(self):
        self.register_config(
            "list_count",
            "5",
            "每次列出多少条精华消息",
            int
        )

        self.register_config(
            "subscribed_groups",
            ["123456789"],  # 示例群号
            "需要订阅的群组列表",
            list
        )


    # ======== 初始化插件 ========
    async def on_load(self):
        self.init_config()
        self.log.info("GroupManager 插件已加载。")


    # ======== 注册指令 ========
    essence_group = command_registry.group("essence", "群精华消息管理根级命令")

    @admin_group_filter
    @essence_group.command("list", description="列出群内所有群精华消息，支持分页显示。")
    @option("a", "all", help="是否显示所有消息")
    @param("page", default=1, help="页码", required=False)
    @require_subscription
    async def cmd_list(self, event: GroupMessageEvent, all: bool = False, page: int = 1):
        """列出群内所有群精华消息，支持分页显示。"""
        essence_messages = await self.api.get_essence_msg_list(event.group_id)
        if len(essence_messages) == 0:
            await event.reply("本群暂无群精华消息喵，你们怎么不爆典喵？~")
            return
        msg_array = MessageArray()
        show_essences = essence_messages if all else essence_messages[(page-1)*self.config["list_count"]:page*self.config["list_count"]]
        page_count = (len(essence_messages) + self.config["list_count"] - 1) // self.config["list_count"]
        msg_array.add_text(f" 本群共有 {len(essence_messages)} 条群精华消息，{' 显示全部消息喵~' if all else f' 当前显示第 {page} / {page_count} 页喵~'}")
        for essence in show_essences:
            if len(msg_array.messages) != 1:
                msg_array.add_text("\n" + "="*10 + "\n")            
            time_array = time.localtime(essence.operator_time)
            msg_array.add_text(f"\n消息ID: {essence.message_id} | 发送者: {essence.sender_nick}({essence.sender_id}) | 时间: {time.strftime('%Y-%m-%d %H:%M:%S', time_array)}\n内容：\n")
            msg_array.messages.extend(essence.content.messages)
        await event.reply(rtf=msg_array)


    @admin_group_filter
    @essence_group.command("add", description="添加群精华消息")
    @param("mid", help="消息ID", required=False)
    @require_subscription
    @require_group_admin(role="admin", reply_message="我不是管理员，不能设置精华消息喵……")
    async def cmd_add(self, event: GroupMessageEvent, mid: str = ""):
        """添加群精华消息"""
        if not mid:
            reply_msg = event.message.filter(Reply)
            if reply_msg and len(reply_msg) != 0:
                mid = reply_msg[0].id
            else:
                await event.reply("请提供一个消息ID或者回复你想要添加精华的消息喵~")
                return
        elif mid.startswith("Reply("):
            mid = mid.split("=")[1].split('"')[1]
        try:
            await self.api.set_essence_msg(mid)
            await event.reply(f"成功添加了群精华消息喵（偷偷告诉你，消息ID是 {mid} 喵）~")
        except Exception as e:
            await event.reply(f"添加群精华消息失败了喵……\n错误信息：{e}")


    # ======== 订阅功能 ========
    @admin_group_filter
    @essence_group.command("subscribe", description="订阅群组管理功能")
    async def cmd_subscribe(self, event: GroupMessageEvent):
        """订阅群组管理功能"""
        subscribed_groups = self.config["subscribed_groups"]
        if str(event.group_id) in subscribed_groups:
            await event.reply("本群组已订阅群精华消息管理功能喵~")
            return
        self.config["subscribed_groups"].append(str(event.group_id))
        await event.reply("订阅了群精华消息管理功能喵~")


    @admin_group_filter
    @essence_group.command("unsubscribe", description="取消订阅群组管理功能")
    async def cmd_unsubscribe(self, event: GroupMessageEvent):
        """取消订阅群组管理功能"""
        subscribed_groups = self.config["subscribed_groups"]
        if str(event.group_id) not in subscribed_groups:
            await event.reply("本群组未订阅群精华消息管理功能喵~")
            return
        self.config["subscribed_groups"].remove(str(event.group_id))
        await event.reply("取消订阅了群精华消息管理功能喵~")


    @admin_group_filter
    @essence_group.command("help", description="获取群精华消息管理帮助信息")
    @param("command", default="", help="指令名称", required=False)
    @require_subscription
    async def cmd_help(self, event: GroupMessageEvent, command: str = ""):
        """获取群精华消息管理帮助信息"""
        help_message = f"插件版本：{self.version}\n"
        help_generator = HelpGenerator()
        try:
            if not command:
                help_message += help_generator.generate_group_help(self.essence_group)
            else:
                command_obj = self.essence_group.commands.get(command, None)  # type: ignore
                if not command_obj:
                    await event.reply(f"未找到指令 {command} 喵，请确认指令名称是否正确喵~")
                    return
                help_message += help_generator.generate_command_help(command_obj)
            await event.reply(help_message)
        except Exception as e:
            await event.reply(f"生成帮助信息时出错了喵：\n{e}")
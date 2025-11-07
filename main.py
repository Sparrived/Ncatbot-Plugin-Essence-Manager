from ncatbot.plugin_system import (
    NcatBotPlugin, 
    admin_group_filter, 
    command_registry, 
    option, 
    param
)
from ncatbot.plugin_system.builtin_plugin.unified_registry.command_system.registry.help_system import HelpGenerator
from ncatbot.utils import get_log
from ncatbot.core import GroupMessageEvent, MessageArray
from typing import Optional
from .utils import require_subscription, require_group_admin, at_check_support


class EssenceManager(NcatBotPlugin):

    name = "EssenceManager"
    version = "1.0.0"
    author = "Sparrived"
    description = "一个用于管理群组精华消息的插件，支持随机播送精华消息，添加/删除精华消息。"

    log = get_log(name)

    def init_config(self):
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
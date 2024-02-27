class RoleEventCallback:
    """各种event listener需要用到的callback，启用的方式是self.call"""

    def __init__(self, callback_func, description_func, display_func=None) -> None:
        """
        - callback_func : 函数接受caster_quid,target_quid,Battle,context(dict),**kwargs(cast的参数)作为参数，返回bool表示是否删除这个listener
        - description_func : 接受context，返回字符串

        可能是被动技能或者buff导致的
        每次在成为caster或者target时，会依次过一遍listener[operation]
        同时数值被减少时也会过一遍listener[某个数值]
        另外还有还有role个人的turn start, turn end，全局的g_turn_start, g_turn_end
        因为不像星穹铁道那样是更即时的插队制
        """
        self.callback_func = callback_func
        self.display_func = display_func
        self.description_func = description_func

        self.context = dict()
        pass

    def call(self, caster_quid, target_quid, Battle, **kwargs):
        if self.display_func is not None:
            self.display_func()
        return self.callback_func(
            caster_quid, target_quid, Battle, self.context, **kwargs
        )

    def get_description(self):
        self.description_func(self.context)


class RoleValueCallback:
    """各种value listener需要用到的callback，启用的方式是self.call"""

    def __init__(self, callback_func, description_func, display_func=None) -> None:
        """
        - callback : 函数接受target_quid,original_value,result_value,Battle,context(dict),**kwargs(cast的参数)作为参数，
                    返回bool表示是否删除这个listener

        数值被修改时会过一遍listener[某种数值]
        """

        self.callback_func = callback_func
        self.display_func = display_func
        self.description_func = description_func
        self.context = dict()
        pass

    def call(self, target_quid, original_value, result_value, Battle, **kwargs):
        if self.display_func is not None:
            self.display_func()
        return self.callback_func(
            target_quid, original_value, result_value, Battle, self.context, **kwargs
        )

    def get_description(self):
        self.description_func(self.context)


class GlobalEventCallback:
    """各种全局事件 listener需要用到的callback，启用的方式是self.call"""

    def __init__(self, callback_func, description_func, display_func=None) -> None:
        """
        - callback : 函数接受Battle,context(dict),**kwargs(cast的参数)作为参数，
                    返回bool表示是否删除这个listener

        数值被修改时会过一遍listener[某种数值]
        """
        self.callback_func = callback_func
        self.display_func = display_func
        self.description_func = description_func
        self.context = dict()
        pass

    def call(self, Battle, **kwargs):
        if self.display_func is not None:
            self.display_func()
        return self.callback_func(Battle, self.context, **kwargs)

    def get_description(self):
        self.description_func(self.context)

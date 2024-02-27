from src.model.battle.skill import Skill
from src.model.battle.item import Item
from src.model.battle.battle_role import BattleRole
from src.model.battle.event_callback import GlobalEventCallback

from src.constant.battle.enum_event import EnumBattleEvent, reverse_event
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.constant.battle.enum_role_value import EnumRoleValue
from src.utils.modify_calculate import modify_calculate


class Battle:
    def __init__(
        self,
        player1_info_list: list[BattleRole],
        player2_info_list: list[BattleRole],
        player1_position: list[int],
        player2_position: list[int],
        skill_dict: dict[int, Skill],
        item_dict: dict[int, tuple[Item, int]],
    ) -> None:
        """
        - *_position: int=quid list, [0,10) player1, [10,20) player2.数字表示站位0-4最左上.15-19最右下

        """
        self.skill_dict = skill_dict
        self.item_dict: dict[int, Item] = {}
        self.item_number_dict: dict[int, int] = {}
        for key, (first, second) in item_dict.items():
            self.item_dict[key] = first
            self.item_number_dict[key] = second

        self.layout: dict[int, BattleRole] = {}
        idx = 0
        for idx in range(len(player1_position)):
            self.layout[player1_position[idx]] = player1_info_list[idx]
        idx = 0
        for idx in range(len(player2_position)):
            self.layout[player2_position[idx]] = player2_info_list[idx]

        self.global_listener: dict[EnumBattleEvent, list[GlobalEventCallback]] = {}

        # 可用的按键
        # 在每个role的回合中的event，发送可以按动的按钮给viewer
        ## player 1
        ## player 2
        pass

    # 出招
    def cast(
        self,
        caster_quid,
        target_quid,
        castable_id,
        operation_type: EnumBattleEvent,
        **kwargs,
    ):
        """处理任何时候释放一些招式到skill cast func
        - caster, target : battle生成的quid
        """
        # 根据type和kwargs得到技能的id
        caster_role = self.layout[caster_quid]
        target_role = self.layout[target_quid]

        # skillId = caster_role.operation_dict[operation_type][kwargs.get("idx", 0)]
        if operation_type != EnumBattleEvent.ENUM_ON_ITEM:
            castable_item = self.skill_dict[castable_id]
        else:
            castable_item = self.item_dict[castable_id]
            # 进行消耗
            ...
        castable_item.cast(caster_quid, target_quid, self)

        # caster 和 target的一些相关event listener触发
        listener = caster_role.role_event_listener.get(operation_type, [])
        new_listener = []
        for listener_callback in listener:
            del_flag = listener_callback.call(caster_quid, target_quid, self, **kwargs)
            if del_flag is False:
                new_listener.append(listener_callback)
        if len(new_listener) == 0:
            caster_role.role_event_listener.pop(operation_type)
        else:
            caster_role.role_event_listener[operation_type] = new_listener

        reversed_operation_type = reverse_event(operation_type)
        listener = target_role.role_event_listener.get(reversed_operation_type, [])
        new_listener = []
        for listener_callback in listener:
            del_flag = listener_callback.call(caster_quid, target_quid, self, **kwargs)
            if del_flag is False:
                new_listener.append(listener_callback)
        if len(new_listener) == 0:
            target_role.role_event_listener.pop(reversed_operation_type)
        else:
            target_role.role_event_listener[reversed_operation_type] = new_listener

    # 场上信息
    ## 修改
    def modify_role_value(
        self,
        target_quid,
        offset,
        value_type: EnumRoleValue,
        calculate: EnumModifyCalculate,
        **kwargs,
    ):
        # 底层的修改状态，在这之前需要经过伤害计算公式
        target_role = self.layout[target_quid]
        origin_value = target_role.value_dict.get(value_type, None)
        if origin_value is not None:
            result_value = modify_calculate(origin_value, offset, calculate)
            target_role.set_value(value_type, result_value)

            listener = target_role.role_value_listener.get(value_type, [])
            new_listener = []
            for listener_callback in listener:
                del_flag = listener_callback.call(
                    target_quid, origin_value, result_value, self, **kwargs
                )
                if del_flag is False:
                    new_listener.append(listener_callback)
            if len(new_listener) == 0:
                target_role.role_value_listener.pop(value_type)
            else:
                target_role.role_value_listener[value_type] = new_listener

    # def query_quid_value(self, quid: int, value_name: str):
    #     """被battle_role.query替代"""
    #     return self.layout[quid].query_current_value(EnumRoleValue.ENUM_ATTACK)

    def add_global_event_listener(
        self, event_type: EnumBattleEvent, callback: GlobalEventCallback
    ):
        listener = self.global_listener.get(event_type, [])
        listener.append(callback)
        self.global_listener[event_type] = listener

    # 选择阶段
    ## 初始化当前回合
    def on_ready_turn_start(self):
        # (caster_quid, skill_id, target_quid)
        self.quid_skill_and_item: list[tuple[int, int, EnumBattleEvent, int]] = []
        # self.quid_item: list[tuple[int, int, int]] = []

    ## select skill/item scroll + select target阶段
    def cancel_by_caster_quid(self, caster_quid):
        """撤销用"""
        self.quid_skill_and_item = [
            t for t in self.quid_skill_and_item if t[0] != caster_quid
        ]
        # self.quid_item = [t for t in self.quid_item if t[0] != caster_quid]

    def ready_skill_by_skillId(
        self, caster_quid, target_quid, skill_id, operation_type: EnumBattleEvent
    ):
        self.quid_skill_and_item.append(
            (caster_quid, skill_id, operation_type, target_quid)
        )

    def ready_skill_by_operation(self, caster_quid, target_quid, operation):
        """针对玩家的operation
        - 1: Attack <
        - 2: Spell[0] ^
        - 3: Spell[1] v
        - 4: Defense >
        - 5: Final Spell
        """
        operation = EnumBattleEvent.ENUM_NULL
        t_skill_id = 0
        match operation:
            case 1:
                t_skill_id = self.layout[caster_quid].operation_dict[
                    EnumBattleEvent.ENUM_ON_ATTACK
                ][0]
                operation = EnumBattleEvent.ENUM_ON_ATTACK
            case 2:
                t_skill_id = self.layout[caster_quid].operation_dict[
                    EnumBattleEvent.ENUM_ON_SPELL
                ][0]
                operation = EnumBattleEvent.ENUM_ON_SPELL
            case 3:
                t_skill_id = self.layout[caster_quid].operation_dict[
                    EnumBattleEvent.ENUM_ON_SPELL
                ][1]
                operation = EnumBattleEvent.ENUM_ON_SPELL

            case 4:
                t_skill_id = self.layout[caster_quid].operation_dict[
                    EnumBattleEvent.ENUM_ON_DEFENSE
                ][0]
                operation = EnumBattleEvent.ENUM_ON_DEFENSE
            case 5:
                t_skill_id = self.layout[caster_quid].operation_dict[
                    EnumBattleEvent.ENUM_ON_FINAL
                ][0]
                operation = EnumBattleEvent.ENUM_ON_FINAL

        self.ready_skill_by_skillId(caster_quid, target_quid, t_skill_id, operation)

    def ready_item_by_itemId(self, caster_quid, target_quid, item_id):
        self.quid_skill_and_item.append(
            (caster_quid, item_id, EnumBattleEvent.ENUM_ON_ITEM, target_quid)
        )

    def ready_item_by_pack_quid(self, caster_quid, target_quid, pack_quid): ...

    # enum_event
    def battle_start(self): ...
    def battle_end(self): ...
    def turn_start(self, caster_quid): ...
    def turn_end(self, caster_quid): ...
    def global_turn_start(self):
        self.cast_ele_generator = self.get_role_cast_generator()

    def global_turn_end(self): ...

    ## 查询
    ### 属性查询
    def get_speed_queue(self):
        """根据当前角色的速度从大到小排序，无视是否存活"""
        return sorted(
            self.layout,
            key=lambda x: self.layout[x].value_dict.get(EnumRoleValue.ENUM_SPEED) or 0,
            reverse=True,
        )

    def is_dead(self, quid):
        return (
            self.layout[quid].query_current_value(EnumRoleValue.ENUM_HEALTH) or -1
        ) <= 0

    #### 事件查询
    def get_role_cast_generator(self):
        self.queue_cast()
        for (
            caster_quid,
            castable_id,
            operation_type,
            target_quid,
        ) in self.quid_skill_and_item:
            if self.is_dead(caster_quid):
                continue
            # 释放法术
            ## 如果target已经死亡，则效果转移给任何一个target同阵营的目标
            flag = False
            while self.is_dead(target_quid):
                if target_quid < 10:
                    if flag:
                        target_quid += 1
                    else:
                        flag = True
                        target_quid = 0
                else:
                    if flag:
                        target_quid += 1
                    else:
                        flag = True
                        target_quid = 10

            # 计算时间
            speed_delta = (
                self.layout[caster_quid].query_current_value(
                    EnumRoleValue.ENUM_ATTACK_SPEED
                )
                or 0
            ) - (
                self.layout[target_quid].query_current_value(
                    EnumRoleValue.ENUM_DEFENSE_SPEED
                )
                or 0
            )
            if speed_delta < 0:  # 防御更快
                mov_time = 0.4 - 0.03 * max(-20, speed_delta)
            else:
                mov_time = 0.4 - 0.015 * min(20, speed_delta)

            yield caster_quid, target_quid, castable_id, operation_type, mov_time
        ...

    def get_role_cast(self):
        """生成器函数，按照速度顺序生成这个回合的出招信息
        客户端需要使用battle.cast()，进行结算，是否防御成功将体现在battle_role.context中
        :return
        |description  |type   |
        |:---:|:---:|
        |caster_quid   |int   |
        |target_quid   |int   |
        |castable_id   |int   |
        |事件   |EnumBattleEvent   |
        |React time   |float   |
        """
        try:
            ret = next(self.cast_ele_generator)
        except StopIteration:
            return None
        else:
            return ret

    ### 技能查询
    def get_role_skills(self, quid) -> list[Skill]:
        """查询一个角色的所有技能，默认顺序attack->defense->spell->final spell"""
        ret = []

        def load_tlist(t_list):
            for t in t_list:
                ret.append(self.skill_dict[t])

        t_list = self.layout[quid].operation_dict.get(EnumBattleEvent.ENUM_ON_ATTACK)
        if t_list is not None:
            load_tlist(t_list)
        t_list = self.layout[quid].operation_dict.get(EnumBattleEvent.ENUM_ON_DEFENSE)
        if t_list is not None:
            load_tlist(t_list)
        t_list = self.layout[quid].operation_dict.get(EnumBattleEvent.ENUM_ON_SPELL)
        if t_list is not None:
            load_tlist(t_list)
        t_list = self.layout[quid].operation_dict.get(EnumBattleEvent.ENUM_ON_FINAL)
        if t_list is not None:
            load_tlist(t_list)

        return ret

    ### 全局信息查询
    def judge_battle_end(self):
        """游戏是否结束
        :return `int`
        - 0: 没有
        - 1: player1
        - 2: player2(右下)
        """

        flag = True
        tmp = 0
        while flag and tmp < 10:
            flag &= self.is_dead(tmp)
        if flag:
            return 2
        flag = True
        while flag and tmp < 20:
            flag &= self.is_dead(tmp)
        if flag:
            return 1
        return 0

    def query_state(self): ...

    ## 其他
    def queue_cast(self):
        """排序:整合释放技能/道具顺序"""
        self.quid_skill_and_item = sorted(
            self.quid_skill_and_item,
            key=lambda x: self.layout[x[0]].query_current_value(
                EnumRoleValue.ENUM_SPEED
            )
            or 0,
            reverse=True,
        )

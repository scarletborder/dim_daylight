from src.constant.battle.enum_party import EnumParty
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.battle.enum_role_value import EnumRoleValue
from src.model.battle.event_callback import RoleEventCallback, RoleValueCallback


class BattleRole:
    """
    Inherited by BattleRoleHero and BattleRoleMob
    """

    operations_in_turn = []
    operations_out_turn = []

    def __init__(
        self,
        role_id,  # 标识人物资源的唯一标识
        name: str,
        description: str,
        weakness: list[int],  # like [0,4,0,6] , sum = 10, each one is integer
        party: EnumParty,
        # 技能
        # {"ATTACK":[id1,id2,],"SPELL":[id4,]}
        # 如果cast的kwargs包含"idx",释放[idx]个，否则[0]
        operation_dict: dict[EnumBattleEvent, list[int]],
        # 属性
        value_content_dict: dict[EnumRoleValue, int | None],
        # 其他基础属性
    ) -> None:
        self.role_id = role_id
        self.name = name
        self.description = description
        self.weakness: list[int] = weakness
        self.party = party

        # skill
        self.operation_dict = operation_dict

        # value
        ## some default value
        self.default_value_dict = value_content_dict
        ## current value
        self.value_dict: dict[EnumRoleValue, int | None] = value_content_dict.copy()

        self.buff_ids: dict[int, int] = {}  # id - duration

        # event listener
        self.role_event_listener: dict[EnumBattleEvent, list[RoleEventCallback]] = {}
        self.role_value_listener: dict[EnumRoleValue, list[RoleValueCallback]] = {}

        self.is_defense = False
        self.context: dict = dict()  # str - any，场上附加的所有额外信息
        pass

    # cast
    def cast_active_defense(self):
        self.is_defense = True

    def cancel_active_defense(self):
        self.is_defense = False

    # high interface
    def query_default_value(self, key: EnumRoleValue):
        return self.default_value_dict.get(key)

    def query_current_value(self, key: EnumRoleValue):
        return self.value_dict.get(key)

    def is_dead(self):
        return (self.query_current_value(EnumRoleValue.ENUM_HEALTH) or -1) <= 0

    # low interface
    def set_value(self, value_type: EnumRoleValue, result):
        self.value_dict[value_type] = result

    def add_role_event_listener(
        self, event: EnumBattleEvent, callback: RoleEventCallback
    ):
        listener = self.role_event_listener.get(event, [])
        listener.append(callback)
        self.role_event_listener[event] = listener
        return

    def add_role_value_listener(
        self, value_type: EnumRoleValue, callback: RoleValueCallback
    ):
        listener = self.role_value_listener.get(value_type, [])
        listener.append(callback)
        self.role_value_listener[value_type] = listener
        return

        # def recv_operation(

    #     self,
    #     caster,
    #     operation_type: EnumOperation,
    #     extra_type: int,
    #     context: BattleContext,
    # ): ...

    # query

    # @DeprecationWarning
    # def is_alive(self):
    #     """以血量大于0决定是否存活"""
    #     return (self.query_current_value(EnumRoleValue.ENUM_HEALTH) or 0) > 0

    def is_affected_by_specified_buff(self, buff_id):
        return buff_id in self.buff_ids.keys()

    def is_in_my_turn(self, battle_party: EnumParty):
        return battle_party == self.party

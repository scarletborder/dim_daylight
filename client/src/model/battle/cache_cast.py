from src.constant.battle.enum_event import EnumBattleEvent


class CacheCast:
    def __init__(self) -> None:
        self.caster_quid = self.end_time = self.target_quid = self.castable_id = 0

        self.operation_type = EnumBattleEvent.ENUM_NULL
        self.has_casted_flag = False
        pass

    def reset(
        self, caster_quid, target_quid, operation_type: EnumBattleEvent, castable_id
    ):
        self.caster_quid = caster_quid
        self.target_quid = target_quid
        self.operation_type = operation_type
        self.castable_id = castable_id
        self.has_casted_flag = False

    def get(self):
        """
        company with battle.cast()
        """
        self.has_casted_flag = True
        return self.caster_quid, self.target_quid, self.castable_id, self.operation_type

    def has_casted(self):
        """
        是否已经计算过效果，防止由于外部限制多次计算效果
        """
        return self.has_casted_flag
        ...

    def start_event(self, current_caster_quid):
        self.current_caster_quid = current_caster_quid
        ...

    def current_event_caster(self):
        return self.current_caster_quid

    def current_event_casted(self):
        """目标的释放法术结束了"""

    def has_current_event_casted(self): ...

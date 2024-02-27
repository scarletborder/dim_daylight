from enum import IntEnum


class EnumBattleEvent(IntEnum):
    """释放xx或者被xx"""

    ENUM_NULL = 0x0000

    ENUM_ON_ATTACK = 0x0001
    ENUM_ON_SPELL = 0x0002
    ENUM_ON_DEFENSE = 0x0004
    ENUM_ON_ITEM = 0x0008
    ENUM_ON_FINAL = 0x0010
    ENUM_ON_QDEF = 0x0020

    ENUM_BE_ATTACK = 0x1001
    ENUM_BE_SPELL = 0x1002
    ENUM_BE_DEFENSE = 0x1004
    ENUM_BE_ITEM = 0x1008
    ENUM_BE_FINAL = 0x1010
    ENUM_BE_QDEF = 0x1020

    ENUM_ON_VALUECHANGE = 0x2001

    ENUM_TURN_START = 0x0040
    ENUM_TURN_END = 0x0080
    ENUM_GLOBAL_TURN_START = 0x1040
    ENUM_GLOBAL_TURN_END = 0x1080

    ENUM_BATTLE_START = 0x2001
    ENUM_BATTLE_END = 0x2002


def reverse_event(e: EnumBattleEvent):
    match e:
        case EnumBattleEvent.ENUM_ON_ATTACK:
            return EnumBattleEvent.ENUM_BE_ATTACK
        case EnumBattleEvent.ENUM_ON_SPELL:
            return EnumBattleEvent.ENUM_BE_SPELL
        case EnumBattleEvent.ENUM_ON_DEFENSE:
            return EnumBattleEvent.ENUM_BE_DEFENSE
        case EnumBattleEvent.ENUM_ON_ITEM:
            return EnumBattleEvent.ENUM_BE_ITEM
        case EnumBattleEvent.ENUM_ON_FINAL:
            return EnumBattleEvent.ENUM_BE_FINAL
        case EnumBattleEvent.ENUM_ON_QDEF:
            return EnumBattleEvent.ENUM_BE_QDEF

        case EnumBattleEvent.ENUM_BE_ATTACK:
            return EnumBattleEvent.ENUM_ON_ATTACK
        case EnumBattleEvent.ENUM_BE_SPELL:
            return EnumBattleEvent.ENUM_ON_SPELL
        case EnumBattleEvent.ENUM_BE_DEFENSE:
            return EnumBattleEvent.ENUM_ON_DEFENSE
        case EnumBattleEvent.ENUM_BE_ITEM:
            return EnumBattleEvent.ENUM_ON_ITEM
        case EnumBattleEvent.ENUM_BE_FINAL:
            return EnumBattleEvent.ENUM_ON_FINAL
        case EnumBattleEvent.ENUM_BE_QDEF:
            return EnumBattleEvent.ENUM_ON_QDEF

    return EnumBattleEvent.ENUM_NULL


def enum_event_to_str(e: EnumBattleEvent, is_short: bool = True):
    if is_short is True:
        match e:
            case EnumBattleEvent.ENUM_ON_ATTACK:
                return "ATTACK"
            case EnumBattleEvent.ENUM_ON_SPELL:
                return "SPELL"
            case EnumBattleEvent.ENUM_ON_DEFENSE:
                return "DEFENSE"
            case EnumBattleEvent.ENUM_ON_ITEM:
                return "ITEM"
            case EnumBattleEvent.ENUM_ON_FINAL:
                return "FINAL"
            case EnumBattleEvent.ENUM_ON_QDEF:
                return "QDEF"

            case EnumBattleEvent.ENUM_BE_ATTACK:
                return "ATTACK"
            case EnumBattleEvent.ENUM_BE_SPELL:
                return "SPELL"
            case EnumBattleEvent.ENUM_BE_DEFENSE:
                return "DEFENSE"
            case EnumBattleEvent.ENUM_BE_ITEM:
                return "ITEM"
            case EnumBattleEvent.ENUM_BE_FINAL:
                return "FINAL"
            case EnumBattleEvent.ENUM_BE_QDEF:
                return "QDEF"
    if is_short is False:
        match e:
            case EnumBattleEvent.ENUM_ON_ATTACK:
                return "ON_ATTACK"
            case EnumBattleEvent.ENUM_ON_SPELL:
                return "ON_SPELL"
            case EnumBattleEvent.ENUM_ON_DEFENSE:
                return "ON_DEFENSE"
            case EnumBattleEvent.ENUM_ON_ITEM:
                return "ON_ITEM"
            case EnumBattleEvent.ENUM_ON_FINAL:
                return "ON_FINAL"
            case EnumBattleEvent.ENUM_ON_QDEF:
                return "ON_QDEF"

            case EnumBattleEvent.ENUM_BE_ATTACK:
                return "BE_ATTACK"
            case EnumBattleEvent.ENUM_BE_SPELL:
                return "BE_SPELL"
            case EnumBattleEvent.ENUM_BE_DEFENSE:
                return "BE_DEFENSE"
            case EnumBattleEvent.ENUM_BE_ITEM:
                return "BE_ITEM"
            case EnumBattleEvent.ENUM_BE_FINAL:
                return "BE_FINAL"
            case EnumBattleEvent.ENUM_BE_QDEF:
                return "BE_QDEF"

    return EnumBattleEvent.ENUM_NULL

from src.constant.enum_modify_calculate import EnumModifyCalculate


def modify_calculate(origin, offset, flag: EnumModifyCalculate):
    offset = round(offset)
    match flag:
        case EnumModifyCalculate.ENUM_ADD:
            return round(origin + offset)
        case EnumModifyCalculate.ENUM_DEC:
            return round(origin - offset)
        case EnumModifyCalculate.ENUM_MUL:
            return round(origin * offset)
        case EnumModifyCalculate.ENUM_DIV:
            return round(origin / offset)
        case EnumModifyCalculate.ENUM_SET:
            return offset

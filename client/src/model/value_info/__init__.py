"""从远端返回的json文本中解析得到的最顶层value_info"""

"""目前支持的最顶层value  
从json中的type中得知是以下的一种后再到各自的类中解析自己的所有成员
1. 当前地图(地理)信息- localmap_value_info
2. 全局地图信息- globalmap_value_info
3. 怪物信息- role_mob_value_info(role中有技能表)
4. 人物信息- role_hero_value_info(role中有培养方案)
5. 技能信息- skill_value_info
6. 道具信息- item_value_info
7. 地图事件信息- event_value_info

技能表中不存放实际的技能描述而只有id，通过id在本地存储寻找，miss再网络请求
"""

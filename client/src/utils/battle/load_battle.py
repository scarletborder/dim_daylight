"""加载战场"""

from src.model.battle.battle_role import BattleRole
from src.model.battle.battle import Battle
from src.model.battle.skill import Skill


from src.constant.battle.enum_party import EnumParty

from src.storage.main_db import Main_DB
from src.utils.battle.ai_turn_run import Ai_
import sys


class LoadBattle:
    @staticmethod
    def load_battle_ai(gang_id: int, hero_id: int):
        """between player and ai"""
        """测试关卡模拟加载遇怪"""
        """
        player2 -> hero 右下方
        player1 -> mob gang 左上方
        """
        skill_id_list = []
        test_mob_gang1_dict = Main_DB.read_all_values("mob_gang_table", gang_id, {})
        if test_mob_gang1_dict is None:
            sys.exit()

        test_mob_gang1_id_list = test_mob_gang1_dict.get("mob_id_list", [])
        test_mob_gang1_quid_list = test_mob_gang1_dict.get("quid_list", [])

        mob_info_list = []
        handle_basic_content_func = test_mob_gang1_dict.get("handle_basic_content_func")
        for idx in range(len(test_mob_gang1_id_list)):
            role_id = test_mob_gang1_id_list[idx]
            role_info = Main_DB.read_all_values("role_table", role_id, {})
            handle_basic_content_func(role_id, role_info)

            for t_skill_id_list in role_info.get("operation_dict").values():
                skill_id_list += t_skill_id_list

            mob_info_list.append(
                BattleRole(
                    role_id,
                    role_info.get("name"),
                    role_info.get("description"),
                    role_info.get("weakness"),
                    EnumParty.ENUM_PLAYER2,
                    role_info.get("operation_dict"),
                    role_info.get("value_content"),
                )
            )

        """模拟加载英雄
        这里现在只测试一个英雄
        """

        hero_role_id = 0
        hero_role_info = Main_DB.read_all_values("role_table", hero_role_id, {})
        hero_info_list = [
            BattleRole(
                hero_role_id,
                hero_role_info.get("name"),
                hero_role_info.get("description"),
                [0, 0, 0, 0],
                EnumParty.ENUM_PLAYER1,
                hero_role_info.get("operation_dict"),
                hero_role_info.get("value_content"),
            )
        ]

        for t_skill_id_list in hero_role_info.get("operation_dict").values():
            skill_id_list += t_skill_id_list

        """加载技能"""
        skill_id_dict = {}
        for skill_id in skill_id_list:
            if skill_id in skill_id_dict:
                continue
            res = Main_DB.read_all_values("skill_table", skill_id, {})
            skill_id_dict[skill_id] = Skill(
                res.get("name"),
                res.get("description"),
                res.get("cast_func"),
                res.get("display_func"),
                res.get("range_method"),
            )

        test_mob_gang1_quid_list = [0, 1]
        """加载战斗模块"""
        return Battle(
            player1_info_list=mob_info_list,
            player1_position=test_mob_gang1_quid_list,
            player2_info_list=hero_info_list,
            player2_position=[10],
            skill_dict=skill_id_dict,
            item_dict={},
            sync_tool=Ai_,
        )

    @staticmethod
    def load_battle_player():
        """between two players"""

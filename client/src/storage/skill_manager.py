import importlib
import sys


class SkillManager:
    def __init__(self):
        self.loaded_skills = {}

    def load_skill(self, skill_id):
        """动态加载技能模块"""
        if skill_id not in self.loaded_skills:
            module_name = f"skills.{skill_id}"
            try:
                # 动态导入技能模块
                module = importlib.import_module(module_name)
                self.loaded_skills[skill_id] = module
                print(f"技能 {skill_id} 加载成功。")
                return module
            except ImportError:
                print(f"技能 {skill_id} 加载失败。")
                return None
        else:
            return self.loaded_skills[skill_id]

    def unload_skill(self, skill_id):
        """从内存中卸载技能模块"""
        if skill_id in self.loaded_skills:
            # 删除模块引用，允许Python垃圾回收器回收资源
            del sys.modules[self.loaded_skills[skill_id].__name__]
            del self.loaded_skills[skill_id]
            print(f"技能 {skill_id} 已卸载。")

    def unload_all_skills(self):
        """卸载所有技能模块"""
        for skill_id in list(self.loaded_skills.keys()):
            self.unload_skill(skill_id)


# 示例使用
skill_manager = SkillManager()
skill_module = skill_manager.load_skill(
    "fireball"
)  # 假设有一个名为 fireball 的技能模块
# 使用技能...
# 战斗结束，卸载所有技能
skill_manager.unload_all_skills()

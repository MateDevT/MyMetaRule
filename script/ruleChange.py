#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: MyMetaRule
# @File: ruleChange.py
# @IDE: PyCharm
# @Author: TT
# @Date: 2025/7/12 15:28
import logging
from pathlib import Path


class RuleChange:
    def __init__(self, mihomoRulePath, singRulePath, geositePath, geoipPath):
        self.mihomoRulePath = mihomoRulePath
        self.singRulePath = singRulePath
        self.geositePath = geositePath
        self.geoipPath = geoipPath

    def to_mihomo_yaml(self, file_path):
        logging.info(f"开始执行：{file_path}to mihomo yaml")
        fp = Path(*[p for p in file_path.parts if p != '..'])
        new_path = Path(self.mihomoRulePath / fp)
        new_path_folder = new_path.parent
        if not new_path_folder.exists():
            logging.info(f"创建文件夹：{new_path_folder}")
            new_path_folder.mkdir(parents=True, exist_ok=True)

        yaml_path = new_path.with_suffix('.yaml')

        with open(file_path, 'r') as f1:
            lines = [line.strip() for line in f1 if line.strip()]

        with open(yaml_path, 'w', encoding='utf-8') as f2:
            f2.write("payload:\n")  # 写入 YAML 的顶级键 'payload:'
            for line in lines:
                f2.write(f"  - {line}\n")

    def to_sing_json(self, file_path):
        logging.info(f"开始执行：{file_path}to sing json")

    def run(self):
        logging.info(self.mihomoRulePath)
        logging.info(self.singRulePath)
        # for path in [self.geositePath, self.geoipPath]:
        for path in [self.geositePath]:
            p = Path(path)
            for file_path in p.rglob('*'):
                if file_path.is_file():
                    logging.info(f"文件：{file_path}")
                    self.to_mihomo_yaml(file_path)
                    # self.to_sing_json(file_path)
                else:
                    logging.info(f"文件夹：{file_path}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    mihomo_rule_path = '../config/mihomo/rule'
    sing_rule_path = '../config/singBox/rule'
    geosite_path = '../geosite'
    geoip_path = '../geoip'

    rule_change = RuleChange(mihomo_rule_path, sing_rule_path, geosite_path, geoip_path)
    rule_change.run()

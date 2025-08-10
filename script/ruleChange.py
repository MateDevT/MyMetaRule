#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: MyMetaRule
# @File: ruleChange.py
# @IDE: PyCharm
# @Author: TT
# @Date: 2025/7/12 15:28

import logging
from pathlib import Path
from typing import overload


class RuleChange:

    def __init__(self):
        self.mihomoRulePath = None
        self.singRulePath = None
        self.geositePath = None
        self.geoipPath = None
        self.toMihomo = False
        self.toSing = False

    @overload
    def set_path_info(self, mihomoRulePath: str, singRulePath: str, geositePath: str, geoipPath: str,
                      toMihomo: bool = False, toSing: bool = False,
                      **kwargs) -> None:
        ...

    def set_path_info(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_mihomo_yaml(self, file_path):
        logging.info(f"开始执行：{file_path}to mihomo yaml")
        fp = Path(*[p for p in file_path.parts if p != '..'])
        new_path = Path(self.mihomoRulePath / fp)
        new_path_folder = new_path.parent
        if not new_path_folder.exists():
            logging.info(f"create folder {new_path_folder}")
            new_path_folder.mkdir(parents=True, exist_ok=True)

        yaml_path = new_path.with_suffix('.yaml')

        with open(file_path, 'r') as f1:
            lines = [line.strip() for line in f1 if line.strip()]

        with open(yaml_path, 'w', encoding='utf-8') as f2:
            f2.write("payload:\n")  # 写入 YAML 的顶级键 'payload:'
            for line in lines:
                f2.write(f"  - {line}\n")

    def run(self):
        for rulePath in [self.geositePath, self.geoipPath]:
            if rulePath is None:
                logging.warning(f"path:{rulePath} is None, skip.")
                continue
            elif not Path(rulePath).exists():
                raise ValueError(f"{rulePath} : The path does not exist. Please check...")
            p = Path(rulePath)
            for file_path in p.rglob('*'):
                if file_path.is_file():
                    logging.info(f"start file：{file_path}")
                    if self.toMihomo:
                        self.to_mihomo_yaml(file_path)
                else:
                    logging.info(f"{file_path} is folder")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    mihomo_rule_path = '../mihomo/rule'
    sing_rule_path = '../singBox/rule'
    geosite_path = '../rule/geosite'
    geoip_path = '../rule/geoip'

    rule_change = RuleChange()
    rule_change.set_path_info(mihomoRulePath=mihomo_rule_path,
                              singRulePath=sing_rule_path,
                              geositePath=geosite_path,
                              geoipPath=geoip_path,
                              toMihomo=True)
    rule_change.run()

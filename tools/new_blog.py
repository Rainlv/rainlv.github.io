#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse
import os
from datetime import datetime

def arg_parser():
  parser  = argparse.ArgumentParser()
  parser.add_argument("title")
  parser.add_argument("--save_path", "-o", default="_posts")
  return parser

def new_md(title: str, save_path: str):
  FULL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S +0800'
  title_time_fmt = "%Y-%m-%d"
  time_ymd_str = datetime.now().strftime(title_time_fmt)
  full_time_str = datetime.now().strftime(FULL_TIME_FORMAT)
  save_file_name = os.path.join(save_path, time_ymd_str + f"-{title}.md")
  if os.path.exists(save_file_name):
    while(1):
      confirm = input("存在同名文件，是否覆盖(y/n):").lower()
      if confirm in ["n", "no"] :
        return
      elif confirm in ["y", "yes"]:
        break
      else:
        print('请输入" y 或 s "!')

  with open(save_file_name, 'w', encoding='utf8') as fw:
    fw.write(f"""---
title: {title}
date: {full_time_str}
---""")
    print(f"{os.path.abspath(save_file_name)} Successfully Generated!") 
    return True

def main():
  os.chdir(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
  parser = arg_parser()
  args = parser.parse_args()
  assert not args.title.isdigit(), "标题不可为数字"
  new_md(args.title, args.save_path)

main()

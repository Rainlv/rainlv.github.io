#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import argparse
import os
from datetime import datetime
from pathlib import Path


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", "-t")
    parser.add_argument("--output_path", "-o", default="_posts")
    parser.add_argument("--format_file", "-f")
    return parser


def time_format(title: str):
    assert not title.isdigit(), "标题不可为数字"
    FULL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S +0800'
    title_time_fmt = "%Y-%m-%d"
    time_ymd_str = datetime.now().strftime(title_time_fmt)
    full_time_str = datetime.now().strftime(FULL_TIME_FORMAT)
    return f"""---
title: {title}
date: {full_time_str}
---\n""", time_ymd_str


def new_md(title: str, save_path: str, raw_file: Path = None):
    title_str, time_ymd_str = time_format(title)
    save_file_name = os.path.join(save_path, time_ymd_str + f"-{title}.md")
    if os.path.exists(save_file_name):
        while 1:
            confirm = input("存在同名文件，是否覆盖(y/n):").lower()
            if confirm in ["n", "no"]:
                return
            elif confirm in ["y", "yes"]:
                break
            else:
                print('请输入" y 或 s "!')
    if raw_file:
        f = raw_file.open("r")
        raw_content = f.read()
        write_str = title_str + raw_content
    else:
        write_str = title_str
    with open(save_file_name, 'w', encoding='utf8') as fw:
        fw.seek(0)
        fw.write(write_str)

    print(f"{os.path.abspath(save_file_name)} Successfully Generated!")
    return True


def format_md(file):
    pass


def main():
    os.chdir(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
    parser = arg_parser()
    args = parser.parse_args()
    if not args.title and not args.format_file:
        raise AssertionError("输入待格式化文件或新建文件标题")
    if args.title:
        title = args.title
        new_md(title, args.output_path)
    else:
        raw_file = Path(args.format_file)
        title = raw_file.stem
        new_md(title, args.output_path, raw_file)


main()

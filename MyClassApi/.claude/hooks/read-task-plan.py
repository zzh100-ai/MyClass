#!/usr/bin/env python
"""
PreToolUse hook: 在每次工具调用前读取 task_plan.md 作为额外上下文注入。
"""
import json, sys, os

# 从脚本位置向上查找项目根目录（含 .claude 目录的父目录）
script_dir = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(script_dir)  # .claude/
project_root = os.path.dirname(parent)  # 项目根目录
# 如果 task_plan.md 不存在，再往上找一层（兼容 MyClassWeb/.claude/hooks/ 的情况）
task_plan_path = os.path.join(project_root, 'task_plan.md')
if not os.path.exists(task_plan_path):
    higher = os.path.dirname(project_root)
    task_plan_path = os.path.join(higher, 'task_plan.md')

try:
    if os.path.exists(task_plan_path):
        with open(task_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": f"[当前任务计划]\n{content}"
            }
        }
    else:
        output = {}
except Exception:
    output = {}

json.dump(output, sys.stdout)
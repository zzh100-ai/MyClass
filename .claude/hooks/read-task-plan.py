#!/usr/bin/env python
"""
PreToolUse hook: 在每次工具调用前读取 task_plan.md 作为额外上下文注入。
"""
import json, sys, os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
task_plan_path = os.path.join(project_root, 'task_plan.md')

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
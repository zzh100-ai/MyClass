#!/bin/bash
# Stop hook：每次 Claude 停止时，检查代码变更并提示需要更新哪些文档

STDIN=$(cat)
SESSION_ID=$(echo "$STDIN" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)

cd /d/code/python/MyClass

# 收集变更文件
CHANGED=$(git diff --name-only HEAD 2>/dev/null)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null)

# 判断需要更新什么文档
API_CHANGED=0
SETTINGS_CHANGED=0
NEW_APP=0
MODEL_CHANGED=0
VIEW_CHANGED=0
TUTORIAL_NEEDED=0

check_pattern() {
    local files="$1"
    echo "$files" | grep -q "apps/.*/models.py" && MODEL_CHANGED=1
    echo "$files" | grep -q "apps/.*/views.py" && VIEW_CHANGED=1
    echo "$files" | grep -q "apps/.*/serializers.py" && VIEW_CHANGED=1
    echo "$files" | grep -q "apps/.*/urls.py" && API_CHANGED=1
    echo "$files" | grep -q "config/settings.py" && SETTINGS_CHANGED=1
    echo "$files" | grep -q "requirements/" && SETTINGS_CHANGED=1
    echo "$files" | grep -q "doc/" && DOCS_CHANGED=1
    # 检查是否有新的 app 目录
    echo "$files" | grep -q "apps/[^/]*/migrations" && NEW_APP=1
}

check_pattern "$CHANGED"
check_pattern "$UNTRACKED"

# 构建提示消息
MSGS=()
[ $API_CHANGED -eq 1 ] && MSGS+=("• API 接口有变更 → 更新 doc/api/ 下对应文档")
[ $MODEL_CHANGED -eq 1 ] && MSGS+=("• 模型有变更 → 更新 doc/tutorials/ 和笔记")
[ $VIEW_CHANGED -eq 1 ] && MSGS+=("• 视图/序列化器有变更 → 更新 doc/api/")
[ $SETTINGS_CHANGED -eq 1 ] && MSGS+=("• 配置有变更 → 更新 CLAUDE.md 技术栈状态和 doc/notes/")
[ $NEW_APP -eq 1 ] && MSGS+=("• 新增 Django app → 更新 CLAUDE.md 架构部分")

if [ ${#MSGS[@]} -eq 0 ]; then
    # 没有明显的代码变更需要更新文档，但可能有 doc 文件本身的变更
    SYSTEM_MSG="本次会话无明显代码变更，CLAUDE.md 和 doc 文档无需更新。"
else
    SYSTEM_MSG="📝 检测到代码变更，下次会话请更新以下文档：\n$(printf '%s\n' "${MSGS[@]}")"
fi

# 输出 JSON，systemMessage 会显示给用户
cat <<EOF
{
  "systemMessage": "$SYSTEM_MSG",
  "continue": true
}
EOF
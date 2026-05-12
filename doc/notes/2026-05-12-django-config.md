# 2026-05-12 Django 后端配置笔记

## 环境信息

- Python: 3.9（conda 环境 `luffycityapi`）
- Django: 4.2.30
- MySQL: 8.0.26（Windows，端口 3306）
- Redis: 默认安装（127.0.0.1:6379，无密码）

## 关键决策

### 1. BASE_DIR 计算
`config/settings.py` 中 `BASE_DIR = Path(__file__).resolve().parent.parent`，即 `config/` 的父目录 = `MyClassApi/`。`.env` 文件放在 `BASE_DIR / ".env"`，即 `MyClassApi/.env`。

### 2. load_dotenv 的坑
`load_dotenv()` 的返回值是 `True`/`False`（表示是否成功加载），不是加载后的字典。正确做法是先调用 `load_dotenv()`，然后使用 `os.getenv()` 逐个读取。不要把 `load_dotenv()` 的返回值当 dict 用。

### 3. mysqlclient vs PyMySQL
选择 `mysqlclient` 是因为性能更好（C 扩展）。Windows 下编译可能遇到问题——如果预编译的 wheel 不可用，备选方案是 `PyMySQL`。

### 4. 目录结构调整
- 原 `MyClassApi/MyClassApi/` → `MyClassApi/config/`
- 新建 `MyClassApi/apps/` 统一存放业务模块
- 新建 `MyClassApi/requirements/` 分环境管理依赖
- 从 `MyClassApi` 内部执行 `mv` 时要注意路径——使用绝对路径更安全

### 5. django-redis 版本降级
安装时发现环境中已有 `django-redis 6.0.0`，但 `requirements/base.txt` 限定了 `<6.0`。因为 6.0 可能引入了不兼容的变更，pip 自动降级到 5.4.0。后续如需升级需评估兼容性。

## 接口约定

- API 基础路径：`/api/v1/`
- 认证方式：待定（后续开发时确定 JWT 或 Session 方案）
- DRF 默认配置：未做额外配置，使用框架默认行为

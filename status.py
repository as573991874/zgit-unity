import utils
import os
import json
import subprocess

# 工作区是否初始化
workspace_is_init = False
# 工作区配置
workspace_setting = None
# 配置仓库是否初始化
repo_config_is_init = False

# 初始化状态
def init():
    global workspace_is_init, workspace_setting, repo_config_is_init
    workspace_is_init = os.path.exists(utils.__setting_path__)
    if workspace_is_init:
        workspace_setting = read_json_file(utils.__setting_path__)
        repo_config_is_init = os.path.exists(utils.__repo_config_path__)

# 检查空间
def check_workspace():
    return workspace_is_init

# 初始化空间
def init_workspace():
    global workspace_setting
    if workspace_is_init:
        return

    # 创建数据结构
    file_path = os.path.join(os.path.dirname(__file__), utils.__template_setting_path__)
    workspace_setting = read_json_file(file_path)
    # 序列化为 JSON
    save_user_config()
    # 重新初始化
    init()

# 获取绝对地址
def get_abs_setting_path():
    return os.path.abspath(utils.__setting_path__)

# 打开文件
def open_txt_editor(file_path):
    if os.path.exists(workspace_setting['vscode']):
        subprocess.run(["open", "-a", workspace_setting['vscode'], file_path])
    else:
        subprocess.run(["open", file_path])

# 读取 JSON 文件
def read_json_file(json_file_path):
    try:
        with open(json_file_path, 'r') as f:
            json_data = json.load(f, encoding='utf-8')
        return json_data
    except json.decoder.JSONDecodeError as e:
        print(f'{json_file_path} JSON 格式错误!')
        return {}
    except Exception as e:
        print(f'读取 {json_file_path} JSON 发生错误!')
        return {}
    
# 保存配置
def save_user_config():
    global workspace_setting
    # 序列化为 JSON
    json_data = json.dumps(workspace_setting, indent=4, ensure_ascii=False)
    os.makedirs(utils.__zgit_path__, exist_ok=True)
    # 存储在本地文件
    with open(utils.__setting_path__, "w") as f:
        f.write(json_data)

# 初始化配置
def init_repo_config():
    if not workspace_is_init:
        return
    if repo_config_is_init:
        return
    subprocess.run(["git", "clone", workspace_setting['repo'], utils.__repo_config_path__])
    print('初始化配置仓库...')
    open_repo(utils.__repo_config_path__)

# 获取绝对地址
def get_abs_repo_config_path():
    return os.path.abspath(utils.__repo_config_path__)

# 打开仓库
def open_repo(repo_path):
    if not os.path.exists(repo_path):
        print("仓库未初始化：" + repo_path)
        return
    if os.path.exists(workspace_setting['fork']):
        subprocess.run(["open", "-a", workspace_setting['fork'], repo_path])
    else:
        subprocess.run(["open", repo_path])
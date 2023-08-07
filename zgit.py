import utils
import status
import argparse
import cmd
import os

class ZGitCLI(cmd.Cmd):
    intro = 'Welcome to zgit - Unity!' 
    prompt = '(zgit) '

    # 打印版本
    def do_version(self, args):
        """Print version"""
        print(utils.__version__)

    # 初始化
    def do_init(self, args):
        status.init()
    
    # 检查状态
    def do_status(self, args):
        self.do_init(args)
        """Check status"""
        if not status.workspace_is_init:
            print(f"{os.getcwd()} 未初始化")
        else:
            print(f"{status.get_abs_setting_path()} 已初始化")

    # 初始化工作区
    def do_init_workspace(self, args):
        self.do_init(args)
        if not status.workspace_is_init:
            status.init_workspace()
        print(f"{status.get_abs_setting_path()} 已初始化")
        status.open_txt_editor(status.get_abs_setting_path())

    # 初始化配置仓库
    def do_init_repo_config(self, args):
        self.do_init(args)
        if not status.workspace_is_init:
            print("清先初始化工作区，--init_workspace")
            return
        if not status.repo_config_is_init:
            status.init_repo_config()
            print(f"{status.get_abs_repo_config_path()} 已初始化")
        else:
            print('初始化配置仓库...')

    # 退出
    def do_exit(self, args):
        return True
    
cli = ZGitCLI()

parser = argparse.ArgumentParser(description='A Git Tool For Unity Version Control')
parser.add_argument('-v', '--version', action='store_true', help='Print tool version')
parser.add_argument('--status', action='store_true', help='Print WorkSpace Status')
parser.add_argument('--init_workspace', action='store_true', help='Init WorkSpace Status')
parser.add_argument('--init_repo_config', action='store_true', help='Init WorkSpace Status')
args = parser.parse_args()

if args.version:
    cli.do_version(args)
elif args.status:
    cli.do_status(args)
elif args.init_workspace:
    cli.do_init_workspace(args)
elif args.init_repo_config:
    cli.do_init_repo_config(args)
else:
    cli.cmdloop()
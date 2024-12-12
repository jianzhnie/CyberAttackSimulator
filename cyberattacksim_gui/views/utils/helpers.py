import glob
import logging
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from django.urls import reverse

# 导入 CyberAttackSimulator 模块
from cyberattacksim import _CAS_HOME_DIR, IMAGES_DIR, NOTEBOOKS_DIR, VIDEOS_DIR
from cyberattacksim.cyberattacksim_run import CyberAttackRun
from cyberattacksim.envs.generic.core.action_loops import ActionLoop
from cyberattacksim.game_modes.game_mode_db import GameModeDB, GameModeSchema
from cyberattacksim.networks.network import Network, NetworkLayout
from cyberattacksim.networks.network_db import NetworkDB, NetworkQuery
from cyberattacksim_gui import CAS_GUI_RUN_LOG, CAS_GUI_STDOUT
from cyberattacksim_server.settings.base import DOCS_ROOT, STATIC_URL


class RunManager:
    """管理运行 CyberAttackSimulator 的工具类。

    提供静态方法和类方法来管理模拟运行，包括启动进程、生成 GIF 和 WebM 输出。
    """

    process = None  # 存储当前运行的多进程对象
    counter = 0  # 用于跟踪运行的次数
    gif_count = len(list(IMAGES_DIR.iterdir()))  # 当前 GIF 文件计数
    webm_count = len(list(VIDEOS_DIR.iterdir()))  # 当前 WebM 文件计数
    run_args = None  # 存储运行参数
    run_started = False  # 标记是否已启动运行

    gif_path = ''  # 当前生成的 GIF 路径
    webm_path = ''  # 当前生成的 WebM 路径

    @staticmethod
    def format_file(path: Path) -> str:
        """格式化文本文件内容为 HTML 格式，供 GUI 显示。

        :param path: 文件路径
        :return: 格式化的 HTML 文本
        """
        try:
            with open(path, 'r') as f:
                lines = [line.replace(' ', '&nbsp;') for line in f.readlines()]
                return '<br>'.join(lines)
        except Exception:
            return ''

    @classmethod
    def run_yt(cls, **kwargs):
        """执行 CyberAttackSimulator 运行，包括训练、评估和导出结果。

        :param kwargs: 运行参数，例如是否保存模型、生成 GIF 等。
        """
        if CAS_GUI_RUN_LOG.exists():
            CAS_GUI_RUN_LOG.unlink()  # 删除旧的运行日志
        logger = logging.getLogger('cas_run')
        logger.setLevel(logging.DEBUG)

        # 设置文件日志记录
        fh = logging.FileHandler(CAS_GUI_RUN_LOG.as_posix())
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        # 捕获 stdout 输出
        with open(CAS_GUI_STDOUT, 'w+') as sys.stdout:
            run = CyberAttackRun(**kwargs, auto=False, logger=logger)
            run.setup()  # 配置运行环境
            run.train()  # 训练模型
            run.evaluate()  # 评估模型

            if kwargs.get('save'):
                run.save()  # 保存模型

            if kwargs.get('export'):
                run.export()  # 导出模型

            # 如果需要生成 GIF 或 WebM
            if kwargs.get('render_gif') or kwargs.get('render_webm'):
                loop = ActionLoop(
                    env=run.env,
                    agent=run.agent,
                    filename='CAS',
                    episode_count=kwargs.get('num_episodes',
                                             run.total_timesteps),
                )
                loop.gif_action_loop(
                    gif_output_directory=IMAGES_DIR,
                    webm_output_directory=VIDEOS_DIR,
                    save_gif=kwargs['render_gif'],
                    save_webm=kwargs['render_webm'],
                    render_network=True,  # 强制渲染网络以解决生成 GIF 的问题
                )

    @classmethod
    def get_output(cls) -> Dict[str, Any]:
        """获取运行输出，包括日志和生成的 GIF/WebM 文件路径。

        :return: 包含输出信息的字典
        """
        cls.counter += 1
        output = {
            'stderr': cls.format_file(CAS_GUI_RUN_LOG),
            'stdout': cls.format_file(CAS_GUI_STDOUT),
            'gif': cls.gif_path,
            'webm': cls.webm_path,
            'active': cls.process.is_alive() if cls.process else False,
            'request_count': cls.counter,
        }

        # 检查是否有新生成的 GIF 或 WebM
        if cls.process and cls.process.is_alive():
            gif_dir = glob.glob(f'{IMAGES_DIR.as_posix()}/*.gif')
            webm_dir = glob.glob(f'{VIDEOS_DIR.as_posix()}/*.webm')

            if len(gif_dir) > cls.gif_count:
                cls.gif_count = len(gif_dir)
                cls.gif_path = max(gif_dir, key=os.path.getctime)
                output[
                    'gif'] = f'/{STATIC_URL}{Path(cls.gif_path).name}'.replace(
                        '\\', '/')

            if len(webm_dir) > cls.webm_count:
                cls.webm_count = len(webm_dir)
                cls.webm_path = max(webm_dir, key=os.path.getctime)
                output[
                    'webm'] = f'/{STATIC_URL}{Path(cls.webm_path).name}'.replace(
                        '\\', '/')

        return output

    @classmethod
    def start_process(cls, fkwargs: dict):
        """启动一个新进程来运行模拟。

        :param fkwargs: 运行参数
        """
        cls.run_started = True
        cls.run_args = fkwargs
        cls.counter = 0
        cls.gif_path = ''
        cls.webm_path = ''

        cls.process = multiprocessing.Process(target=cls.run_yt,
                                              kwargs=fkwargs)
        cls.process.start()


class NetworkManager:
    """Handle all interfacing with CyberAttackSim networks in :attribute:

    `network_db` and their info for the GUI session.
    """

    db: NetworkDB = NetworkDB()
    current_network: Network = None

    @classmethod
    def filter_entry_nodes(cls, min, max) -> List[str]:
        """Generate a list of ``uuids`` corresponding to networks that have a
        number of entry nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid for network in cls.db.search(
                NetworkQuery.num_of_entry_nodes_between(min, max))
        ]

    @classmethod
    def filter_high_value_nodes(cls, min, max) -> List[str]:
        """Generate a list of ``uuids`` corresponding to networks that have a
        number of high value nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid for network in cls.db.search(
                NetworkQuery.num_of_high_value_nodes_between(min, max))
        ]

    @classmethod
    def filter_network_nodes(cls, min, max) -> List[str]:
        """Generate a list of ``uuids`` corresponding to networks that have a
        number of nodes within ``min`` <= x <= ``max``.

        :param min: the minimum value (inclusive)
        :param max: the maximum value (inclusive)
        """
        return [
            network.doc_metadata.uuid for network in cls.db.search(
                NetworkQuery.num_of_nodes_between(min, max))
        ]

    @classmethod
    def filter(cls, filters: Dict[str, dict]) -> List[str]:
        """Call the filter method for the appropriate attribute.

        :param attribute: the string name of a network attribute to filter
        :param min: the minimum value of the attribute (inclusive)
        :param max: the maximum value of the attribute (inclusive)
        """
        networks: List[set] = []
        for k, v in filters.items():
            attr = f'filter_{k}'
            if hasattr(cls, attr):
                networks.append(set(getattr(cls, attr)(v['min'], v['max'])))
        if len(networks) == 1:
            return list(networks[0])
        return list(networks[0].intersection(*[networks][1:]))

    @classmethod
    def get_network_data(cls) -> List[dict]:
        """Gather the doc metadata of all network objects."""
        return [network.doc_metadata for network in cls.db.all()]


class GameModeManager:
    """Wrapper over an instance of :class:

    `~cyberattacksim.game_modes.game_mode_db.GameModeDB` to provide helper
    functions to the GUI.
    """

    db: GameModeDB = GameModeDB()

    @classmethod
    def get_game_mode_data(cls, valid_only: bool = False) -> List[dict]:
        """Gather the doc metadata of all game mode objects adding a field
        `valid` to denote that a game mode is fully valid.

        :param valid_only: return only valid game modes.
        """
        game_modes = [{
            **g.doc_metadata.to_dict(), 'valid': g.validation.passed
        } for g in cls.db.all()]
        if not valid_only:
            return game_modes
        return [g for g in game_modes if g['valid']]

    @classmethod
    def get_game_modes_compatible_with(cls, network: Network):
        """Retrieve all game modes compatible with a given network.

        :param network: an instance of :class: `~cyberattacksim.networks.network.Network`
        """
        return cls.db.search(
            GameModeSchema.NETWORK_COMPATIBILITY.compatible_with(network))

    # @classmethod
    # def filter(cls, filters: dict):
    #     """Filter a game mode using a dictionary of ranges or values."""
    #     item_dict = GameMode().to_legacy_dict()
    #     queries = []
    #     for name, filter in filters.items():
    #         if isinstance(item_dict[name], (FloatItem, IntItem)):
    #             queries.append(item_dict[name].query.bt(filter["min"], filter["max"]))
    #         else:
    #             queries.append((item_dict[name].query == filter))
    #     _filter = reduce(and_, queries)
    #     return cls.db.search(_filter)


def next_key(_dict: dict, key: int) -> Any:
    """获取字典中指定键的下一个键。

    如果当前键是字典中最后一个键，则返回字典的第一个键。

    参数:
    _dict (dict): 要操作的字典。
    key (int): 当前键。

    返回:
    Any: 下一个键或字典的第一个键。
    """
    keys = list(_dict.keys())  # 获取字典的键列表
    key_index = keys.index(key)  # 找到当前键的位置
    if key_index < (len(keys) - 1):  # 如果不是最后一个键
        return keys[key_index + 1]  # 返回下一个键
    return keys[0]  # 否则返回第一个键


def uniquify(path: Path) -> Path:
    """通过在文件名后添加编号生成唯一的文件路径。

    如果指定路径已存在，则在文件名后添加 (1)、(2) 等直到路径唯一。

    参数:
    path (Path): 提供的初始路径。

    返回:
    Path: 唯一化后的路径。
    """
    filename = path.stem  # 获取文件名（不含扩展名）
    extension = path.suffix  # 获取文件扩展名
    parent = path.parent  # 获取路径的父目录
    counter = 1  # 初始化计数器

    while path.exists():  # 如果路径已存在
        path = parent / f'{filename}({counter}){extension}'  # 在文件名后加编号
        counter += 1  # 计数器递增
    return path  # 返回唯一路径


def get_docs_sections():
    """获取 Sphinx 文档的所有部分名称。

    返回:
    List[str]: 文档部分的名称列表。
    """
    docs_dir = DOCS_ROOT / 'source'  # 定位到文档的源目录
    docs_sections = []
    if docs_dir.exists():  # 如果目录存在
        sections = [p.stem for p in docs_dir.iterdir()
                    if p.suffix == '.html']  # 提取 HTML 文件名
        docs_sections += sections
    docs_dir = docs_dir / '_autosummary'  # 进入自动摘要目录
    if docs_dir.exists():  # 如果目录存在
        sections = [
            f'_autosummary/{p.stem}' for p in docs_dir.iterdir()
            if p.suffix == '.html'
        ]
        docs_sections += sections
    return docs_sections


def get_url(url_name: str, *args, **kwargs):
    """封装 Django 的 reverse 函数，用于 URL 反向解析。

    参数:
    url_name (str): URL 名称。
    *args: 位置参数。
    **kwargs: 关键字参数。

    返回:
    str: 反向解析后的 URL 或 None（如果解析失败）。
    """
    try:
        return reverse(url_name, args=args, kwargs=kwargs)  # 尝试反向解析 URL
    except Exception:
        return None  # 如果失败则返回 None


def get_url_dict(name: str, href: str, new_tab: bool = False):
    """创建一个描述 URL 链接的字典。

    参数:
    name (str): 链接名称。
    href (str): 链接地址。
    new_tab (bool): 是否在新标签页中打开。

    返回:
    dict: 描述链接的字典。
    """
    return {'name': name, 'href': href, 'new_tab': new_tab}


def get_toolbar(current_page_title: str = None):
    """生成包含工具栏项的字典。

    参数:
    current_page_title (str): 当前页面的标题。

    返回:
    dict: 工具栏项信息的字典。
    """
    default_toolbar = {
        'platform': {
            'icon': 'bi-house-door',
            'title': 'PlatForm',
            'title_zh': '平台主页',
            'cypressRefToolbar': 'toolbar-home',
            'cypressRefMenu': 'menu-home',
        },
        'manage-game_modes': {
            'icon': 'bi-gear',
            'title': 'Manage game modes',
            'title_zh': '仿真配置',
            'cypressRefToolbar': 'toolbar-manage-game-modes',
            'cypressRefMenu': 'menu-manage-game-modes',
        },
        'manage-networks': {
            'icon': 'bi-diagram-2',
            'title': 'Manage networks',
            'title_zh': '网络配置',
            'cypressRefToolbar': 'toolbar-manage-networks',
            'cypressRefMenu': 'menu-manage-networks',
        },
        'run-view': {
            'icon': 'bi-play',
            'title': 'Run session',
            'title_zh': '仿真训练',
            'cypressRefToolbar': 'toolbar-run-yt',
            'cypressRefMenu': 'menu-run-yt',
        },
        'about': {
            'icon':
            'bi-question-lg',
            'title':
            'About',
            'title_zh':
            '关于',
            'links': [
                get_url_dict(n, href, True) for n, href in zip(
                    [
                        'Contributors', 'Discussions', 'Report bug',
                        'Feature request'
                    ],
                    [
                        'https://git.pcl.ac.cn/niejzh/CyberAttackSimulator/graphs/contributors',
                        'https://git.pcl.ac.cn/niejzh/CyberAttackSimulator/discussions',
                        'https://git.pcl.ac.cn/niejzh/CyberAttackSimulator/issues/new?assignees=&labels=bug&template=bug_report.md&title=[BUG]',
                        'https://git.pcl.ac.cn/niejzh/CyberAttackSimulator/issues/new?assignees=&labels=feature_request&template=feature_request.md&title=[REQUEST]',
                    ],
                )
            ],
            'info': [f'Version: {version()}'],
            'cypressRefToolbar':
            'toolbar-about',
            'cypressRefMenu':
            'menu-about',
        },
    }
    for id, info in default_toolbar.items():  # 标记当前页面为活动状态
        default_toolbar[id]['active'] = info['title'] == current_page_title
    return default_toolbar


def version() -> str:
    """Gets the version from the `VERSION` file.

    :return: The version string.
    """
    import cyberattacksim

    return cyberattacksim.__version__


def open_jupyter_notebook():
    """Open a jupyter session for the notebooks directory in a subprocess and
    return the url."""
    print('OPENING NOTEBOOKS')
    # look into a project dir for a config
    os.environ.setdefault('JUPYTER_CONFIG_PATH',
                          (_CAS_HOME_DIR / 'notebooks').as_posix())
    # subprocess.call("jupyter trust Create a Network.ipynb",env=os.environ.copy()) # TODO: Delete
    # see if the required session is active
    b = subprocess.check_output('jupyter-lab list'.split(),
                                env=os.environ.copy(),
                                stderr=subprocess.STDOUT).decode('utf-8')
    print('LIST>>>', b)
    if '9999' not in b:
        # if not active create it
        working_dir = os.getcwd()
        os.chdir(NOTEBOOKS_DIR)
        subprocess.Popen('jupyter-lab  --no-browser --port 9999'.split(),
                         env=os.environ.copy())
        os.chdir(working_dir)
    start_time = time.time()
    unreachable_time = 10
    while '9999' not in b:
        # try to find the active session
        timer = time.time()
        elapsed_time = timer - start_time
        b = subprocess.check_output('jupyter-lab list'.split(),
                                    env=os.environ.copy(),
                                    stderr=subprocess.STDOUT).decode('utf-8')
        if '9999' in b:
            break
        if elapsed_time > unreachable_time:
            return None
    # get the tokenised url
    paths = [p.split('::', 1)[0] for p in b.split('\n')]

    paths = [p.split(']')[1].lstrip().rstrip() for p in paths if 'http' in p]
    path = [p for p in paths if '9999' in p][-1]
    return path


def get_network_layouts():
    """Get an array of available network layout algorithms."""
    return list(map(lambda c: c.value, NetworkLayout))

import logging
import multiprocessing
import sys
from typing import Any, Dict

from cyberattacksim import IMAGES_DIR, VIDEOS_DIR
# 导入 CyberAttackSimulator 模块
from cyberattacksim_gui import CAS_GUI_RUN_LOG, CAS_GUI_STDOUT
from cyberwheel.cyberwheel_run import CyberWheelAttackRun


class MassiveNetworkRunManager:
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
    def format_file(path):
        """Format a text reference file as a html object."""
        with open(path, 'r') as f:
            try:
                lines = [line.replace(' ', '&nbsp;') for line in f.readlines()]
                text = '<br>'.join(lines)
                return text
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
            run = CyberWheelAttackRun(**kwargs, auto=False, logger=logger)
            run.setup()  # 配置运行环境
            run.train()  # 训练模型
            run.evaluate()  # 评估模型

            if kwargs.get('save'):
                run.save()  # 保存模型

            if kwargs.get('export'):
                run.export()  # 导出模型

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
        return output

    @classmethod
    def get_output_another(cls) -> Dict[str, Any]:
        """获取运行输出，包括日志和生成的 GIF/WebM 文件路径。

        :return: 包含输出信息的字典
        """
        cls.counter += 1
        output = {
            'stderr': cls.format_file(CAS_GUI_RUN_LOG),
            'stdout': cls.format_file(CAS_GUI_STDOUT),
            'active': cls.process.is_alive() if cls.process else False,
            'request_count': cls.counter,
        }
        return output

    @classmethod
    def start_process(cls, fkwargs: dict):
        """Spawn a subprocess to run the instance of :class:

        `~yawning_titan.yawning_titan_run.YawningTitanRun` with the given
        arguments.
        """
        cls.run_started = True
        cls.run_args = fkwargs
        cls.counter = 0
        # clear gif path
        cls.gif_path = ''

        # clear webm path
        cls.webm_path = ''

        cls.process = multiprocessing.Process(
            target=MassiveNetworkRunManager.run_yt,
            kwargs=fkwargs,
        )
        cls.process.start()

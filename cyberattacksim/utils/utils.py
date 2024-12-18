import platform
from typing import Iterable
import psutil
import torch
from transformers.utils import is_torch_cuda_available, is_torch_npu_available
import logging
import time


# 配置 logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_system_info(logger: None):
    logger.info("系统诊断信息:")

    # 获取平台信息
    plat_info = {
        '操作系统': platform.platform(),
        'Python版本': platform.python_version(),
        'CPU核心数': psutil.cpu_count(),
        '可用内存': psutil.virtual_memory().available / (1024**3),
    }

    # 获取CUDA和PyTorch信息
    info = {
        'CUDA可用': torch.cuda.is_available(),
        'CUDA版本': torch.version.cuda,
        'CUDA设备数': torch.cuda.device_count(),
        'cuDNN版本': torch.backends.cudnn.version(),
        'PyTorch版本': torch.__version__,
    }

    # 检查CUDA支持
    if is_torch_cuda_available():
        info['PyTorch版本'] += ' (GPU)'
        info['CUDA版本'] = torch.cuda.get_device_name()

    # 检查NPU支持
    if is_torch_npu_available():
        info['PyTorch版本'] += ' (NPU)'
        info['NPU type'] = torch.npu.get_device_name()
        info['CANN version'] = torch.version.cann

    # 合并信息
    info.update(plat_info)

    # 打印所有信息
    for key, value in info.items():
        logger.info(f"{key}: {value}")

    return info


def print_process_items(
    iterable_items: Iterable, description: str = "H", interval: int = 100
) -> None:
    total = len(iterable_items)
    for idx, item in enumerate(iterable_items, start=1):
        # 每处理固定步长打印进度
        if idx % interval == 0 or idx == total:
            logger.info(
                f"{description} {idx}/{total} items ({(idx / total) * 100:.2f}%)"
            )


# 示例使用
if __name__ == "__main__":
    items = range(100)
    print_process_items(items)

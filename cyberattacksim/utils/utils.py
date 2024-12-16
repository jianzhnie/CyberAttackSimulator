import platform

import psutil
import torch
from transformers.utils import is_torch_cuda_available, is_torch_npu_available


def get_system_info():
    print('系统诊断信息:')

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
        print(f'{key}: {value}')

    return info

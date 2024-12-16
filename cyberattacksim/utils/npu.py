from abc import ABC
from importlib.util import find_spec
from typing import List, Union

import torch


def is_package_present(package_name: str) -> bool:
    try:
        return find_spec(package_name) is not None
    except ModuleNotFoundError:
        return False


NPU_TORCH_PACKAGE_AVAILABLE = is_package_present('torch_npu')

if NPU_TORCH_PACKAGE_AVAILABLE:
    import torch_npu  # noqa: F401


class TorchDeviceManager(ABC):
    """This class contains the function needed for supporting an acclerator
    family in Ray AI Library."""

    def is_available(self) -> bool:
        """Validate if device is available."""
        ...

    def get_devices(self) -> List[torch.device]:
        """Gets the correct torch device configured for this process."""
        ...

    def set_device(self, device: Union[torch.device, int, str, None]):
        """Set the correct device for this process."""
        ...

    def supports_stream(self) -> bool:
        """Validate if the device type support create a stream."""
        ...

    def create_stream(self, device: torch.device):
        """Create a device stream."""
        ...

    def get_stream_context(self, stream):
        """Get a stream context of device.

        If device didn't support stream, this should return a empty context
        manager instead of  None.
        """
        ...

    def get_current_stream(self):
        """Get current stream on accelerators like
        torch.cuda.current_stream."""
        ...


class NPUTorchDeviceManager(TorchDeviceManager):
    """Ascend NPU device manager."""

    @staticmethod
    def register_custom_torch_dist_backend():
        if NPU_TORCH_PACKAGE_AVAILABLE:
            import torch_npu  # noqa: F401, F811

    def is_available(self) -> bool:
        if not NPU_TORCH_PACKAGE_AVAILABLE:
            return False

        return torch.npu.is_available()

    def get_devices(self) -> List[torch.device]:
        """Gets the correct torch device list configured for this process.

        Returns a list of torch NPU devices allocated for the current worker.
        If no NPUs are assigned, then it returns a list with a single CPU
        device.
        """
        if NPU_TORCH_PACKAGE_AVAILABLE:
            devices = [torch.device('npu')]
        else:
            raise RuntimeError(
                'Using NPUTorchDeviceManager but torch npu is not available.')

        return devices

    def set_device(self, device: Union[torch.device, int]):
        torch.npu.set_device(device)

    def supports_stream(self) -> bool:
        """Validate if the device type support to create a stream."""
        return True

    def create_stream(self, device):
        """Create a stream on NPU device."""
        return torch.npu.Stream(device)

    def get_stream_context(self, stream):
        """Get a torch.stream context on NPU device."""
        return torch.npu.stream(stream)

    def get_current_stream(self):
        """Get current stream for NPU device."""
        return torch.npu.current_stream()

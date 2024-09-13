
#  镜像列表

- http://mirrors.cn-central-221.ovaijisuan.com/mirrors.html

##  Ascend Docker Images

```shell
swr.cn-central-221.ovaijisuan.com/wh-aicc-fae/pytorch2_1_0_kernels             PyTorch2.1.0-cann8.0.RC2_py_3.9-euler_2.8.3-64GB          897707ec6dbc   4 weeks ago      28.6GB
swr.cn-east-317.qdrgznjszx.com/donggang/llama-factory-ascend910b               cann8-py310-torch2.2.0-ubuntu18.04                        3b7c5870a34d   3 months ago     24.9GB
swr.cn-central-221.ovaijisuan.com/mindformers/mindformers1.0_mindspore2.2.11   aarch_20240125                                            e75681b68f94   7 months ago     13.6GB
swr.cn-central-221.ovaijisuan.com/dxy/mindspore_kernels                        MindSpore2.2.10-cann7.0.0beta1_py_3.9-euler_2.8.3-64GB    1f1e9f6a2a74   7 months ago     13.1GB
swr.cn-central-221.ovaijisuan.com/dxy/pytorch2_1_0_kernels                     PyTorch2.1.0-cann7.0.0.alpha003_py_3.9-euler_2.8.3-64GB   3b308b71c9b5   8 months ago     13.3GB
swr.cn-central-221.ovaijisuan.com/dxy/pytorch2_1_0                             PyTorch2.1.0-cann7.0rc1_py_3.9-euler_2.8.3-64GB           35c2e65ccb82   10 months ago    12.6GB
```



## Docker Run Scripts

### Docker Image @1

```shell
## PyTorch2.1.0-cann8.0.RC2_py_3.9-euler_2.8.3-64GB
docker_images=swr.cn-central-221.ovaijisuan.com/wh-aicc-fae/pytorch2_1_0_kernels:PyTorch2.1.0-cann8.0.RC2_py_3.9-euler_2.8.3-64GB
model_dir=/home/niejz/work_dir/
docker run -it -u root --ipc=host --net=host \
        --device=/dev/davinci0   \
        --device=/dev/davinci_manager  \
        --device=/dev/devmm_svm   \
        --device=/dev/hisi_hdc \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
        -v /usr/local/dcmi:/usr/local/dcmi  \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi   \
        -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware   \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi   \
        -v ${model_dir}:${model_dir} \
        --entrypoint=/bin/bash   \
        ${docker_images} 
```

### Docker Image @2
```shell
# Change `device` upon your resources
docker_images=swr.cn-east-317.qdrgznjszx.com/donggang/llama-factory-ascend910b:cann8-py310-torch2.2.0-ubuntu18.04
model_dir=/home/niejz/work_dir/CyberAttackSimulator
docker run -it -u root --ipc=host --net=host \
        --device=/dev/davinci7 \
        --device=/dev/davinci_manager \
        --device=/dev/devmm_svm \
        --device=/dev/hisi_hdc \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
        -v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
        -v /var/log/npu:/usr/slog ${docker_images} \
        /bin/bash
```

### Docker Image @3
```shell
# aarch_20240125 
docker_images=swr.cn-central-221.ovaijisuan.com/mindformers/mindformers1.0_mindspore2.2.11:aarch_20240125 
model_dir=/home/niejz/work_dir/
docker run -it -u root  --ipc=host --network=host \
        --device=/dev/davinci0 \
        --device=/dev/davinci1 \
        --device=/dev/davinci_manager \
        --device=/dev/devmm_svm \
        --device=/dev/hisi_hdc \
        -v /var/log/npu/:/usr/slog \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
        -v ${model_dir}:${model_dir} \
        ${docker_images} \
        /bin/bash
```


### Docker Image @4
```shell
# MindSpore2.2.10-cann7.0.0beta1_py_3.9-euler_2.8.3-64GB
docker_images=swr.cn-central-221.ovaijisuan.com/dxy/mindspore_kernels:MindSpore2.2.10-cann7.0.0beta1_py_3.9-euler_2.8.3-64GB
model_dir=/home/niejz/work_dir/
docker run -it  -u root  --ipc=host --net=host \
        --device=/dev/davinci0   \
        --device=/dev/davinci_manager   \
        --device=/dev/devmm_svm \
        --device=/dev/hisi_hdc   \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver    \
        -v /usr/local/dcmi:/usr/local/dcmi   \
        -v /usr/local/Ascend/toolbox:/usr/local/Ascend/toolbox \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi   \
        -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware  \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi   \
        -v ${model_dir}:${model_dir} \
        --entrypoint=/bin/bash   \
        ${docker_images} 
```


### Docker Image @5
```shell
# PyTorch2.1.0-cann7.0.0.alpha003_py_3.9-euler_2.8.3-64GB
docker_images=swr.cn-central-221.ovaijisuan.com/dxy/pytorch2_1_0_kernels:PyTorch2.1.0-cann7.0.0.alpha003_py_3.9-euler_2.8.3-64GB
model_dir=/home/niejz/work_dir/
docker run -it  -u root  --ipc=host --net=host \
        --device=/dev/davinci7 \
        --device=/dev/davinci_manager  \
        --device=/dev/devmm_svm  \
        --device=/dev/hisi_hdc  \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver   \
        -v /usr/local/dcmi:/usr/local/dcmi  \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi  \
        -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware  \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi  \
        -v ${model_dir}:${model_dir} \
        --entrypoint=/bin/bash   \
        ${docker_images} 
```



### Docker Image @6
```shell
# PyTorch2.1.0-cann7.0rc1_py_3.9-euler_2.8.3-64GB
docker_images=swr.cn-central-221.ovaijisuan.com/dxy/pytorch2_1_0:PyTorch2.1.0-cann7.0rc1_py_3.9-euler_2.8.3-64GB
model_dir=/home/niejz/work_dir/
docker run -it  -u root  --ipc=host --network=host \
        --device=/dev/davinci0  \
        --device=/dev/davinci_manager \
        --device=/dev/devmm_svm \
        --device=/dev/hisi_hdc \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver  \
        -v /usr/local/dcmi:/usr/local/dcmi \
        -v /usr/local/Ascend/toolbox:/usr/local/Ascend/toolbox  \
        -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
        -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
        -v ${model_dir}:${model_dir} \
        --entrypoint=/bin/bash \
        ${docker_images} 
```
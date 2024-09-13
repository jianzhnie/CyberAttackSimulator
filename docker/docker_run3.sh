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


# PyTorch2.1.0-cann7.0.0.alpha003_py_3.9-euler_2.8.3-64GB
docker_images=swr.cn-central-221.ovaijisuan.com/dxy/pytorch2_1_0_kernels:PyTorch2.1.0-cann7.0.0.alpha003_py_3.9-euler_2.8.3-64GB
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
        --entrypoint=/bin/bash   \
        ${docker_images} 

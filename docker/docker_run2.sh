# Change `device` upon your resources
docker_images=cybersim:v2
model_dir=/home/niejz/work_dir

docker run -it -u root --ipc=host --net=host \
        --name niejzh_PleaseDontStop \
        --device=/dev/davinci6 \
        --device=/dev/davinci_manager \
        --device=/dev/devmm_svm \
        --device=/dev/hisi_hdc \
        -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
        -v /usr/local/dcmi:/usr/local/dcmi   \
        -v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
        -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi   \
        -v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware  \
        -v ${model_dir}:${model_dir} \
        -v /var/log/npu:/usr/slog ${docker_images} \
        /bin/bash

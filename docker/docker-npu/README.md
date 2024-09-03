# Dockerfile 内容详解

## 1. 选择基础镜像

```dockerfile
# Use the Ubuntu 22.04 image with CANN 8.0.rc1
# More versions can be found at https://hub.docker.com/r/ascendai/cann/tags
# FROM ascendai/cann:8.0.rc1-910-openeuler22.03-py3.8
# FROM ascendai/cann:8.0.rc1-910b-openeuler22.03-py3.8
# FROM ascendai/cann:8.0.rc1-910-ubuntu22.04-py3.8
# FROM ascendai/cann:8.0.rc1-910-ubuntu22.04-py3.9
# FROM ascendai/cann:8.0.rc1-910b-ubuntu22.04-py3.8
# FROM ascendai/cann:8.0.rc1-910b-ubuntu20.04-py3.8
FROM ascendai/cann:8.0.rc1-910b-ubuntu22.04-py3.9
# FROM ascendai/cann:8.0.rc1-910b-ubuntu20.04-py3.9
```

- 基础镜像: 选择了一个基于 Ubuntu 22.04 和 CANN 8.0.rc1 的镜像。CANN（Compute Architecture for Neural Networks）是华为 Ascend AI 处理器的计算架构。这个镜像预装了一些与机器学习和深度学习相关的库和工具。

## 2. 设置环境变量

```dockerfile
# Define environments
ENV DEBIAN_FRONTEND=noninteractive
```

- `DEBIAN_FRONTEND=noninteractive:` 设置环境变量以使 Debian（或 Ubuntu）在安装软件包时不会提示用户进行交互。这通常用于自动化安装过程，确保 Docker 构建过程中不会停下来等待用户输入。

## 3. 定义构建参数

```dockerfile
# Define installation arguments
ARG INSTALL_DEEPSPEED=false
ARG PIP_INDEX=https://pypi.org/simple
ARG TORCH_INDEX=https://download.pytorch.org/whl/cpu
```

- `INSTALL_DEEPSPEED`: 构建参数，用于决定是否安装 deepspeed 包。默认为 false。
- `PIP_INDEX`: Python 包索引的 URL，用于设置 pip 默认的索引源。
- `TORCH_INDEX`: PyTorch 的包索引 URL，用于指定额外的索引源。

## 4. 设置工作目录

```dockerfile
# Set the working directory
WORKDIR /app
```

- ` WORKDIR /app`: 设置工作目录为 /app。所有后续的 `COPY` 和` RUN` 命令都会在这个目录下执行。

## 5. 安装依赖

```dockerfile
# Install the requirements
COPY requirements.txt /app
RUN pip config set global.index-url "$PIP_INDEX" && \
    pip config set global.extra-index-url "$TORCH_INDEX" && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt
```

- `COPY requirements.txt /app`: 将本地的 `requirements.txt` 文件复制到容器的 /app 目录中。
- `RUN pip config set ...`: 配置 pip 使用指定的索引 URL。
- `python -m pip install --upgrade pip`: 升级 pip 到最新版本。
- `python -m pip install -r requirements.txt`: 根据 requirements.txt 文件安装 Python 依赖。

## 6. 复制应用程序代码

```dockerfile
# Copy the rest of the application into the image
COPY . /app
```

- `COPY . /app`: 将当前目录下的所有文件复制到容器的 `/app ` 目录中。这通常包括应用程序的源代码和其他必要文件。

## 7. 安装 LLaMA Factory

```dockerfile
# Install the LLaMA Factory
RUN EXTRA_PACKAGES="torch-npu,metrics"; \
    if [ "$INSTALL_DEEPSPEED" == "true" ]; then \
    EXTRA_PACKAGES="${EXTRA_PACKAGES},deepspeed"; \
    fi; \
    pip install -e ".[$EXTRA_PACKAGES]"
```

- `EXTRA_PACKAGES`: 设置一个包含默认包 `torch-npu` 和 `metrics` 的变量。
- `if [ "$INSTALL_DEEPSPEED" == "true" ]`: 如果 `INSTALL_DEEPSPEED` 为 true，则将 `deepspeed` 包添加到 `EXTRA_PACKAGES` 中。
- `pip install -e ".[$EXTRA_PACKAGES]"`
  -e 表示以可编辑模式安装当前目录中的 Python 包。通常，这表示该目录包含一个 `setup.py `或 `pyproject.toml` 文件，定义了如何安装你的包。
  ".\[$EXTRA_PACKAGES\]" 是传递给 pip install 的选项，指定了要安装的附加依赖包。\`\`EXTRA_PACKAGES \`变量的值会在运行时被替换，从而将附加的包名传递给 pip。

## 8. 设置挂载点

```dockerfile
# Set up volumes
VOLUME [ "/root/.cache/huggingface", "/root/.cache/modelscope", "/app/data", "/app/output" ]
```

在 Dockerfile 中，VOLUME 指令用于创建一个或多个挂载点，将容器中的目录映射到主机系统中的目录。这使得你可以将容器的文件系统中的某些目录持久化或与其他容器共享数据。

- VOLUME ：创建并挂载容器中的这些目录为数据卷，确保这些目录中的数据在容器重启或删除后仍然保留。目录包括：

- `/root/.cache/huggingface`:

  - 这个目录通常用于存储 Hugging Face 相关的缓存数据，例如模型文件和其他下载的资源。
  - 将其设置为卷可以确保这些缓存数据在容器的不同生命周期间保持持久性。

- `/root/.cache/modelscope`:

  - 类似于 Hugging Face 的缓存目录，这是用于存储 ModelScope 框架的缓存数据。
  - 通过设置为卷，可以持久化这些数据，避免每次启动容器时重新下载。

- `/app/data`:

  - 这是一个应用程序数据目录，用于存储应用程序所需的数据文件。
  - 通过将其设置为卷，可以方便地将数据与容器中的应用程序分开管理，并允许数据持久化。

- `/app/output`:

  - 这是一个用于存储应用程序输出数据的目录。
  - 将其设置为卷使得应用程序生成的输出数据可以在容器重启或删除后继续保留。

## 9. 暴露端口

```dockerfile
# Expose port 7860 for the LLaMA Board
ENV GRADIO_SERVER_PORT 7860
EXPOSE 7860

# Expose port 8000 for the API service
ENV API_PORT 8000
EXPOSE 8000
```

- `ENV GRADIO_SERVER_PORT 7860`: 设置环境变量 `GRADIO_SERVER_PORT` 为 7860，用于指定 Gradio 服务器的端口。
- `EXPOSE 7860`: 暴露容器的 7860 端口，使得主机和其他容器可以访问这个端口。
- `ENV API_PORT 8000`: 设置环境变量 API_PORT 为 8000，用于指定 API 服务的端口。
- `EXPOSE 8000`: 暴露容器的 8000 端口。

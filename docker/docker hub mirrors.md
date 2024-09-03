# Docker Hub 镜像加速器

国内从 Docker Hub 拉取镜像有时会遇到困难，此时可以配置镜像加速器。

## 1️⃣ Docker daemon 配置代理（推荐）

参考 [Docker daemon 配置代理](https://docs.docker.com/config/daemon/systemd/#httphttps-proxy)

## 2️⃣ 自建镜像加速服务

- [自建镜像仓库代理服务](https://github.com/bboysoulcn/registry-mirror)
- [利用 Cloudflare Workers 自建 Docker Hub 镜像](https://github.com/ImSingee/hammal)

## 3️⃣ 国内三方加速镜像

> ⚠️⚠️⚠️ 自 2024-06-06 开始，国内的 Docker Hub 镜像加速器相继停止服务，可选择为 Docker daemon 配置代理或自建镜像加速服务。

创建或修改 `/etc/docker/daemon.json`：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json
{
    "registry-mirrors": [
        "https://dockerproxy.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://docker.nju.edu.cn"
    ]
}

sudo systemctl daemon-reload
sudo systemctl restart docker
```

### Docker Hub 镜像加速器列表

Docker 官方和国内很多云服务商都提供了国内加速器服务。以下镜像站来源于互联网（感谢热心网友），可能出现宕机、转内网、关停等情况，建议同时配置多个镜像源。

| 镜像加速器                                                                                                                         | 镜像加速器地址                            | 专属加速器[？](# "需登录后获取平台分配的专属加速器")                          | 其它加速[？](# "支持哪些镜像来源的镜像加速")                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [DaoCloud 镜像站](https://github.com/DaoCloud/public-image-mirror)                                                                 | `https://docker.m.daocloud.io`            | 白名单模式                                                                    | GCR、K8S、GHCR、Quay、NVCR 等                                                                                          |
| [Azure 中国镜像](https://github.com/Azure/container-service-for-azure-china/blob/master/aks/README.md#22-container-registry-proxy) | `https://dockerhub.azk8s.cn`              | [仅供内部访问](https://mirror.azk8s.cn/help/docker-registry-proxy-cache.html) | Docker Hub、GCR、Quay                                                                                                  |
| [科大镜像站](https://mirrors.ustc.edu.cn/help/dockerhub.html)                                                                      | `https://docker.mirrors.ustc.edu.cn`      | [仅供内部访问](https://mirrors.ustc.edu.cn/help/dockerhub.html)               | [GCR](https://github.com/ustclug/mirrorrequest/issues/91)、[Quay](https://github.com/ustclug/mirrorrequest/issues/135) |
| [阿里云](https://cr.console.aliyun.com)                                                                                            | `https://<your_code>.mirror.aliyuncs.com` | 需登录，系统分配                                                              | ~~Docker Hub~~                                                                                                         |
| [腾讯云](https://cloud.tencent.com/document/product/457/9113)                                                                      | `https://mirror.ccs.tencentyun.com`       | 仅供内部访问                                                                  | ~~Docker Hub~~                                                                                                         |
| [Docker 镜像代理](https://dockerproxy.com)                                                                                         | `https://dockerproxy.com`                 |                                                                               | Docker Hub、GCR、K8S、GHCR                                                                                             |
| [百度云](https://cloud.baidu.com/doc/CCE/s/Yjxppt74z#%E4%BD%BF%E7%94%A8dockerhub%E5%8A%A0%E9%80%9F%E5%99%A8)                       | `https://mirror.baidubce.com`             |                                                                               | ~~Docker Hub~~                                                                                                         |
| [南京大学镜像站](https://doc.nju.edu.cn/books/35f4a)                                                                               | `https://docker.nju.edu.cn`               |                                                                               | GCR、GHCR、Quay、NVCR 等                                                                                               |
| [中科院软件所镜像站](https://mirror.iscas.ac.cn/mirror/docker.html)                                                                | `https://mirror.iscas.ac.cn`              |                                                                               | ~~Docker Hub~~                                                                                                         |

## 检查加速器是否生效

命令行执行 `docker info`，如果从结果中看到了如下内容，说明配置成功。

```shell
Registry Mirrors:
 [...]
 https://docker.m.daocloud.io
```

## Docker Hub 镜像测速

使用镜像前后，可使用 `time` 统计所花费的总时间。测速前先移除本地的镜像！

```shell
docker rmi node:latest

time docker pull node:latest


Pulling repository node
[...]

real   1m14.078s
user   0m0.176s
sys    0m0.120s
```

## 参考链接

- https://docs.docker.com/registry/recipes/mirror/
- https://github.com/yeasy/docker_practice/blob/master/install/mirror.md
- https://github.com/moby/moby/blob/d409b05970e686993e343d226fae5b463d872082/docs/articles/registry_mirror.md
- https://www.fengbohello.top/archives/docker-registry-mirror
- https://www.ilanni.com/?p=14534
- https://github.com/Azure/container-service-for-azure-china/blob/master/aks/README.md#22-container-registry-proxy

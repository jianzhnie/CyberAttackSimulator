"""ASGI config for temp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/

这段代码是一个Django项目的ASGI（Asynchronous Server Gateway Interface）配置文件。
ASGI是Python异步Web服务器和Web应用之间的标准接口。与WSGI不同，ASGI支持异步功能，使其能够处理WebSockets等协议。

## 作用
- get_asgi_application函数用于设置Django的ASGI应用，这个函数返回一个可调用对象，用于处理请求。
这个application对象是ASGI服务器（例如 Daphne、Uvicorn、Hypercorn 等）用来与Django应用进行通信的接口。

## 在部署中的作用
当部署Django项目时，ASGI服务器将请求传递给这个ASGI应用对象。ASGI应用对象处理请求并返回响应。
这个配置文件在支持异步处理的环境中使用，允许Django项目处理异步请求和协议，如HTTP/2和WebSockets。
"""

from django.core.asgi import get_asgi_application

application = get_asgi_application()

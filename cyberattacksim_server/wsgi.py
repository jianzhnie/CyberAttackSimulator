"""WSGI config for cyberattacksim_gui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/


这段代码是一个Django项目的WSGI（Web Server Gateway Interface）配置文件。
WSGI是Python应用和Web服务器之间的接口标准。Django项目使用WSGI来处理Web服务器传入的请求。

- get_wsgi_application 函数用于设置Django的WSGI应用，这个函数返回一个可调用对象，用于处理请求。
这个application对象是WSGI服务器（例如Gunicorn、uWSGI或Django内置的开发服务器）用来与Django应用进行通信的接口。

在部署中的作用
- 当部署Django项目时，Web服务器将请求传递给这个WSGI应用对象。WSGI应用对象处理请求并返回响应。
- 这个配置文件通常在生产环境中使用，帮助Django项目与Web服务器对接，处理和响应客户端请求。
"""

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView

from cyberattacksim_gui.views.docs_view import DocsView
from cyberattacksim_gui.views.game_mode_config_view import GameModeConfigView
from cyberattacksim_gui.views.game_modes_view import GameModesView
from cyberattacksim_gui.views.home_view import HomeView
from cyberattacksim_gui.views.jupyter_view import JupyterView
from cyberattacksim_gui.views.network_creator_view import NetworkCreator
from cyberattacksim_gui.views.network_editor_view import NetworkEditor
from cyberattacksim_gui.views.networks_view import NetworksView
from cyberattacksim_gui.views.run_view import RunView
from cyberattacksim_gui.views.utils.helpers import get_docs_sections
from cyberattacksim_gui.views.utils.update_network_layout import \
    update_network_layout
from cyberattacksim_gui.views.utils.utils import (db_manager, get_output,
                                                  update_game_mode)

# 这段代码是一个Django项目中的URL配置模块，它定义了项目中不同的URL路径及其对应的视图。

# - staticfiles_urlpatterns: 用于为静态文件创建URL模式。
# - path: Django的URL路径函数，用于定义URL和视图的映射。
# - TemplateView: Django的通用视图，用于渲染静态模板。

# 每个path函数定义了一个URL路径及其对应的视图和名称。例如：
# - path('', HomeView.as_view(), name='Home')：当访问根URL时，调用HomeView视图。
# - path('docs/', DocsView.as_view(), name='docs')：当访问/docs/时，调用DocsView视图。

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('docs/', DocsView.as_view(), name='docs'),
    path('run/', RunView.as_view(), name='Run session'),
    path('docs/', DocsView.as_view(), name='Documentation'),
    path('jupyter/', JupyterView.as_view(), name='Jupyter Notebooks'),
    path('docs/<str:section>/', DocsView.as_view(), name='Documentation'),
    path('game_modes/', GameModesView.as_view(), name='Manage game modes'),
    path('networks/', NetworksView.as_view(), name='Manage networks'),
    path('network_creator', NetworkCreator.as_view(), name='network creator'),
    path(
        'network_creator/<str:network_id>/',
        NetworkCreator.as_view(),
        name='network creator',
    ),
    path(
        'game_mode_config/',
        GameModeConfigView.as_view(),
        name='game mode config',
    ),
    path(
        'game_mode_config/<str:game_mode_id>/',
        GameModeConfigView.as_view(),
        name='game mode config',
    ),
    path(
        'game_mode_config/<str:game_mode_id>/<str:section_name>/',
        GameModeConfigView.as_view(),
        name='game mode config',
    ),
    path('network_editor/', NetworkEditor.as_view(), name='network editor'),
    path('update_network_layout/',
         update_network_layout,
         name='update network layout'),
    path(
        'network_editor/<str:network_id>',
        NetworkEditor.as_view(),
        name='network editor',
    ),
    path('manage_db/', db_manager, name='db manager'),
    path('update_game_mode/', update_game_mode, name='update config'),
    path('output/', get_output, name='stderr'),
    path(
        'docs/index.html',
        TemplateView.as_view(template_name='docs/index.html'),
        name='docs index',
    ),
]

# 这段代码动态生成URL模式，用于文档的源文件页面。
# get_docs_sections函数返回文档的部分名称列表，然后为每个部分生成一个URL模式。

urlpatterns += [
    path(
        f'docs/source/{name}.html',
        TemplateView.as_view(template_name=f'docs/source/{name}.html'),
        name=f'docs_{name}',
    ) for name in get_docs_sections()
]

# 这几行代码为静态文件（如图片、模块、源文件和静态文件）添加URL模式，
# 使得Django可以在开发模式下正确地提供这些文件。
urlpatterns += staticfiles_urlpatterns()
urlpatterns += staticfiles_urlpatterns('docs/_images')
urlpatterns += staticfiles_urlpatterns('docs/_modules')
urlpatterns += staticfiles_urlpatterns('docs/_sources')
urlpatterns += staticfiles_urlpatterns('docs/_static')

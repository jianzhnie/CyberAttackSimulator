from django.urls import path

from cyberattacksim_gui.views.app_view import AppView
from cyberattacksim_gui.views.game_mode_config_view import GameModeConfigView
from cyberattacksim_gui.views.game_modes_view import GameModesView
from cyberattacksim_gui.views.home_view import HomeView
from cyberattacksim_gui.views.marl_view import MarlView
from cyberattacksim_gui.views.massive_network_run_view import \
    MassiveNetworkRunView
from cyberattacksim_gui.views.network_creator_view import NetworkCreator
from cyberattacksim_gui.views.network_editor_view import NetworkEditor
from cyberattacksim_gui.views.network_view import NetWorkView
from cyberattacksim_gui.views.networks_view import NetworksView
from cyberattacksim_gui.views.platform_view import PlatformView
from cyberattacksim_gui.views.run_view import RunView
from cyberattacksim_gui.views.utils.update_network_layout import \
    update_network_layout
from cyberattacksim_gui.views.utils.utils import (db_manager, get_output,
                                                  update_game_mode)
from cyberattacksim_gui.views.vrl_view import VrlView

# 这段代码是一个Django项目中的URL配置模块，它定义了项目中不同的URL路径及其对应的视图。

# - staticfiles_urlpatterns: 用于为静态文件创建URL模式。
# - path: Django的URL路径函数，用于定义URL和视图的映射。
# - TemplateView: Django的通用视图，用于渲染静态模板。

# 每个path函数定义了一个URL路径及其对应的视图和名称。例如：
# - path('', HomeView.as_view(), name='Home')：当访问根URL时，调用HomeView视图。
# - path('docs/', DocsView.as_view(), name='docs')：当访问/docs/时，调用DocsView视图。

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('network/', NetWorkView.as_view(), name='Network'),
    path('vrl/', VrlView.as_view(), name='Vrl'),
    path('marl/', MarlView.as_view(), name='Marl'),
    path('app/', AppView.as_view(), name='App'),
    path('platform/', PlatformView.as_view(), name='PlatForm'),
    path('run/', RunView.as_view(), name='Run session'),
    path(
        'massive_network/',
        MassiveNetworkRunView.as_view(),
        name='Massive Network Simulator',
    ),
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
]

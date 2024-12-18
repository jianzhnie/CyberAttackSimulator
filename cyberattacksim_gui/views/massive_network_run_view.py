from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from cyberattacksim_gui.forms.massive_network_form import MassiveNetworkForm
from cyberattacksim_gui.views.utils.helpers import get_toolbar
from cyberattacksim_gui.views.utils.massive_network_run import \
    MassiveNetworkRunManager


class MassiveNetworkRunView(View):
    """Django page template for CyberAttackSim Run class."""

    def get(self, request: HttpRequest, *args, **kwargs):
        """Handle page get requests.

        :param request: the Django page `request` object containing the html data for `run.html` and the server GET / POST request bodies.
        """
        form = MassiveNetworkForm()

        return render(
            request,
            'massive_network_run.html',
            {
                'form': form,
                'toolbar': get_toolbar('Massive Network Simulator'),
            },
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handle page POST requests."""
        form = MassiveNetworkForm(request.POST)
        if form.is_valid():
            fkwargs = form.cleaned_data
            MassiveNetworkRunManager.start_process(fkwargs=fkwargs)
            return JsonResponse({'message': 'complete'})
        return JsonResponse({'message': 'error'}, status=400)

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('servicos/', ServicosView.as_view(), name='servicos'),
    path('profissionais/', ProfissionaisView.as_view(), name='profissionais'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('agendamento/', AgendamentoView.as_view(), name='agendamento'),
    path('apoio-emocional/', ApoioEmocionalView.as_view(), name='apoio_emocional'),
]

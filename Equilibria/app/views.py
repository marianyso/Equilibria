from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    
    def post(self, request):
        pass

class SobreView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sobre.html')

class ServicosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'servicos.html')

class ProfissionaisView(View):
    def get(self, request, *args, **kwargs):
        # Buscar psicólogos do banco de dados
        psicologos = Psicologo.objects.all()
        context = {
            'psicologos': psicologos
        }
        return render(request, 'profissionais.html', context)

class BlogView(View):
    def get(self, request, *args, **kwargs):
        # Aqui você pode adicionar lógica para buscar artigos do blog
        # Por enquanto, o template usa dados estáticos
        return render(request, 'blog.html')

class ContatoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contato.html')
    
    def post(self, request, *args, **kwargs):
        # Processar formulário de contato
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        aceito_termos = request.POST.get('aceito_termos')
        aceito_newsletter = request.POST.get('aceito_newsletter')
        
        if not all([nome, email, assunto, mensagem, aceito_termos]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'contato.html')
        
        try:
            # Aqui você pode salvar no banco de dados ou enviar por email
            # Por enquanto, vamos apenas simular o envio
            
            # Exemplo de envio de email (descomente se configurar SMTP)
            # send_mail(
            #     subject=f'Contato - {assunto}',
            #     message=f'Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\n\nMensagem:\n{mensagem}',
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=['contato@equilibria.com.br'],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('contato')
            
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao enviar sua mensagem. Tente novamente.')
            return render(request, 'contato.html')

# Views para funcionalidades específicas do site psicológico
class AgendamentoView(View):
    def get(self, request, *args, **kwargs):
        # Buscar psicólogos disponíveis
        psicologos = Psicologo.objects.all()
        context = {
            'psicologos': psicologos
        }
        return render(request, 'agendamento.html', context)
    
    def post(self, request, *args, **kwargs):
        # Processar agendamento de consulta
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para agendar uma consulta.')
            return redirect('login')
        
        psicologo_id = request.POST.get('psicologo')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        
        if not all([psicologo_id, data, horario]):
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('agendamento')
        
        try:
            psicologo = get_object_or_404(Psicologo, id=psicologo_id)
            
            # Verificar se já existe consulta no mesmo horário
            consulta_existente = Consulta.objects.filter(
                id_psicologo=psicologo,
                data=data,
                horario=horario,
                status='agendada'
            ).exists()
            
            if consulta_existente:
                messages.error(request, 'Este horário já está ocupado. Escolha outro horário.')
                return redirect('agendamento')
            
            # Criar nova consulta
            consulta = Consulta.objects.create(
                id_usuario=request.user,
                id_psicologo=psicologo,
                data=data,
                horario=horario,
                status='agendada'
            )
            
            messages.success(request, f'Consulta agendada com sucesso para {data} às {horario} com {psicologo.nome}!')
            return redirect('agendamento')
            
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao agendar a consulta. Tente novamente.')
            return redirect('agendamento')

class ApoioEmocionalView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'apoio_emocional.html')
    
    def post(self, request, *args, **kwargs):
        # Processar interação com IA
        mensagem_usuario = request.POST.get('mensagem')
        
        if not mensagem_usuario:
            return JsonResponse({'error': 'Mensagem não pode estar vazia'}, status=400)
        
        try:
            # Aqui você integraria com uma API de IA real
            # Por enquanto, vamos simular uma resposta
            resposta_ia = self.gerar_resposta_ia(mensagem_usuario)
            
            # Salvar interação no banco se usuário estiver logado
            if request.user.is_authenticated:
                InteracaoIA.objects.create(
                    id_usuario=request.user,
                    mensagem_usuario=mensagem_usuario,
                    resposta_ia=resposta_ia
                )
            
            return JsonResponse({
                'resposta': resposta_ia,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
    
    def gerar_resposta_ia(self, mensagem):
        # Simulação de resposta da IA
        # Em um ambiente real, você integraria com OpenAI, Anthropic, etc.
        respostas_exemplo = [
            "Entendo que você está passando por um momento difícil. É importante reconhecer seus sentimentos. Que tal tentarmos um exercício de respiração?",
            "Obrigado por compartilhar isso comigo. Seus sentimentos são válidos. Como posso te ajudar melhor neste momento?",
            "Percebo que você está enfrentando desafios. Lembre-se de que buscar ajuda é um sinal de força, não de fraqueza.",
            "É normal sentir-se assim às vezes. Vamos trabalhar juntos para encontrar estratégias que possam te ajudar.",
        ]
        
        # Lógica simples baseada em palavras-chave
        mensagem_lower = mensagem.lower()
        
        if any(palavra in mensagem_lower for palavra in ['ansioso', 'ansiedade', 'nervoso']):
            return "Entendo que você está sentindo ansiedade. Vamos tentar um exercício de respiração: inspire por 4 segundos, segure por 4, expire por 6. Repita algumas vezes. Como você está se sentindo agora?"
        
        elif any(palavra in mensagem_lower for palavra in ['triste', 'deprimido', 'sozinho']):
            return "Sinto muito que você esteja se sentindo assim. Seus sentimentos são válidos e você não está sozinho. Às vezes, conversar sobre o que está acontecendo pode ajudar. Gostaria de me contar mais sobre o que está te deixando triste?"
        
        elif any(palavra in mensagem_lower for palavra in ['estresse', 'estressado', 'pressão']):
            return "O estresse pode ser muito desafiador. Uma técnica que pode ajudar é a regra 5-4-3-2-1: identifique 5 coisas que você pode ver, 4 que pode tocar, 3 que pode ouvir, 2 que pode cheirar e 1 que pode saborear. Isso pode te ajudar a se conectar com o momento presente."
        
        else:
            import random
            return random.choice(respostas_exemplo)

from django.utils import timezone

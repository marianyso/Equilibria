from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # O AbstractUser já inclui username, email, first_name, last_name, password, etc.
    # Podemos adicionar campos extras se necessário, mas os básicos já estão cobertos.
    # Se quiser usar email como campo único principal, pode ser necessário ajustar settings.py
    pass

    def __str__(self):
        return self.username # ou self.get_full_name() se preferir

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Psicologo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Psicólogo")
    # Outros campos relevantes para o psicólogo podem ser adicionados aqui
    # Ex: CRP, especialidades, etc.
    # Para simplificação inicial, apenas o nome foi considerado baseado nos requisitos.
    # Se for necessário vincular a um usuário do sistema, adicione:
    # usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Psicólogo"
        verbose_name_plural = "Psicólogos"


class Consulta(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    id_psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, verbose_name="Psicólogo")
    data = models.DateField(verbose_name="Data da Consulta")
    horario = models.TimeField(verbose_name="Horário da Consulta")
    # Considerando status como CharField para maior flexibilidade (ex: 'agendada', 'cancelada', 'realizada')
    status = models.CharField(max_length=20, default='agendada', verbose_name="Status da Consulta")

    def __str__(self):
        return f"Consulta de {self.id_usuario} com {self.id_psicologo} em {self.data} às {self.horario}"

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"


class Agenda(models.Model):
    id_psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, verbose_name="Psicólogo")
    # Armazenando dias disponíveis como um campo de texto. Pode ser refinado para JSONField ou modelo separado.
    dias_disponiveis = models.TextField(verbose_name="Dias Disponíveis") # Ex: "segunda, quarta, sexta"
    # Armazenando horários disponíveis como um campo de texto. Pode ser refinado para JSONField ou modelo separado.
    horarios_disponiveis = models.TextField(verbose_name="Horários Disponíveis") # Ex: "09:00-12:00, 14:00-17:00"

    def __str__(self):
        return f"Agenda de {self.id_psicologo}"

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"


class InteracaoIA(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem_usuario = models.TextField(verbose_name="Mensagem do Usuário")
    resposta_ia = models.TextField(verbose_name="Resposta da IA")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora da Interação")

    def __str__(self):
        return f"Interação de {self.id_usuario} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Interação com IA"
        verbose_name_plural = "Interações com IA"


class Notificacao(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem = models.TextField(verbose_name="Mensagem da Notificação")
    data_envio = models.DateTimeField(verbose_name="Data/Hora de Envio")
    # Pode-se adicionar um campo para indicar se foi lida
    lida = models.BooleanField(default=False, verbose_name="Lida")

    def __str__(self):
        return f"Notificação para {self.id_usuario} - {self.data_envio.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"


class Avaliacao(models.Model):
    # Avaliação está ligada à consulta, pois é pós-atendimento
    id_consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, verbose_name="Consulta")
    nota = models.IntegerField(verbose_name="Nota") # Assumindo nota numérica, pode ser de 1 a 5
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentário")

    def __str__(self):
        return f"Avaliação da consulta {self.id_consulta.id} - Nota: {self.nota}"

    class Meta:
        # Garantindo que um usuário só possa avaliar uma consulta uma vez (via restrição no banco)
        unique_together = ('id_consulta',)
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

# Observações:
# 1. A tabela 'Atendimento' do diagrama original parece corresponder às 'InteracoesIA'.
# 2. A tabela 'Autoavaliação Emocional' não foi modelada explicitamente, pois seu resultado
#    parece ser usado para direcionar o atendimento da IA, podendo ser armazenado em InteracaoIA
#    ou em um campo específico do usuário se for persistente.
# 3. A funcionalidade de 'Autoavaliação Emocional' pode ser implementada como uma lógica
#    no frontend/backend que utiliza a IA ou retorna conteúdo específico baseado nas respostas,
#    sem necessariamente precisar de uma tabela dedicada.
# 4. A tabela 'Administrador' não foi incluída, pois o Django já possui um sistema de admin
#    que pode ser usado com o modelo Usuario ou um modelo de grupo/permissão.
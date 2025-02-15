from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


def emitente_upload_file(instance, filename):
    if instance.cnpj:
        doc = instance.cnpj
    else:
        doc = instance.cpf

    path: str = f"{doc}/media/"
    path += filename
    return path


class Emitente(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    nome = models.CharField('Nome', max_length=60)
    cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
    inscricao_estadual = models.CharField('Inscrição Estadual', max_length=14, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    logradouro = models.CharField(max_length=60)
    numero = models.CharField(max_length=40)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    bairro = models.CharField(max_length=60)
    municipio = models.CharField(max_length=60)
    uf = models.CharField('UF', max_length=2)
    cep = models.CharField('CEP', max_length=8)
    telefones = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField('E-mail', max_length=100, null=True, blank=True)
    certificado_a1 = models.FileField(upload_to=emitente_upload_file, null=True, blank=True)
    logotipo_dfe = models.ImageField(upload_to=emitente_upload_file, null=True, blank=True)

    # DFe's - Controle de Emissões, séries e numeração ambiente Produção & Homologação (testes)

    nfe_emite = models.BooleanField('Emite NFe', default=False)
    nfe_serie = models.IntegerField('Série NFe', default=0)
    nfe_numero = models.IntegerField('Número NFe', default=0)
    nfe_serie_homologacao = models.IntegerField('Série NFe em homologação', default=0)
    nfe_numero_homologacao = models.IntegerField('Número NFe em homologação', default=0)

    nfce_emite = models.BooleanField('Emite NFCe', default=False)
    nfce_serie = models.IntegerField('Série NFCe', default=0)
    nfce_numero = models.IntegerField('Número NFCe', default=0)
    nfce_serie_homologacao = models.IntegerField('Série NFCe em homologação', default=0)
    nfce_numero_homologacao = models.IntegerField('Número NFCe em homologação', default=0)

    cte_emite = models.BooleanField('Emite CTe', default=False)
    cte_serie = models.IntegerField('Série CTe', default=0)
    cte_numero = models.IntegerField('Número CTe', default=0)
    cte_serie_homologacao = models.IntegerField('Série CTe', default=0)
    cte_numero_homologacao = models.IntegerField('Número CTe em homologação', default=0)

    mdfe_emite = models.BooleanField('Emite MDFe', default=False)
    mdfe_serie = models.IntegerField('Série MDFe', default=0)
    mdfe_numero = models.IntegerField('Número MDFe', default=0)
    mdfe_serie_homologacao = models.IntegerField('Série MDFe em homologação', default=0)
    mdfe_numero_homologacao = models.IntegerField('Número MDFe em homologação', default=0)

    # Token de autenticação enviado ao Emitente/ERP/TMS para acesso a API

    token = models.UUIDField(default=uuid4, editable=False)

    # Limites: Número de créditos restantes de solicitações (requests) para o período atual, decrescente
    requests_credit = models.IntegerField('Crédito Requisições', default=100)
    # Número de segundos inicial da contagem do cronômetro até 60 segundos para até 100 solicitações
    requests_timer = models.IntegerField('Cronômetro de Requisições', default=0)

    """
    emissoes_suspensas: Se ativo, suspende as emissões dos DFes acima selecionados.
    Motivos: 
        - Manutenção
        - Suspensão de um ou mais serviços solicitado pelo emitente
        - Cobrança: Falta de pagamento
    """
    emissoes_suspensas = models.BooleanField('Suspender Emissões', default=False)
    is_active = models.BooleanField('Emitente Ativo', default=True,
                                    help_text='Emitentes inativos não aparecem no sistema (api)')
    created_at = models.DateField('Cadastrado Em', auto_now_add=True)

    def __str__(self):
        return self.nome

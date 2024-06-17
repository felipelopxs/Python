from constantes import ACESSO, PASTA_DE_TRABALHO
from datetime import datetime, time
from typing import List
from tqdm import tqdm
import time as t
import pyodbc
import os

QTDE_DE_LINHAS_POR_EXECUCAO: int = 1
HORARIO_DE_INICIO = time(18, 0, 0)
HORARIO_DE_FINALIZACAO = time(7, 30, 0)

def obter_comandos(id_cliente: str) -> List:
    conexao = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=***.database.windows.net;"
        "DATABASE=***_producao;"
        f"UID={ACESSO['user']};"
        f"PWD={ACESSO['pass']}"
        )
    cursor = conexao.cursor()
    cursor.execute(
        """
        DECLARE @IdCliente UNIQUEIDENTIFIER = ?;

        SELECT		*
        FROM		(
                    SELECT	DISTINCT 1 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.Documento WHERE Id = ''',d.Id,''';') AS 'ComandoSQL'
                    FROM	GedDocumento.Documento d
                    WHERE	d.IdCliente = @IdCliente
                    UNION ALL
                    SELECT		DISTINCT 2 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItem WHERE Id = ''',si.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    UNION ALL
                    SELECT		DISTINCT 2 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItem WHERE Id = ''',si.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    UNION ALL
                    SELECT		DISTINCT 3 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItemAtendimentoDocumento WHERE Id = ''',siad.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoDocumento siad ON siad.IdSolicitacaoItem = si.Id
                    UNION ALL
                    SELECT		DISTINCT 3 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItemAtendimentoDocumento WHERE Id = ''',siad.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoDocumento siad ON siad.IdSolicitacaoItem = si.Id
                    UNION ALL
                    SELECT		DISTINCT 4 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItemAtendimentoCaixa WHERE Id = ''',siac.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoCaixa siac ON siac.IdSolicitacaoItem = si.Id
                    UNION ALL
                    SELECT		DISTINCT 4 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItemAtendimentoCaixa WHERE Id = ''',siac.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoCaixa siac ON siac.IdSolicitacaoItem = si.Id
                    UNION ALL
                    SELECT		DISTINCT 5 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.SolicitacaoItemAtendimentoImagem WHERE IdImagem = ''',siai.IdImagem,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoImagem siai ON siai.IdImagem = i.Id
                    UNION ALL
                    SELECT		DISTINCT 6 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItem WHERE Id = ''',di.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.DevolucaoItem di ON di.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    UNION ALL
                    SELECT		DISTINCT 6 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItem WHERE Id = ''',di.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.DevolucaoItem di ON di.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    UNION ALL
                    SELECT		DISTINCT 7 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItemTmp WHERE Id = ''',dit.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoDocumento siad ON siad.IdSolicitacaoItem = si.Id
                    INNER JOIN	GedRequisicao.DevolucaoItemTmp dit ON dit.IdSolicitacaoItemAtendimentoDocumento = siad.Id
                    UNION ALL
                    SELECT		DISTINCT 7 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItemTmp WHERE Id = ''',dit.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoDocumento siad ON siad.IdSolicitacaoItem = si.Id
                    INNER JOIN	GedRequisicao.DevolucaoItemTmp dit ON dit.IdSolicitacaoItemAtendimentoDocumento = siad.Id
                    UNION ALL
                    SELECT		DISTINCT 7 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItemTmp WHERE Id = ''',dit.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoCaixa siac ON siac.IdSolicitacaoItem = si.Id
                    INNER JOIN	GedRequisicao.DevolucaoItemTmp dit ON dit.IdSolicitacaoItemAtendimentoCaixa = siac.Id
                    UNION ALL
                    SELECT		DISTINCT 7 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItemTmp WHERE Id = ''',dit.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedRequisicao.SolicitacaoItem si ON si.IdCaixa = d.IdCaixa AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedRequisicao.SolicitacaoItemAtendimentoCaixa siac ON siac.IdSolicitacaoItem = si.Id
                    INNER JOIN	GedRequisicao.DevolucaoItemTmp dit ON dit.IdSolicitacaoItemAtendimentoCaixa = siac.Id
                    UNION ALL
                    SELECT		DISTINCT 0 AS 'Ordem', CONCAT('DELETE FROM GedCaixa.Caixa WHERE Id = ''',cx.Id,''';') AS 'ComandoSQL'
                    FROM		GedCaixa.Caixa cx
                    WHERE		cx.IdCliente = @IdCliente OR
                                cx.IdUnidadeCliente IN (SELECT Id FROM GedHierarquia.UnidadeCliente uc WHERE uc.IdCliente = @IdCliente)
                    UNION ALL
                    SELECT		DISTINCT 8 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.PedidoCaixaNovaItem WHERE Id = ''',pcni.Id,''';') AS 'ComandoSQL'
                    FROM		GedCaixa.Caixa cx
                    INNER JOIN	GedRequisicao.PedidoCaixaNovaItem pcni ON pcni.IdCaixa = cx.Id AND
                                (cx.IdCliente = @IdCliente OR
                                cx.IdUnidadeCliente IN (SELECT Id FROM GedHierarquia.UnidadeCliente uc WHERE uc.IdCliente = @IdCliente))
                    UNION ALL
                    SELECT		DISTINCT 9 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.DownloadMassaImagem WHERE IdImagem = ''',dmi.IdImagem,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedDocumento.DownloadMassaImagem dmi ON dmi.IdImagem = i.Id
                    UNION ALL
                    SELECT		DISTINCT 10 AS 'Ordem', CONCAT('DELETE FROM GedWorkflow.WorkflowEtapaAnexoAssinatura WHERE Id = ''',weaa.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedWorkflow.WorkflowEtapaAnexoAssinatura weaa ON weaa.IdImagem = i.Id
                    UNION ALL
                    SELECT		DISTINCT 11 AS 'Ordem', CONCAT('UPDATE GedWorkflow.Workflow SET IdImagem = NULL WHERE Id = ''',w.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedWorkflow.Workflow w ON w.IdImagem = i.Id
                    UNION ALL
                    SELECT		DISTINCT 12 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.CapturaCertificado WHERE Id = ''',cc.Id,''';') AS 'ComandoSQL'
                    FROM		GedDocumento.Documento d
                    INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
                                d.IdCliente = @IdCliente
                    INNER JOIN	GedDocumento.CapturaCertificado cc ON cc.IdImagem = i.Id
                    UNION ALL
                    SELECT		DISTINCT 0 AS 'Ordem', CONCAT('UPDATE GedEndereco.Endereco SET Utilizado = 0 WHERE Id = ''',ed.Id,''';') AS 'ComandoSQL'
                    FROM		GedCaixa.Caixa cx
                    INNER JOIN	GedEndereco.Endereco ed ON ed.Id = cx.IdEndereco AND
                                cx.IdUnidadeCliente IN (SELECT Id FROM GedHierarquia.UnidadeCliente uc WHERE uc.IdCliente = @IdCliente)
                    ) cmd
        ORDER BY	cmd.Ordem DESC;
        """, (id_cliente)
        )
    
    resultado = [i[1] for i in cursor.fetchall()]
    cursor.close()
    conexao.close()
    
    return resultado

def executar(comandos_sql):
    
    comando_para_executar: str = comandos_sql
    conexao = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=***.database.windows.net;"
        "DATABASE=***_producao;"
        f"UID={ACESSO['user']};"
        f"PWD={ACESSO['pass']}"
        )
    cursor = conexao.cursor()
    cursor.execute(comando_para_executar)
    cursor.commit()
    conexao.commit()
    cursor.close()
    conexao.close()
    

clientes = ["21DB61A3-A6FB-4123-8023-***********",]    

for cliente in clientes:
    comandos_para_executar = obter_comandos(id_cliente=cliente)

    loop_externo: bool = True    
    while loop_externo:
        if len(comandos_para_executar) > 0:
            lista_de_linhas_de_comandos: List = [comandos_para_executar[i:i+QTDE_DE_LINHAS_POR_EXECUCAO] for i in range(0, len(comandos_para_executar), QTDE_DE_LINHAS_POR_EXECUCAO)]
            qtde_de_partes = len(lista_de_linhas_de_comandos)
            
            for comando in tqdm(lista_de_linhas_de_comandos, total=len(lista_de_linhas_de_comandos), desc="PROGRESSO"):
                novo_comando = "".join(comando).replace("\n", " ")
                loop_interno: bool = True
                
                while loop_interno:
                    if datetime.now().time() >= HORARIO_DE_INICIO or datetime.now().time() <= HORARIO_DE_FINALIZACAO:
                        hora_atual: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        try:
                            executar(comandos_sql=novo_comando)
                            
                        except Exception as e:
                            e = str(e).replace("\n", " ")
                            with open(
                                file=os.path.join(PASTA_DE_TRABALHO, "logs", "log_de_erro.txt"),
                                mode="a",
                                encoding="utf-8"
                                ) as log_de_erro:
                                log_de_erro.write(f"""Erro! | {hora_atual} | {novo_comando} | {e}\n""")
                        
                        with open(
                            file=os.path.join(PASTA_DE_TRABALHO, "logs", "log_de_sucesso.txt"),
                            mode="a",
                            encoding="utf-8"
                            ) as log_de_sucesso:
                            log_de_sucesso.write(f"""{hora_atual} | {novo_comando}\n""")
                            
                        loop_interno: bool = False
                            
                    else:
                        t.sleep(900)        
        else:
            loop_externo: bool = False
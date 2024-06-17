# IMPORTANDO BIBLIOTECAS DE TERCEIROS
import os
import pyodbc
import pandas as pd
from tqdm import tqdm
from typing import List, Dict



# SUPERCLASSE DE CONEXÃO COM O BANCO DE DADOS
class Conexao:
    def __init__(self) -> None:
        self.__conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=***.database.windows.net;'
            'Database=***_producao;'
            'Uid=***;'
            'Pwd=Mig@***$17;'
        )
           
# CLASSES PARA REALIZAR AÇÕES ESPECÍFICAS NO BANCO
class CamposCustomizados(Conexao):

    def __init__(self, id_cliente: str) -> None:
        super().__init__()
        self.__cursor = self._Conexao__conn.cursor()      
        self.__cursor.execute(
            f"""
            SELECT	(
                    SELECT	STRING_AGG(CONVERT(NVARCHAR(MAX), s.TEXT_SELECT), ', ') AS 'SELECT'
                    FROM	(
                            SELECT		DISTINCT CONCAT('ISNULL(dcc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.Valor,'''') AS ''CC_',cc.nome,'''') AS 'TEXT_SELECT'
                            FROM		GedConfCliente.CampoCustomizado cc
                            INNER JOIN	GedHierarquia.Cliente c              ON c.Id = cc.IdCliente
                            INNER JOIN	GedSistema.DefinicaoCamposCultura dc ON dc.IdDefinicaoCampos = cc.IdDefinicaoDeCampo 
                                        AND dc.IdCultura = 1
                            WHERE		cc._del IS NULL
                                        AND cc.IdCliente = '{id_cliente}'
                                        AND cc.Id IN (SELECT		DISTINCT IdcampoCustomizado 
                                                        FROM			Geddocumento.DocumentoCampoCustomizado dcc 
                                                        INNER JOIN	Geddocumento.Documento d ON d.Id = dcc.Iddocumento 
                                                        WHERE			d.IdCliente = '{id_cliente}')
                            ) s
                    ) AS 'SELECT',
                    (
                    SELECT	STRING_AGG(CONVERT(NVARCHAR(MAX), s.TEXT_LEFT), ' ') AS 'LEFT'
                    FROM	(
                            SELECT		DISTINCT CONCAT('LEFT JOIN GedDocumento.DocumentoCampoCustomizado dcc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),' ON d.Id = dcc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.IdDocumento AND dcc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.IdCampoCustomizado = ''',cc.Id,'''') AS 'TEXT_LEFT'
                            FROM		GedConfCliente.CampoCustomizado cc
                            INNER JOIN	GedHierarquia.Cliente c              ON c.Id = cc.IdCliente
                            INNER JOIN	GedSistema.DefinicaoCamposCultura dc ON dc.IdDefinicaoCampos = cc.IdDefinicaoDeCampo 
                                        AND dc.IdCultura = 1
                            WHERE		cc._del IS NULL
                                        AND cc.IdCliente = '{id_cliente}'
                                        AND cc.Id IN (SELECT		DISTINCT IdcampoCustomizado 
                                                        FROM			Geddocumento.DocumentoCampoCustomizado dcc 
                                                        INNER JOIN	Geddocumento.Documento d ON d.Id = dcc.Iddocumento 
                                                        WHERE			d.IdCliente = '{id_cliente}')
                            ) s
                    ) AS 'LEFT',
                    (
                    SELECT	STRING_AGG(CONVERT(NVARCHAR(MAX), s.TEXT_GROUPBY), ', ') AS 'GROUP_BY'
                    FROM	(
                            SELECT		DISTINCT CONCAT('dcc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.Valor') AS 'TEXT_GROUPBY'
                            FROM		GedConfCliente.CampoCustomizado cc
                            INNER JOIN	GedHierarquia.Cliente c              ON c.Id = cc.IdCliente
                            INNER JOIN	GedSistema.DefinicaoCamposCultura dc ON dc.IdDefinicaoCampos = cc.IdDefinicaoDeCampo 
                                        AND dc.IdCultura = 1
                            WHERE		cc._del IS NULL
                                        AND cc.IdCliente = '{id_cliente}'
                                        AND cc.Id IN (SELECT		DISTINCT IdcampoCustomizado 
                                                        FROM			Geddocumento.DocumentoCampoCustomizado dcc 
                                                        INNER JOIN	Geddocumento.Documento d ON d.Id = dcc.Iddocumento 
                                                        WHERE			d.IdCliente = '{id_cliente}')
                            ) s
                    ) AS 'GROUP_BY';
            """
        )
        self.__resultado = self.__cursor.fetchone()
        self.__cursor.close()
        self._Conexao__conn.close()
        
    @property
    def get_blocos(self) -> dict:
        dados: dict = {
            "select": self.__resultado[0],
            "left": self.__resultado[1],
            "group_by": self.__resultado[2]
        }
    
        return dados
        
class CamposDeLista(Conexao):

    def __init__(self, id_cliente: str) -> None:
        super().__init__()
        self.__cursor = self._Conexao__conn.cursor()    
        self.__cursor.execute(
            f"""
            SELECT	(
                    SELECT	STRING_AGG(CONVERT(NVARCHAR(MAX), s.TEXT_SELECT), ', ') AS 'SELECT'
                    FROM	(
                            SELECT		DISTINCT CONCAT('MAX(ISNULL(llc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.Valor,'''')) AS ''CL_',lc.Nome,'''') AS 'TEXT_SELECT'
                            FROM		GedLista.Campo lc 
                            INNER JOIN	GedLista.Lista l ON l.id = lc.IdLista AND lc._del IS NULL
                            INNER JOIN	GedHierarquia.Cliente c ON c.Id = l.IdCliente
                            INNER JOIN	GedSistema.DefinicaoCamposCultura dcc ON dcc.IdDefinicaoCampos = lc.IdDefinicaoCampos AND dcc.IdCultura = 1 
                            WHERE		l.Id IN (
                                                SELECT	DISTINCT Id 
                                                FROM	GedLista.Lista 
                                                WHERE	IdCliente = '{id_cliente}'
                                                )
                            ) s
                    ) AS 'SELECT',
                    (
                    SELECT	STRING_AGG(CONVERT(NVARCHAR(MAX), s.TEXT_LEFT), ' ') AS 'SELECT'
                    FROM	(
                            SELECT		DISTINCT CONCAT('LEFT JOIN GedLista.LinhaListaCampo llc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),' ON dll.IdLinhaLista = llc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.IdLinhaLista AND llc',ROW_NUMBER() OVER(ORDER BY c.NomeFantasia),'.IdCampo = ''',lc.Id,'''') AS 'TEXT_LEFT'
                            FROM		GedLista.Campo lc 
                            INNER JOIN	GedLista.Lista l ON l.id = lc.IdLista AND lc._del IS NULL
                            INNER JOIN	GedHierarquia.Cliente c ON c.Id = l.IdCliente
                            INNER JOIN	GedSistema.DefinicaoCamposCultura dcc ON dcc.IdDefinicaoCampos = lc.IdDefinicaoCampos AND dcc.IdCultura = 1 
                            WHERE		l.Id IN (
                                                SELECT	Id 
                                                FROM	GedLista.Lista 
                                                WHERE	IdCliente = '{id_cliente}'
                                                )
                            ) s
                    ) AS 'LEFT';
            """
        )
        self.__resultado = self.__cursor.fetchone()
        self.__cursor.close()
        self._Conexao__conn.close()
        
    @property
    def get_blocos(self) -> dict:
        dados: dict = {
            "select": "{}".format(self.__resultado[0]),
            "left": "{}".format(self.__resultado[1])
        }
    
        return dados
    
class Backup(Conexao):
    
    def __init__(self, id_cliente: str, where_personalizado: str, incluir_imagens: bool) -> None:

        self.__imagens: Dict = {
            "select_imagens": """CASE WHEN i.Id IS NOT NULL THEN CONCAT('Arquivos/', d.Codigo, ' - ', REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(i.Nome, '\', ''), '/', ''), '|', ''), '<', ''), '>', ''), '*', ''), ':', ''), '"', ''), '?', '') , '''', ''), CONCAT('.', ex.Extensao), ''), '.', LOWER(ex.Extensao)) ELSE '' END AS 'Arquivo',""" if incluir_imagens == True else "",
            "select_concat": """CASE WHEN i.Id IS NOT NULL THEN CONCAT(d.Codigo, ' - ', CONCAT(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(i.Nome, '\', ''), '/', ''), '|', ''), '<', ''), '>', ''), '*', ''), ':', ''), '"', ''), '?', '') , '''', ''), CONCAT('.', ex.Extensao), ''), '.', LOWER(ex.Extensao)), '|@#', LOWER(i.Id), '.', LOWER(ex.Extensao)) ELSE '' END AS 'CONCAT_APP'""" if incluir_imagens == True else "",
            "left_imagens": """LEFT JOIN GedDocumento.Imagem i ON d.id = i.IdDocumento AND i._del IS NULL AND i.DataExclusao IS NULL LEFT JOIN GedSistema.Extensao ex ON ex.Id = i.IdExtensao""" if incluir_imagens == True else ""
        }
        
        self.__inst_campos_customizados = CamposCustomizados(id_cliente)
        self.__dados_campos_customizados: dict = self.__inst_campos_customizados.get_blocos
        self.__select_campo_customizado: str = "" if self.__dados_campos_customizados['select'] is None or self.__dados_campos_customizados['select'] == "" else f"{self.__dados_campos_customizados['select']},"
        self.__left_campo_customizado: str = "" if self.__dados_campos_customizados['left'] is None or self.__dados_campos_customizados['left'] == "" else self.__dados_campos_customizados["left"]
        
        self.__inst_campos_de_lista = CamposDeLista(id_cliente)
        self.__dados_campos_de_lista: dict = self.__inst_campos_de_lista.get_blocos
        self.__select_campo_de_lista: str = "" if self.__dados_campos_de_lista['select'] == "None" or self.__dados_campos_de_lista['select'] == "" else f",{self.__dados_campos_de_lista['select']}"
        self.__left_campo_de_lista: str = "" if self.__dados_campos_de_lista['left'] == "None" or self.__dados_campos_de_lista['left'] == "" else self.__dados_campos_de_lista["left"]

        __group_by_padrao: List = ["d.Codigo", "cx1.Codigo", "cx3.Codigo", "cx2.Codigo", "edu1.Label", "edu2.Label", "edc1.Label", "edc2.Label", "ao.LabelArvoreCompleta", "d.DataCadastro", "u.Nome", "i.Nome", "ex.Extensao", "i.Id"]

        if incluir_imagens is False:
            __group_by_padrao.remove("i.Nome")
            __group_by_padrao.remove("ex.Extensao")
            __group_by_padrao.remove("i.Id")

        self.__group_by_personalizado: str = "" if self.__dados_campos_de_lista['left'] == "None" or self.__dados_campos_de_lista['left'] == "" else f"GROUP BY {', '.join(__group_by_padrao)}, {self.__dados_campos_customizados['group_by']}"

        self.__documentos = f"""
            SELECT      DISTINCT d.Id AS 'IdDocumento'
            FROM        GedDocumento.Documento d
            INNER JOIN  GedConfCliente.ArvoreOrganizacional ao ON ao.Id = d.IdArvoreOrganizacional AND
                        d.IdDocumentoStatus NOT IN (4, 7, 8) AND
                        ao._del IS NULL
            WHERE       d.IdCliente = '{id_cliente}'
                        {where_personalizado}
        """

        super().__init__()
        self.__cursor = self._Conexao__conn.cursor()
        self.__cursor.execute(self.__documentos)

        self.__lista_de_documentos: List = [i[0] for i in self.__cursor.fetchall()]
        self.__lista_paginada: List = [self.__lista_de_documentos[i:i+1000] for i in range(0, len(self.__lista_de_documentos), 1000)]

        self.__cursor.close()
        self._Conexao__conn.close()

        __colunas: List = []
        __dados: List = []

        print(f"\nGERANDO METADADOS PAGINADOS ({len(self.__lista_paginada)} PARTES DE 1000 ITENS).")
        for index, lista in tqdm(enumerate(self.__lista_paginada), total=len(self.__lista_paginada), desc="PROGRESSO"):

            __lista = f"""('{"', '".join(lista)}')"""
            self.__consulta = f"""
                SELECT		/*DEFAULT INICIO*/
                            d.Codigo AS 'Codigo do Documento',
                            ISNULL(ISNULL(CONVERT(VARCHAR, cx1.Codigo), CONVERT(VARCHAR, cx3.Codigo)), '') AS 'Caixa',
                            ISNULL(CONVERT(VARCHAR, cx2.Codigo), '') AS 'Subcaixa',
                            ISNULL(ISNULL(ISNULL(ISNULL(edu1.Label, edu2.Label), edc1.Label), edc2.Label), '') AS 'Endereço',
                            ao.LabelArvoreCompleta AS 'Árvore Documental',
                            CONVERT(DATE, d.DataCadastro, 105) AS 'Data de Cadastro',
                            u.Nome AS 'Usuário de Cadastro',
                            {self.__imagens['select_imagens']}
                            /*DEFAULT FIM*/
                            /* CAMPOS CUSTOMIZADOS */
                            {self.__select_campo_customizado}
                            /* CAMPOS DE LISTA */
                            {self.__select_campo_de_lista}
                            {self.__imagens['select_concat']}
                /*DEFAULT INICIO*/   
                FROM		GedDocumento.Documento d
                {self.__imagens['left_imagens']}
                INNER JOIN	GedConfCliente.ArvoreOrganizacional ao ON ao.Id = d.IdArvoreOrganizacional
                            AND ao._del IS NULL
                            AND d.Id IN {__lista}
                INNER JOIN  GedSeguranca.Usuario u ON u.Id = d.IdUsuario
                LEFT JOIN	GedCaixa.Caixa cx1 ON cx1.id  = d.IdCaixa AND
                            cx1.IdCaixaTipo = 75 AND
                            cx1.IdCaixaPai IS NULL
                LEFT JOIN	GedCaixa.Caixa cx2 ON cx2.Id = d.IdCaixa AND
                            cx2.IdCaixaTipo != 75 AND
                            cx2.IdCaixaPai IS NOT NULL
                LEFT JOIN	GedCaixa.Caixa cx3 ON cx3.Id = cx2.IdCaixaPai
                LEFT JOIN	GedDocumento.DocumentoLinhaLista dll ON d.id  = dll.IdDocumento
                LEFT JOIN	GedEndereco.Endereco edu1 ON	(
                                                            edu1.Id = cx1.IdEndereco OR
                                                            edu1.Id = cx3.IdEndereco
                                                            )
                LEFT JOIN	GedEndereco.Endereco edu2 ON edu2.Id = cx2.IdEndereco
                LEFT JOIN	GedEndereco.EnderecoCliente edc1 ON	(
                                                                edc1.Id = cx1.IdEnderecoCliente OR
                                                                edc1.Id = cx3.IdEnderecoCliente
                                                                )
                LEFT JOIN	GedEndereco.EnderecoCliente edc2 ON edc2.Id = cx2.IdEnderecoCliente
                /*DEFAULT FIM*/
                /*CAMPOS CUSTOMIZADOS*/
                {self.__left_campo_customizado}
                /*CAMPOS DE LISTA*/
                {self.__left_campo_de_lista}
                /* DEFAULT INICIO */  
                WHERE		d.IdCliente = '{id_cliente}'
                            {where_personalizado}
                {self.__group_by_personalizado}
                ORDER BY	[Árvore Documental], [Caixa], [Codigo do Documento];
                /* DEFAULT FIM */
            """
            # print(self.__consulta)
            # os.system('pause')
            super().__init__()
            self.__cursor = self._Conexao__conn.cursor()
            self.__cursor.execute(self.__consulta)

            if index == 0:
                __colunas = [coluna[0] for coluna in self.__cursor.description]

            for linha in self.__cursor.fetchall():
                __dados.append(list(linha))

            self.__cursor.close()
            self._Conexao__conn.close()
        
        self.__dados_resultado = pd.DataFrame(__dados, columns=__colunas)
    
    @property
    def get_dados_anexos(self) -> list:

        __lista_de_arquivos: list = []
        for index, linha in self.__dados_resultado.iterrows():
            if linha["CONCAT_APP"] is not None and linha["CONCAT_APP"] != "":
                __lista_de_arquivos.append(linha["CONCAT_APP"])

        return __lista_de_arquivos
    
    def salvar_planilha(self, caminho) -> None:

        if "CONCAT_APP" in self.__dados_resultado.columns:
            self.__dados_resultado = self.__dados_resultado.drop("CONCAT_APP", axis=1)

        tamanho_da_parte =  500000
        partes = []
        
        for inicio in range(0, len(self.__dados_resultado), tamanho_da_parte):
            fim = inicio + tamanho_da_parte
            parte = self.__dados_resultado.iloc[inicio:fim]
            partes.append(parte)

        for index, parte in enumerate(partes):
            caminho = os.path.join(caminho, f"METADADOS_P{index}.xlsx")
            with pd.ExcelWriter(caminho, engine="openpyxl") as escritor:
                parte.to_excel(escritor, sheet_name=f"METADADOS",index=False)
        
class UnidadeCliente(Conexao):

    def __init__(self, id_unidade_cliente: str) -> None:
    
        super().__init__()
        self.__cursor = self._Conexao__conn.cursor()
        self.__cursor.execute(
            """
            SELECT      u.Id AS 'IdUnidade',
                        c.Id AS 'IdCliente',
                        u.Azure_NomeConta AS 'ContaAzure',
                        u.Azure_ChaveAcessoPrimario AS 'ChaveAzure'
            FROM        GedHierarquia.UnidadeCliente uc
            INNER JOIN  GedHierarquia.Unidade u ON u.Id = uc.IdUnidade AND uc.Id = ?
            INNER JOIN  GedHierarquia.Cliente c ON c.Id = uc.IdCliente
            """, id_unidade_cliente
        )

        self.__resultado = self.__cursor.fetchone()
        self.__cursor.close()
        self._Conexao__conn.close()

    @property
    def get_retorno(self) -> dict:

        __dados = {
            "id_unidade": self.__resultado[0],
            "id_cliente": self.__resultado[1],
            "azure_conta": self.__resultado[2],
            "azure_chave": self.__resultado[3]
        }
        
        return __dados
    
DECLARE @IdCliente UNIQUEIDENTIFIER = ?;

SELECT		*
FROM		(
            SELECT	DISTINCT 1 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.Documento WHERE Id = ''',d.Id,''';') AS 'ComandoSQL'
            FROM	GedDocumento.Documento d
            WHERE	d.IdCliente = @IdCliente
            UNION ALL
			SELECT		DISTINCT 1.1 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.DocumentoCampoCustomizado WHERE Id = ''',dcc.Id,''';') AS 'ComandoSQL'
            FROM		GedDocumento.Documento d
			INNER JOIN	GedDocumento.DocumentoCampoCustomizado dcc ON dcc.IdDocumento = d.Id AND
						d.IdCliente = @IdCliente
            UNION ALL
			SELECT		DISTINCT 1.2 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.DocumentoLinhaLista WHERE IdDocumento = ''',dll.IdDocumento,''' AND IdLinhaLista = ''',dll.IdLinhaLista,''';') AS 'ComandoSQL'
            FROM		GedDocumento.Documento d
			INNER JOIN	GedDocumento.DocumentoLinhaLista dll ON dll.IdDocumento = d.Id AND
						d.IdCliente = @IdCliente
            UNION ALL
			SELECT		DISTINCT 1.3 AS 'Ordem', CONCAT('DELETE FROM GedDocumento.Imagem WHERE Id = ''',i.Id,''';') AS 'ComandoSQL'
            FROM		GedDocumento.Documento d
			INNER JOIN	GedDocumento.Imagem i ON i.IdDocumento = d.Id AND
						d.IdCliente = @IdCliente
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
            SELECT		DISTINCT 0.1 AS 'Ordem', CONCAT('DELETE FROM GedRequisicao.DevolucaoItem WHERE Id = ''',di.Id,''';') AS 'ComandoSQL'
            FROM		GedCaixa.Caixa cx
            INNER JOIN	GedRequisicao.DevolucaoItem di ON di.IdCaixa = cx.Id AND
                        (cx.IdCliente = @IdCliente OR cx.IdUnidadeCliente IN (SELECT Id FROM GedHierarquia.UnidadeCliente WHERE IdCliente = @IdCliente))
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
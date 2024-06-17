from azure.cosmosdb.table.tableservice import TableService
import csv

# Configurações do Azure Cosmos DB
account_name = '***'
account_key = '**'
table_name = '****LogProducao'
table_to_search = ['Workflow']
csv_filename = r'****\OneDrive - *** Franchising Ltda\****\logs-azure.csv'

# Conexão com o Azure Cosmos DB
table_service = TableService(account_name=account_name, account_key=account_key)

# Lista para armazenar os dados
data_to_save = []

# Consulta e coleta os dados das partições especificadas
for partition_key in table_to_search:
    query = f"PartitionKey eq '{table_name}'"
    entities = table_service.query_entities(table_name, filter=query)

    for entity in entities:
        data_to_save.append({
            'PartitionKey': entity.PartitionKey,
            'RowKey': entity.RowKey,
            'TimeStamp': entity.Timestamp,
            'Data': entity.Data,
            'IdUsuario': entity.IdUsuario,
            'Operacao': entity.Operacao.encode("utf-8").decode("utf-8"),
            'Tabela': entity.Tabela,
            'NomeCampo': entity.NomeCampo,
            'ValorAntigo': entity.ValorAntigo,
            'ValorNovo': entity.ValorNovo
            # Adicione mais campos conforme necessário
        })

# Salva os dados no arquivo CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['PartitionKey', 'RowKey','TimeStamp','Data','IdUsuario','Operacao','Tabela','NomeCampo','ValorAntigo','ValorNovo']  # Adicione mais campos conforme necessário
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for data in data_to_save:
        writer.writerow(data)

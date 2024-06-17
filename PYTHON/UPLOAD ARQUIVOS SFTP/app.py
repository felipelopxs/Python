import paramiko

# Conectar ao servidor SFTP
hostname = r'sftp://sftp.la.***********'
port = 22
username = 'Archive'
password = '***********'

transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)

# Iniciar uma sessão SFTP
sftp = transport.open_sftp()

# Enviar um arquivo
arquivo_local = r'CAMINHO'
arquivo_remoto = 'My Files\******'

sftp.put(arquivo_local, arquivo_remoto)

# Fechar a conexão SFTP e o transporte
sftp.close()
transport.close()

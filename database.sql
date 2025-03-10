-- Criação das tabelas seguindo relações 1->N
-- Modelo genérico compatível com a maioria dos bancos de dados

-- Tabela Setores (1 para N com Usuários)
CREATE TABLE Setores (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL
);

-- Tabela Usuários (1 para N com Agendamentos)
CREATE TABLE Usuarios (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    idSetor INT NOT NULL,
    Tipo ENUM('Condutor', 'Comum') NOT NULL, -- Tipos de usuário
    FOREIGN KEY (idSetor) REFERENCES Setores(Id)
);

-- Tabela Veículos (1 para N com Agendamentos)
CREATE TABLE Veiculos (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Placa VARCHAR(15) NOT NULL UNIQUE,
    Marca VARCHAR(50) NOT NULL,
    Status ENUM('Disponível', 'Em uso', 'Manutenção') NOT NULL
);

-- Tabela Agendamentos (N para 1 com Usuários e Veículos)
CREATE TABLE Agendamentos (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Horario_Retirada DATETIME NOT NULL,
    Horario_Saida DATETIME NOT NULL,
    Destino VARCHAR(200) NOT NULL,
    Motivo TEXT NOT NULL,
    idCondutor INT NOT NULL,
    idUsuario INT NOT NULL,
    idVeiculo INT NOT NULL,
    FOREIGN KEY (idCondutor) REFERENCES Usuarios(Id),
    FOREIGN KEY (idUsuario) REFERENCES Usuarios(Id),
    FOREIGN KEY (idVeiculo) REFERENCES Veiculos(Id)
);

-- Índices para melhorar performance em buscas
CREATE INDEX idx_veiculo_status ON Veiculos(Status);
CREATE INDEX idx_agendamento_data ON Agendamentos(Horario_Retirada);
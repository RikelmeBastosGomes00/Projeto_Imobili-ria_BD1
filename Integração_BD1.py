import mysql.connector

# Configurações da conexão
conexao = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="TrabalhoFinal",
    password="senhaSegura123",
    database="TrabalhoFinal"
)

cursor = conexao.cursor()

# Lista de consultas SQL
consultas = [
"""-- 1) O terreno com o valor mais caro 
SELECT 
T.idTerreno,
T.descricao,
T.areaTerreno,
TP.descricao AS tipoContrato,
THT.valorSugerido
FROM Terreno T
INNER JOIN Tipo_has_Terreno THT
ON T.idTerreno = THT.Terreno_idTerreno
INNER JOIN Tipo TP
ON TP.idTipo = THT.Tipo_idTipo
WHERE THT.valorSugerido = (
SELECT MAX(valorSugerido)
FROM Tipo_has_Terreno
)
ORDER BY THT.valorSugerido DESC;""",

"""-- 2) A casa com o valor mais barato 
SELECT 
C.idCasa,
C.descricao,
C.areaCasa,
TP.descricao AS tipoContrato,
THC.valorSugerido
FROM Casa AS C
INNER JOIN Tipo_has_Casa AS THC
ON C.idCasa = THC.Casa_idCasa
INNER JOIN Tipo AS TP
ON TP.idTipo = THC.Tipo_idTipo
WHERE THC.valorSugerido = (
SELECT MIN(valorSugerido)
FROM Tipo_has_Casa
)
ORDER BY THC.valorSugerido DESC;""",

"""
-- 3) Ver os imóveis disponíveis

SELECT 
"Apartamento" AS Tipo_Imovel,
A.idApartamento AS id_imovel,
D.descricaoDispo,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Apartamento AS A
INNER JOIN Disponibilidade AS D 
ON A.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON A.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'Disponível'

UNION

SELECT 
"Casa",
C.idCasa,
D.descricaoDispo,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Casa AS C
INNER JOIN Disponibilidade AS D 
ON C.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON C.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'Disponível'


UNION

SELECT 
"SalaComercial",
S.idSalaComercial,
D.descricaoDispo,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM SalaComercial AS S
INNER JOIN Disponibilidade AS D 
ON S.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON S.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'Disponível'

UNION

SELECT 
"Terreno",
T.idTerreno,
D.descricaoDispo,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Terreno AS T
INNER JOIN Disponibilidade AS D 
ON T.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON T.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'Disponível';""",

"""-- 4) Ver as casas que foram retiradas 

SELECT 
'Casa' AS tipo_imovel,
C.idCasa,
D.descricaoDispo,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Casa C
INNER JOIN Disponibilidade D 
ON C.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco E 
ON C.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio MUN 
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado EST ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'Retirado' ;""",

"""-- 5) Imóveis indisponíveis no bairro Consolação
SELECT 
'Apartamento' AS tipo_imovel,
A.idApartamento AS id_imovel,
D.descricaoDispo AS status,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Apartamento AS A
INNER JOIN Disponibilidade AS D 
ON A.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON A.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN 
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'indisponivel'  
AND E.bairro = 'Consolação'             

UNION

SELECT
'Casa',
C.idCasa AS id_imovel,
D.descricaoDispo AS status,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Casa AS C
INNER JOIN Disponibilidade AS D 
ON C.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON C.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN 
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'indisponivel'  
AND E.bairro = 'Consolação'              

UNION

SELECT 
'Sala Comercial', 
S.idSalaComercial AS id_imovel,
D.descricaoDispo AS status,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM SalaComercial AS S
INNER JOIN Disponibilidade AS D 
ON S.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON S.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN 
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'indisponivel'  
AND E.bairro = 'Consolação'             

UNION

SELECT 
'Terreno',
T.idTerreno AS id_imovel,
D.descricaoDispo AS status,
E.logradouro,
E.numero,
E.bairro,
MUN.nomeMunicipio,
EST.nomeEstado
FROM Terreno AS T
INNER JOIN Disponibilidade AS D
ON T.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco AS E 
ON T.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio AS MUN 
ON E.Municipio_idMunicipio = MUN.idMunicipio
INNER JOIN Estado AS EST 
ON MUN.Estado_idEstado = EST.idEstado
WHERE D.descricaoDispo = 'indisponivel'  
AND E.bairro = 'Consolação';       """,

"""-- 6) Ver os imóveis que possuem administração por imóveis e qual seu tipo

SELECT 
'Casa' AS tipo_imovel,
C.idCasa AS id_imovel,
TA.descricao AS tipo_administracao,
AI.situacao,
AI.dataInicio,
AI.dataFim,
TA.PercentualTaxaImobiliaria AS porcentagem_Taxa
FROM Casa C
INNER JOIN AdministracaoImovel AI 
ON C.AdministracaoImovel_idAdministracaoImovel = AI.idAdministracaoImovel
INNER JOIN TipoAdm TA 
ON AI.TipoAdm_idTipoAdm = TA.idTipoAdm

UNION

SELECT 
'Apartamento',
A.idApartamento AS id_imovel,
TA.descricao AS tipo_administracao,
AI.situacao,
AI.dataInicio,
AI.dataFim,
TA.PercentualTaxaImobiliaria AS porcentagem_Taxa
FROM Apartamento A
INNER JOIN AdministracaoImovel AI 
ON A.AdministracaoImovel_idAdministracaoImovel = AI.idAdministracaoImovel
INNER JOIN TipoAdm TA 
ON AI.TipoAdm_idTipoAdm = TA.idTipoAdm

UNION

SELECT 
'Sala Comercial',
SC.idSalaComercial AS id_imovel,
TA.descricao AS tipo_administracao,
AI.situacao,
AI.dataInicio,
AI.dataFim,
TA.PercentualTaxaImobiliaria AS porcentagem_Taxa
FROM SalaComercial SC
INNER JOIN AdministracaoImovel AI 
ON SC.AdministracaoImovel_idAdministracaoImovel = AI.idAdministracaoImovel
INNER JOIN TipoAdm TA 
ON AI.TipoAdm_idTipoAdm = TA.idTipoAdm

UNION

SELECT 
'Terreno' ,
T.idTerreno AS id_imovel,
TA.descricao AS tipo_administracao,
AI.situacao,
AI.dataInicio,
AI.dataFim,
TA.PercentualTaxaImobiliaria AS porcentagem_Taxa
FROM Terreno T
INNER JOIN AdministracaoImovel AI 
ON T.AdministracaoImovel_idAdministracaoImovel = AI.idAdministracaoImovel
INNER JOIN TipoAdm TA 
ON AI.TipoAdm_idTipoAdm = TA.idTipoAdm;""",

"""-- 7) Ver a quantidade visitas feitas nas casas disponíveis 

SELECT 
C.idCasa AS id_imovel,
E.logradouro,
E.numero,
E.bairro,
COUNT(CV.Visita_idVisita) AS total_visitas,
D.descricaoDispo 
FROM Casa C
INNER JOIN CasaVisitada CV 
ON C.idCasa = CV.Casa_idCasa
INNER JOIN Disponibilidade D 
ON C.Disponibilidade_idDisponibilidade = D.idDisponibilidade
INNER JOIN Endereco E 
ON C.Endereco_idEndereco = E.idEndereco
WHERE D.descricaoDispo = 'Disponível'
GROUP BY C.idCasa
ORDER BY total_visitas DESC;""",

"""-- 8) Consultar quais foram as transações mais caras por imóvel 

-- Casas

SELECT 
'Casa' AS tipo_imovel,
C.idCasa AS id_imovel,
C.descricao AS descricao_imovel,
T.ValorFinal AS valor_transacao,
T.formaPagamento,
E.logradouro,
E.numero,
E.bairro,
M.nomeMunicipio AS municipio,
ES.nomeEstado AS estado,
D.descricaoDispo AS disponibilidade
FROM Casa C
INNER JOIN Contrato_has_Casa CHC
ON C.idCasa = CHC.Casa_idCasa
INNER JOIN Transacao T ON 
CHC.Contrato_idContrato = T.Contrato_idContrato
INNER JOIN Endereco E 
ON C.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio M 
ON E.Municipio_idMunicipio = M.idMunicipio
INNER JOIN Estado ES 
ON M.Estado_idEstado = ES.idEstado
INNER JOIN Disponibilidade D 
ON C.Disponibilidade_idDisponibilidade = D.idDisponibilidade
WHERE T.ValorFinal = (
SELECT MAX(T2.ValorFinal)
FROM Transacao T2
INNER JOIN Contrato_has_Casa CHC2 
ON T2.Contrato_idContrato = CHC2.Contrato_idContrato
WHERE CHC2.Casa_idCasa = C.idCasa
)

UNION 

-- Apartamentos
SELECT 
'Apartamento',
A.idApartamento AS id_imovel,
A.descricao AS descricao_imovel,
T.ValorFinal AS valor_transacao,
T.formaPagamento,
E.logradouro,
E.numero,
E.bairro,
M.nomeMunicipio AS municipio,
ES.nomeEstado AS estado,
D.descricaoDispo AS disponibilidade
FROM Apartamento A
INNER JOIN Contrato_has_Apartamento CHA 
ON A.idApartamento = CHA.Apartamento_idApartamento
INNER JOIN Transacao T 
ON CHA.Contrato_idContrato = T.Contrato_idContrato
INNER JOIN Endereco E 
ON A.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio M 
ON E.Municipio_idMunicipio = M.idMunicipio
INNER JOIN Estado ES 
ON M.Estado_idEstado = ES.idEstado
INNER JOIN Disponibilidade D 
ON A.Disponibilidade_idDisponibilidade = D.idDisponibilidade
WHERE T.ValorFinal = (
SELECT MAX(T2.ValorFinal)
FROM Transacao T2
INNER JOIN Contrato_has_Apartamento CHA2 
ON T2.Contrato_idContrato = CHA2.Contrato_idContrato
WHERE CHA2.Apartamento_idApartamento = A.idApartamento
)

UNION 

-- Salas Comerciais
SELECT 
'Sala Comercial',
S.idSalaComercial AS id_imovel,
S.descricao AS descricao_imovel,
T.ValorFinal AS valor_transacao,
T.formaPagamento,
E.logradouro,
E.numero,
E.bairro,
M.nomeMunicipio AS municipio,
ES.nomeEstado AS estado,
D.descricaoDispo AS disponibilidade
FROM SalaComercial S
INNER JOIN Contrato_has_SalaComercial CHS 
ON S.idSalaComercial = CHS.SalaComercial_idSalaComercial
INNER JOIN Transacao T 
ON CHS.Contrato_idContrato = T.Contrato_idContrato
INNER JOIN Endereco E 
ON S.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio M 
ON E.Municipio_idMunicipio = M.idMunicipio
INNER JOIN Estado ES 
ON M.Estado_idEstado = ES.idEstado
INNER JOIN Disponibilidade D 
ON S.Disponibilidade_idDisponibilidade = D.idDisponibilidade
WHERE T.ValorFinal = (
SELECT MAX(T2.ValorFinal)
FROM Transacao T2
INNER JOIN Contrato_has_SalaComercial CHS2 
ON T2.Contrato_idContrato = CHS2.Contrato_idContrato
WHERE CHS2.SalaComercial_idSalaComercial = S.idSalaComercial
)

UNION 

-- Terrenos
SELECT 
'Terreno',
TR.idTerreno AS id_imovel,
TR.descricao AS descricao_imovel,
T.ValorFinal AS valor_transacao,
T.formaPagamento,
E.logradouro,
E.numero,
E.bairro,
M.nomeMunicipio AS municipio,
ES.nomeEstado AS estado,
D.descricaoDispo AS disponibilidade
FROM Terreno TR
JOIN Contrato_has_Terreno CHT 
ON TR.idTerreno = CHT.Terreno_idTerreno
JOIN Transacao T 
ON CHT.Contrato_idContrato = T.Contrato_idContrato
INNER JOIN Endereco E 
ON TR.Endereco_idEndereco = E.idEndereco
INNER JOIN Municipio M 
ON E.Municipio_idMunicipio = M.idMunicipio
INNER JOIN Estado ES 
ON M.Estado_idEstado = ES.idEstado
INNER JOIN Disponibilidade D 
ON TR.Disponibilidade_idDisponibilidade = D.idDisponibilidade
WHERE T.ValorFinal = (
SELECT MAX(T2.ValorFinal)
FROM Transacao T2
JOIN Contrato_has_Terreno CHT2 
ON T2.Contrato_idContrato = CHT2.Contrato_idContrato
WHERE CHT2.Terreno_idTerreno = TR.idTerreno
)
ORDER BY valor_transacao DESC;

""",

"""-- 9) Analise de salários com base nos cargos 

SELECT 
    
C.nomeCargo AS cargo,
COUNT(F.idFuncionario) AS quantidade_funcionarios,
MIN(F.salario) AS menor_salario,
MAX(F.salario) AS maior_salario,
AVG(F.salario) AS media_salarial,
SUM(F.salario) AS total_folha
FROM Cargo C
INNER JOIN CargoOcupado CO
 ON C.idCargo = CO.Cargo_idCargo
INNER JOIN Funcionario F 
ON CO.Funcionario_idFuncionario = F.idFuncionario
GROUP BY C.nomeCargo
ORDER BY media_salarial DESC;""",

"""-- 10) Análise e detalhamento da clase transação com as comissoões ( Funcionário e imobiliaria) 

SELECT 
T.idTransacao,
T.DataEHoraTransacao,
T.formaPagamento,
T.ValorFinal,    
T.PercentualComissaoFuncionario AS percentual_comissao_func,
T.ValorFinal * (T.PercentualComissaoFuncionario / 100) AS comissao_func_calculada,
T.ComissaoFuncionario AS comissao_func_armazenada,
(T.ValorFinal * (T.PercentualComissaoFuncionario / 100)) - T.ComissaoFuncionario AS diferenca_comissao_func,
TA.PercentualTaxaImobiliaria AS percentual_taxa_imob,
T.ValorFinal * (TA.PercentualTaxaImobiliaria / 100) AS comissao_imob_calculada,
T.ComissaoImobiliaria AS comissao_imob_armazenada,
(T.ValorFinal * (TA.PercentualTaxaImobiliaria / 100)) - T.ComissaoImobiliaria AS diferenca_comissao_imob,
T.ValorFinal AS valor_bruto,
T.ComissaoFuncionario + T.ComissaoImobiliaria AS total_comissoes,
T.ValorFinal - (T.ComissaoFuncionario + T.ComissaoImobiliaria) AS valor_proprietario,    
TA.descricao AS tipo_administracao,
P.nomeCompleto AS nome_funcionario,
TP.descricao AS tipo_operacao
FROM Transacao T
INNER JOIN TipoAdm TA 
ON T.TipoAdm_idTipoAdm = TA.idTipoAdm
INNER JOIN Funcionario F 
ON T.Funcionario_idFuncionario = F.idFuncionario
INNER JOIN Pessoa P 
ON F.Pessoa_idPessoa = P.idPessoa
INNER JOIN Contrato CT ON T.Contrato_idContrato = CT.idContrato
INNER JOIN Tipo TP ON CT.Tipo_idTipo = TP.idTipo
ORDER BY T.ValorFinal DESC;""",
]


for i, consulta in enumerate(consultas, start=1):
    print(f"\n--- Resultado da Consulta {i} ---")
    cursor.execute(consulta)
    resultados = cursor.fetchall()


    colunas = [desc[0] for desc in cursor.description]
    print("Colunas:", ", ".join(colunas))

    for linha in resultados:
        print(linha)


cursor.close()
conexao.close()
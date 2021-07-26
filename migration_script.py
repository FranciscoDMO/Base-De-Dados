import sys
import mysql.connector
import json
import io 
from datetime import datetime

cnx = mysql.connector.connect(user='root', password='dev',
                              host='127.0.0.1',
                              database='trabalhonovo')

cursor = cnx.cursor()
cursor.execute("SET NAMES 'utf8';")

cursor.execute("SELECT id FROM Testes;")

testes = []
for (idTeste,) in cursor:
    testes.append(int(idTeste))

cursor.execute("SELECT id FROM PfS;")
pfs = []
for (idPFS,) in cursor:
    pfs.append(int(idPFS))

cursor.execute("SELECT idCivil FROM Atletas;")
atletas = []
for (idAtleta,) in cursor:
    atletas.append(int(idAtleta))

cursor.close()
cursor = cnx.cursor()

def data_to_string(data):
    return data.strftime("%Y-%m-%d %H:%M:%S")

def obter_modalidade(idModalidade):
    modalidade = {}
    cursor.execute("SELECT id, nome FROM Modalidade WHERE id = %u" % idModalidade)
    for (idMod, nome) in cursor:
        modalidade['id'] = idMod
        modalidade['nome'] = nome
    
    return modalidade

def obter_categorias(idAtleta):
    categorias = []
    cursor.execute("SELECT id, nome, descricao, FKModalidade FROM Categoria WHERE FKatleta = %u" % idAtleta)
    for (idCat, nome, descricao, fkModalidade) in cursor:
        categoria = {}
        categoria['idCat'] = idCat
        categoria['nome'] = nome
        categoria['descricao'] = descricao
        categoria['modalidade'] = fkModalidade
        categorias.append(categoria)

    for categoria in categorias:
        categoria['modalidade'] = obter_modalidade(categoria['modalidade'])
    
    return categorias
 

def obter_atleta(id_):
    atleta = {}
    cursor.execute("SELECT idCivil, nome, DoB, contacto, email, CondicaoMedica FROM Atletas WHERE idCivil = %u" % id_)
    for (idAtleta, nome, data, contacto, email, CondicaoMedica) in cursor:
        atleta['idCivil'] = idAtleta
        atleta['nome'] = nome.encode("utf8")
        atleta['DoB'] = data_to_string(data)
        atleta['contacto'] = contacto
        atleta['email'] = email
        atleta['CondicaoMedica'] = CondicaoMedica
        atleta['categorias'] = obter_categorias(id_)
 
    return atleta

def obter_pfs(idPfs):
    pfs = {}
    cursor.execute("SELECT id, nome, contacto, email, Especialidade FROM PfS WHERE id = %u" % idPFS)
    for (idPfs, nome, contacto, email, especialidade) in cursor:
        pfs['idPfs'] = idPfs
        pfs['nome'] = nome
        pfs['contacto'] = contacto
        pfs['email'] = email
        pfs['especialidade'] = especialidade

    return pfs


testesJson = []
for idTeste in testes:
    testeJson = json.loads('{}')
    cursor.execute("SELECT * FROM Testes WHERE id = %u" % idTeste)
    for (idTeste, DataTeste, Local, tipoTestes, Resultado, atleta, pfs) in cursor:
        testeJson['id'] = idTeste
        testeJson['data'] = data_to_string(DataTeste)
        testeJson['local'] = Local
        testeJson['tipo'] = tipoTestes
        testeJson['resultado'] = Resultado
        testeJson['atleta'] = obter_atleta(atleta)
        testeJson['pfs'] = obter_pfs(pfs)

        testesJson.append(testeJson)

with io.open('out.json', 'w', encoding='utf8') as json_file:
    data = json.dumps(testesJson, ensure_ascii=False, indent=4 , encoding='utf8')
    json_file.write(unicode(data) + u"\n")


cursor.close()
    

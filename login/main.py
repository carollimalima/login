from flask import Flask,render_template, request
from funcionario import *
from departamento import *
from datetime import datetime
import psycopg2
from flask import session


app = Flask(__name__) 

@app.route('/trataform',methods=["POST","GET"])
def trataform():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        login = request.form["login"]
        senha = request.form["senha"]
        depto = int(request.form["departamento"])
        cod=request.form["id"]

        f = Funcionario(nome,email,senha,login)
        fdao = funcionarioDao()
        
        if (cod):
            f.id=cod
            
        if (depto):
            f.departamento=depto
            
        fdao.salvar(f)

        return render_template('tela.html')

    return render_template('form.html')



@app.route('/lista')
def lista():
    fdao = funcionarioDao().listar()

    return render_template('tela.html',flistar=fdao)


@app.route('/excluir/<id>')
def excluir(id):
    id=int(id)
    fdao = funcionarioDao()
    fdao.excluir(id)
    flistar = fdao.listar()
    return render_template('tela.html',flistar=flistar)



@app.route('/editar/<id>')

def editar(id):
    fdao = funcionarioDao()
    f = fdao.buscar(id)
    nome = f.nome
    email = f.email
    login=f.login
    senha=f.senha
    idDepartamento = f.departamento
    return render_template('editar.html',nome=nome,email=email,idDepartamento=idDepartamento,login=login,senha=senha,id=id)




@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]
        fdao = funcionarioDao()
        f = fdao.login(login,senha)
        try:
            return render_template('home.html',aviso=f.nome)
        except BaseException:
            return render_template('login.html',aviso=f)

    return render_template('login.html')



@app.route('/d/listar')
def depto_listar():
    d = departamentoDao().listar()
    return render_template('depto_listar.html',dlistar=d)


@app.route('/d/inserir',methods=["POST","GET"])
def depto_inserir():
    if request.method == "POST":
        nome = request.form["nome"]
        cod=request.form["id"]
        idGerente = request.form["idGerente"]
        
        d = Departamento(nome)
        ddao = departamentoDao()
        
        if (cod):
            d.id=int(cod)
        
        if(idGerente):
            d.funcionario=idGerente
            
        ddao.salvar(d)

        return render_template('depto_listar.html')

    return render_template('depto_form.html')

    

@app.route('/d/editar/<id>')
def depto_editar(id):
    ddao = departamentoDao()
    d = ddao.buscar(id)
    nome = d.nome
    idGerente = d.funcionario
    return render_template('depto_editar.html',nome=nome,idGerente=idGerente,id=id)


@app.route('/d/excluir/<id>')
def depto_excluir(id):
    id=int(id)
    ddao = departamentoDao()
    ddao.excluir(id)
    dlistar = ddao.listar()
    return render_template('depto_listar.html',dlistar=dlistar)




if __name__ == '__main__':
    app.run(debug = True)


"""
@app.before_first
def before_first_request(): 
    print('before_first_request')

@app.before_request
def before_request():
    print(request.path)
    print('before_request')

@app.after_request
def after_request(response):
    print('after_request')
    return response
"""

    

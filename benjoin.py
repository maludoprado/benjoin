
#from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testeuser:benjoin23@localhost:3306/mybenjo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(45))
    end = db.Column('usu_end', db.String(256))


    def __init__(self, nome, email, senha, end):
        self.nome = nome
        self.email= email
        self.senha = senha
        self.end = end
      
class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def index():
    return render_template('index.html')
   
@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/novo", methods=['POST'])
def novousuario():
    usuario = Usuario(request.form.get('nome'), request.form.get('email'),request.form.get('senha'), request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhes/<int:id>")
def buscausuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome 

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        usuario.end = request.form.get('end')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('euusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))  

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', categorias = Categoria.query.all(), anuncios = Anuncio.query.all(), titulo = "Anuncios")

@app.route("/anuncio/novo", methods=['POST'])
def novoanuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),
    request.form.get('preco'),request.form.get('cat'),request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))
 

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template('pergunta.html')

@app.route("/anuncios/compra")
def compra():
    print("anuncio comprado")
    return ""

@app.route("/anuncio/favoritos")
def favoritos():
    print("favorito inserido")
    return f"<h4>Comprado</h4>"

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo = "Categoria")

@app.route("/categoria/novo", methods=['POST'])
def novacategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html', titulo="Relatorio de Vendas")

@app.route("/relatorios/compras")
def relCompras():
    return render_template ('relCompras.html', titulo="Ultimas compras")


if __name__ == 'benjoin':
#o comando if __name__ == '__main__': é utilizado para que um código ao ser importado não 'rode', servindo apenas como biblioteca importada.
# Obs: No caso de rodar diretamente com o interpretador do VSCode ou de outra IDE, o interpretador ira reconhecer o arquivo como MAIN, independente de seu nome. 
# Mas no caso de executar o script via cmd, bash ou powershell, ele irá reconhecer o arquivo pelo seu nome, nesse caso, benjoin. Por isso, se estiver rodando direto na IDE,
# deixe if __name__ == '__main__':, mas se estiver rodando no cmd, bash ou powershell, utilize if __name__== 'nome_do_arquivo':       
    print('testesom')
    with app.app_context():  
        db.create_all()
    
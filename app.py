
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://udinhxlznhmruf:ec5464e0704dd35ea015c44cfa850ea39928f3662d93e7ad76b3df1ab0d50ad8@ec2-52-86-177-34.compute-1.amazonaws.com:5432/dcpsptc6rsus41'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Notas(db.Model):
    '''Clase Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key=True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(200))

    def __init__(self, tituloNota, cuerpoNota):

        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota


@app.route('/')
def index():
    consultar = Notas.query.all()
    for nota in consultar:
        print(nota.tituloNota)
        print(nota.cuerpoNota)
    return render_template('index.html', consulta=consultar)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/createnote', methods=['POST'])
def createnote():
    ctitulo = request.form['titulo']
    ccontenido = request.form['contenido']
    notaNueva = Notas(tituloNota=ctitulo, cuerpoNota=ccontenido)
    db.session.add(notaNueva)
    db.session.commit()
    return redirect('/')
    # return 'nota creada ' + titulo +' ' + contenido


@app.route('/leernotas')
def leernotas():
    consultar = Notas.query.all()
    print(consultar)
    for nota in consultar:
        print(nota.tituloNota)
        print(nota.cuerpoNota)
    # return "Notas consultadas"
    return render_template("index.html", consulta=consultar)


@app.route('/eliminarN/<id>')
def eliminar(id):
    nota = Notas.query.filter_by(idNota=int(id)).delete()
    print(nota)
    db.session.commit()
    return redirect('/')


@app.route('/editarN/<id>')
def editar(id):
    nota = Notas.query.filter_by(idNota=int(id)).first()
    print(nota)
    return render_template("edittemplate.html", nota=nota)


@app.route('/editnote', methods=['POST'])
def editnore():
    ctitulo = request.form['titulo']
    ccontenido = request.form['contenido']
    cid = request.form['id']
    notaM = Notas.query.filter_by(idNota=int(cid)).first()
    notaM.tituloNota = ctitulo
    notaM.cuerpoNota = ccontenido
    db.session.commit()
    return redirect('/')
    # return 'nota creada ' + titulo +' ' + contenido


if __name__ == "__main__":
    db.create_all()
    app.run()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import socket


#Initialize flask app and config db
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_app.db'
db.init_app(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()


def fetchDetails(): 
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)

@app.route('/')
def index():
    items = Item.query.all()
    hostname,ip = fetchDetails()
    return render_template('index.html', items=items, HOSTNAME=hostname, IP=ip)

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    description = request.form['description']
    item = Item(name=name, description=description)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        try:
            item.name = request.form['name']
            item.description = request.form['description']
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            pass
    return render_template('edit.html', item=item)
    # return redirect(url_for('update',id=id))

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


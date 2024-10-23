from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'  # Cambia esto por una clave secreta segura


@app.before_request
def initialize_session():
    if 'products' not in session:
        session['products'] = []

@app.route('/')
def index():
    return render_template('index.html', products=session['products'])

@app.route('/add', methods=['POST'])
def add_product():
    new_id = request.form['id']
    
    if any(p['id'] == new_id for p in session['products']):
        return "Error: El ID ya existe, intenta con otro ID."

   
    new_product = {
        'id': new_id,
        'nombre': request.form['nombre'],
        'cantidad': request.form['cantidad'],
        'precio': request.form['precio'],
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }


    session['products'].append(new_product)
    session.modified = True
    return redirect('/')

@app.route('/delete/<product_id>')
def delete_product(product_id):
    
    session['products'] = [p for p in session['products'] if p['id'] != product_id]
    session.modified = True
    return redirect('/')

@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        for product in session['products']:
            if product['id'] == product_id:
                product['nombre'] = request.form['nombre']
                product['cantidad'] = request.form['cantidad']
                product['precio'] = request.form['precio']
                product['fecha_vencimiento'] = request.form['fecha_vencimiento']
                product['categoria'] = request.form['categoria']
                session.modified = True
                break
        return redirect('/')
    else:
        product_to_edit = next((p for p in session['products'] if p['id'] == product_id), None)
        if not product_to_edit:
            return "Producto no encontrado."
        return render_template('edit.html', product=product_to_edit)

if __name__ == '__main__':
    app.run(debug=True)

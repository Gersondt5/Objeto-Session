from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta más segura

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminario = request.form['seminario']
        
        # Guardar en la sesión
        if 'inscritos' not in session:
            session['inscritos'] = []
        session['inscritos'].append({
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminario': seminario
        })
        session.modified = True  # Indicar que la sesión ha cambiado
        return redirect(url_for('index'))  # Redirigir al índice

    return render_template('registro.html')

@app.route('/editar/<int:inscrito_id>', methods=['GET', 'POST'])
def editar(inscrito_id):
    if 'inscritos' in session and inscrito_id < len(session['inscritos']):
        if request.method == 'POST':
            # Actualizar datos del formulario
            session['inscritos'][inscrito_id]['fecha'] = request.form['fecha']
            session['inscritos'][inscrito_id]['nombre'] = request.form['nombre']
            session['inscritos'][inscrito_id]['apellidos'] = request.form['apellidos']
            session['inscritos'][inscrito_id]['turno'] = request.form['turno']
            session['inscritos'][inscrito_id]['seminario'] = request.form['seminario']
            session.modified = True  # Indicar que la sesión ha cambiado
            return redirect(url_for('index'))  # Redirigir al índice
        
        inscrito = session['inscritos'][inscrito_id]
        return render_template('editar.html', inscrito=inscrito, inscrito_id=inscrito_id)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:inscrito_id>')
def eliminar(inscrito_id):
    if 'inscritos' in session and inscrito_id < len(session['inscritos']):
        session['inscritos'].pop(inscrito_id)
        session.modified = True  # Indicar que la sesión ha cambiado
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

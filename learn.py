# Program for learning REST with bottle and JSON
# Massoud Maher

from bottle import route, run, template, request


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


 
@route('/hi')
def hello():
  name = request.cookies.username or 'Guest'
  return template('Hello {{name}}', name=name)

run(host='localhost', port=8080, debug=True)

# Author: Massoud Maher

import json
import CellGene
from bottle import route, run, template, request

class CellGeneService:
  """Runs REST service that fetches abundance values for cell-gene pair


  """

  

  @route('/hello/<name>')
  def index(name):
      return template('<b>Hello {{name}}</b>!', name=name)


   
  @route('/hi')
  def hello():
    name = request.cookies.username or 'Guest'
    return template('Hello {{name}}', name=name)



  def main():
    run(host='localhost', port=8080, debug=True)

  if __name__ == "__main__":
    main()

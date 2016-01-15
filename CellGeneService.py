# Author: Massoud Maher

import json
from CellGene import CellGene
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

  @route('/context/expression/cell_line/<gene_set>', method='GET')
  def get_json(gene_set):
    cg = CellGene()
    output = cg.get_abundance_json(gene_set, ['X769P_KIDNEY', 'X786O_KIDNEY'])
    return output


  def main():
    run(host='localhost', port=8080, debug=True)

  if __name__ == "__main__":
    main()

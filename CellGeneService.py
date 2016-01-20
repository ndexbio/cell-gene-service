# Author: Massoud Maher

import json
import pandas as pd
import CellGene
from bottle import route, run, template, request, response

cg = CellGene.CellGene()

class CellGeneService(object):
  """Runs REST service that fetches abundance values for cell-gene pair"""

  @route('/context/expression/cell_line', method='POST')
  def test_json():
    """Returns a JSON of abundance values for the provided JSON inputs

    Returns:
      A JSON string representing the associated abundance values of cell_line and gene. See JSON format in README
      Returns Null if input is invalid (including integers) or not found in matrix
    """

    # Initialize input dict, CellGene object, output dataframe
    input_set = request.json
    output_df = pd.DataFrame()


    # For each gene
    for key in input_set.keys():
      # Get abundance for its associated cells and append onto output_df

      # Remove duplicate cell lines and get list of values
      cell_lines = set(input_set[key])
      abundance_list = cg.get_abundance(key, cell_lines)

      # If gene is already in output dataframe, skip it
      if key in output_df.index.values:
        break

      output_df = output_df.append(abundance_list)


    print "----------------- output_df -----------------"
    print output_df
    print "---------- index json -------------"
    output_json = output_df.to_json(orient="index")
    print output_json 

    response.content_type = "application/json"
    return output_json

  @route('/context/expression/cell_line/ids_available', method='GET')
  def get_ids():
    
  

  def main():
    """Runs the service on localhost:8080"""
    run(host='localhost', port=8080, debug=True)

  if __name__ == "__main__":
    main()

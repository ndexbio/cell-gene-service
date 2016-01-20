# Author: Massoud Maher

import json
import pandas as pd
import CellGene
from bottle import route, run, template, request

# TODO remove duplicates from JSON before requesting. duplicate cell-lines result in "cannot reindex from a duplicate axis"
class CellGeneService:
  """Runs REST service that fetches abundance values for cell-gene pair"""


  @route('/json_test', method='POST')
  def test_json():
    """Returns a JSON of abundance values for the provided JSON inputs

    Returns:
      A JSON string representing the associated abundance values of cell_line and gene. See JSON format in README
      Returns Null if input is invalid (including integers) or not found in matrix
    """
    print("JSON is: " + str(request.json))
    print("Type is: " + str(type(request.json)))
    print("values are: " + str( request.json.values() ))
    print("keys are: " + str( request.json.keys() ))

    # Initialize input dict, CellGene object, output dataframe
    input_set = request.json
    cg = CellGene.CellGene()
    output_df = pd.DataFrame()


    # For each gene
    for key in input_set.keys():
      # Get abundance for its associated cells and append onto output_df
      abundance_list = cg.get_abundance(key, input_set[key])

      print "--------------- abundance list --------"
      print abundance_list

      # Check for duplicates before attempting to add
      # If gene is already in output dataframe, skip it
      if key in output_df.index.values:
        break

      output_df = output_df.append(abundance_list)

      print "----------------- output_df -----------------"
      print output_df


    print "---------- index json -------------"
    print output_df.to_json(orient="index")
  

  def main():
    """Runs the service on localhost:8080"""
    run(host='localhost', port=8080, debug=True)

  if __name__ == "__main__":
    main()

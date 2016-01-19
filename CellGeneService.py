# Author: Massoud Maher

import json
import pandas as pd
from CellGene import CellGene
from bottle import route, run, template, request

# TODO put json format in README
# TODO remove duplicates from JSON before requesting. duplicate cell-lines result in "cannot reindex from a duplicate axis"
class CellGeneService:
  """Runs REST service that fetches abundance values for cell-gene pair"""


  @route('/json_test', method='POST')
  def test_json():
    """Returns a JSON of abundance values for the provided JSON inputs

    Returns:
      A JSON string representing the associated abundance values of cell_line and gene in the following format

      {
        "gene_name":
          {
            "cell_line_name":abundance_val
            ...
          },

        ...

        "gene_name":
          {
            "cell_line_name":abundance_val
            ...
          }
        }

      Returns Null if input is invalid (including integers) or not found in matrix
    """
    print("JSON is: " + str(request.json))
    print("Type is: " + str(type(request.json)))
    print("values are: " + str( request.json.values() ))
    print("keys are: " + str( request.json.keys() ))

    # Dictionary of gene:cell pairs
    input_set = request.json

    cg = CellGene()
    output_df = pd.DataFrame()


    # For each gene
    for key in input_set.keys():
      # Get abundance for its associated cells and add into output_dict
      abundance_list = cg.get_abundance(key, input_set[key])

      print "--------------- abundance list --------"
      print abundance_list

      output_df = output_df.append(abundance_list)

      print "----------------- output_df -----------------"
      print output_df


    print "---------- index json -------------"
    print output_df.to_json(orient="index")
    
    print "---------- column json -------------"
    print output_df.to_json()



  @route('/context/expression/cell_line/gene_set=<gene_set>cell_line_set=<cell_line_set>', method='GET')
  def get_json(gene_set, cell_line_set):
    """Returns a JSON of abundance values for the provided inputs

    Args:
      gene_set: Comma seperated string of gene names eg. "MED6, AKT4"

    Returns:
      A JSON string representing the associated abundance values of cell_line and gene in the following format

      {
        "gene_name":
          {
            "cell_line_name":abundance_val
            ...
          },

        ...

        "gene_name":
          {
            "cell_line_name":abundance_val
            ...
          }
        }

      Returns Null if input is invalid (including integers) or not found in matrix
    """

    # Prepare input
    gene_set.upper()
    gene_list = gene_set.split(',')

    # Get abundance values in JSON and return
    cg = CellGene()
    output = cg.get_abundance_json(gene_list, ['X769P_KIDNEY', 'X786O_KIDNEY'])
    print('output is : ' + str(output))
    return output


  def main():
    """Runs the service on localhost:8080"""
    run(host='localhost', port=8080, debug=True)

  if __name__ == "__main__":
    main()

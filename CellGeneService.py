# Author: Massoud Maher

import json
import pandas as pd
import CellGene
from bottle import route, run, template, request, response
from bottledaemon import daemon_run

cg = CellGene.CellGene('CCLE_protein')

# TODO handle invalid json synax
# TODO handle multiple cell line input where none are in data
# TODO add T/F option in URL to download .tab or not
# Note, if a gene is defined twice in input, first one is used, all others are ignored
"""Runs REST service that fetches abundance values for cell-gene pair"""

@route('/context/expression/cell_line/<dataset>', method='POST')
def test_json(dataset):
  """Returns a JSON of abundance values for the provided JSON inputs for CCLE_protein dataset

  Returns:
    A JSON string representing the associated abundance values of cell_line and gene. See JSON format in README
    Returns Null if input is invalid (including integers) or not found in matrix
  """
  print "REQUEST RECEIVED!!!!"

  # Initialize input dict, CellGene object, output dataframe
  input_set = request.json["input"]["data"]
  output_df = pd.DataFrame()

  # For all inputs
  for key, val in input_set.iteritems():

    # Make genes uppercase
    input_set[key.upper()] = input_set[key]
    del input_set[key]
    key = key.upper()
    # Make cell lines uppercase
    input_set[key] = [cell.upper() for cell in val] 

    # Remove duplicate cell lines 
    cell_lines = set(input_set[key])

    # Get abundance for its associated cells and append onto output_df
    abundance_list = cg.get_abundance(key, cell_lines)
    # Skip duplicate genes
    if key in output_df.index.values:
      break

    output_df = output_df.append(abundance_list)


  output_json = output_df.to_json(orient="index")
  response.content_type = "application/json"
  return output_json

@route('/context/expression/cell_line/get_tab', method='POST')
def get_tab():
  """Downloads a tab-delimeted file of abundance values for the provided JSON inputs for CCLE_protein dataset
  for testing purposes. Also returns an equivalent json via HTTP

  Returns:
    A JSON string representing the associated abundance values of cell_line and gene. See JSON format in README
    Returns Null if input is invalid (including integers) or not found in matrix
  """
  print "REQUEST RECEIVED!!!!"

  # Initialize input dict, CellGene object, output dataframe
  input_set = request.json
  output_df = pd.DataFrame()

  # For all inputs
  for key, val in input_set.iteritems():

    # Make genes uppercase
    input_set[key.upper()] = input_set[key]
    del input_set[key]
    key = key.upper()
    # Make cell lines uppercase
    input_set[key] = [cell.upper() for cell in val] 

    # Remove duplicate cell lines 
    cell_lines = set(input_set[key])

    # Get abundance for its associated cells and append onto output_df
    abundance_list = cg.get_abundance(key, cell_lines)
    # Skip ducplicate genes
    if key in output_df.index.values:
      break

    output_df = output_df.append(abundance_list)


  output_json = output_df.to_json(orient="index")
  output_df.to_csv("file_out.tab", sep="\t")
  response.content_type = "application/json"
  return output_json

@route('/context/expression/cell_line/ids_available/<dataset>', method='GET')
def get_ids(dataset):
  "Returns json of all genes"
  response.content_type = "application/json"
  return cg.get_all_ids()   

@route('/context/expression/cell_line/samples_available/<dataset>', method='GET')
def get_samples(dataset):
  "Returns json of all cell lines"
  response.content_type = "application/json"
  return cg.get_all_samples()   

# Start service
run(host='0.0.0.0', port=8080, debug=True)

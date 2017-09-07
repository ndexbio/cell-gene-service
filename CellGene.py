# Author: Massoud Maher

import pandas as pd
import json

# Maps dataset names to be put in to URL to respective filenames
dataset_dict = {'CCLE_protein':'CCLE_inferred_prot_abundance.tab', 'CCLE_mutations':'CCLE_mutated.tab', 'CCLE_amplifications':'CCLE_amplified.tab', 'CCLE_deletions':'CCLE_deleted.tab'}

class CellGene(object):
  """Class for reading in cell-gene matrix and fetching data from it

  Attributes:
    cell_matrix: Pandas DataFrame with cell-line names as indexing column, gene names as
      column names. The contents of the matrix is the abundance of the associated cell-line / gene
      pair.

  """


  def __init__(self, dataset):
    """Reads cell-gene matrix into memory

    Params:
      dataset name of dataset to be put into URL

    Returns:
      CellGene object with matrix read in
    """

    filename = dataset_dict[dataset]
    self.cell_matrix = pd.read_csv(filename, sep='\t', index_col="Description")

  def test(self):
    """Function to test this class during development"""
    ids = self.get_all_ids()

  def get_abundance(self, cell_line, gene):
    """Fetches the abundance value for a given cell-line / gene pair

    Args:
      cell_line: String that is name of cell line or set of those names
      gene: String that is name of gene or set of those names

    Returns:
      Depending on input (set vs. String):
      a DataFrame of only the desired values if both inputs are sets of at least 2 elements
      a Series if one input is a single value and other is a set
      a numpy number if both inputs are single values
      Returns Null if input is invalid (including integers) or not found in matrix
    """
    try:
      return self.cell_matrix.loc[cell_line, gene]
    except:
     return None


  def get_abundance_json(self, cell_line, gene):
    """Fetches the abundance value for a given cell-line / gene pair

    Args:
      cell_line: String that is name of cell line or set of those names
      gene: String that is name of gene or set of those names

    Returns:
      A JSON string representing the associated abundance values of cell_line and gene in the following format
      Returns Null if input is invalid (including integers) or not found in matrix
    """
    try:
      results = self.cell_matrix.loc[cell_line, gene]
      return results.to_json(orient='index')
    except KeyError:
      return None

  def get_all_ids(self):
    """Returns list of all gene IDs"""
    return json.dumps(list(self.cell_matrix.index.values))

  def get_all_samples(self):
    """Returns json of all cell lines"""
    return json.dumps(list(self.cell_matrix.columns.values))

#cg = CellGene('CCLE_protein')
#cg.test()

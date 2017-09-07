# Author: Massoud Maher

import pandas as pd
import json

# Maps dataset names to be put in to URL to respective filenames
dataset_dict = {'CCLE_protein':'CCLE_inferred_prot_abundance.tab'}

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
    self.cell_matrix = pd.read_csv('CCLE_inferred_prot_abundance.tab', sep='\t', index_col="Description")

  def test(self):
    """Function to test this class during development"""
    ids = self.get_all_ids()

  def get_abundance(self, gene, cell_line):
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
    
    # Check if inputs are valid, remove invalid inputs
    new_params = self.__check_validity(cell_line, gene)
    cell_line = new_params[0]
    gene = new_params[1]

    try:
      return self.cell_matrix.loc[gene, cell_line]
    except:
      print "Error in get_abundance(), cannot get value from: " + str(gene) + ", " + str(cell_line)
      return None

  def __check_validity(self, cell_line, gene):
    """Checks if cell_line and gene are contained in dataset. If not, removes invalid elements and returns pruned parameters

    Args:
      cell_line: String that is name of cell line or set of those names
      gene: String that is name of gene or set of those names

    Return:
      Tuple where 1st element is cell_line, and second element is pruned gene
      Value will be None if no items found in dataset
    """
    # Check if inputs are contained in matrix, remove them if they're not
    count = 0
    if type(cell_line) is set:
      new_cell_line = []
      for item in cell_line:
        # If item is not in matrix, do not copy it over
        if not (item in self.cell_matrix.columns):
          print "*************************************"
          print item + " not found in matrix, skipping"
          continue
        else:
          if count % 5000 == 0:
            print "Appending item %s" % str(item)
          if count > 5000000:
            print 'Reached max item count'
            break
            #raise Exception('Reached max item count')
          new_cell_line.append(item)
          count += 1
        cell_line = new_cell_line
    elif not (cell_line in self.cell_matrix.columns):
      print "*************************************"
      print cell_line + " not found in matrix, data lookup failed"
      cell_line = None

    count = 0
    if type(gene) is set:
      new_gene = []
      for item in gene:
        if not (item in self.cell_matrix.index):
          print "*************************************"
          print item + " not found in matrix, skipping"
        else:
          if count % 5000 == 0:
            print "Appending item %s" % str(item)
          if count > 5000000:
            print 'Reached max item count'
            break
          new_gene.append(item)
        gene = new_gene
    elif not (gene in self.cell_matrix.index):
      print "*************************************"
      print gene + " not found in matrix, data lookup failed"
      gene = None

    return (cell_line, gene)



  def get_all_ids(self):
    """Returns list of all gene IDs"""
    return json.dumps(list(self.cell_matrix.index.values))

  def get_all_samples(self):
    """Returns json of all cell lines"""
    return json.dumps(list(self.cell_matrix.columns.values))

#cg = CellGene('CCLE_protein')
#cg.test()

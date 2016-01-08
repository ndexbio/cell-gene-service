# Class for fetching data from matrix
# Author: Massoud Maher

import pandas as pd
import os

class CellGene:

  # "Contructor" reads cell-gene matrix into memory
  def __init__(self):
    self.cell_matrix = pd.read_csv('CCLE_inferred_prot_abundance.tab', sep='\t', index_col="Description")
    

  # function to test this class during development
  def test(self):
    print self.cell_matrix["X769P_KIDNEY"]

# "main"
cg = CellGene()
cg.test()

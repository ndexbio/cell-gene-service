import json
"""Module for comparing json files output by CellGeneService"""


def compare_outputs(expected_fp, actual_fp):
  """Compares two json objects for equality, order does not matter

    Params:
      expected: filepath of expected json file
      actual: filepath of actual json output file
  """
  expected_json = json.load(open(expected_fp))
  actual_json = json.load(open(actual_fp))

  if(expected_json == actual_json):
    print "Passed!"
  else:
    print "Failed!"
    print expected_fp + " != " + actual_fp


print "Test case 1: duplicate cell lines, lowercase gene and cell-line"
compare_outputs("expected/duplicate_gene_exp.json", "output/duplicate_cell_out.json")

print "Test case 2: duplicate genes"
compare_outputs("expected/duplicate_gene_exp.json", "output/duplicate_gene_out.json")

print "Test case 3: nonexistent gene"
compare_outputs("expected/non_ex_gene_exp.json", "output/non_ex_gene_out.json")

print "Test case 4: nonexistent cell-line"
compare_outputs("expected/non_ex_cell_exp.json", "output/non_ex_cell_out.json")

print "Test case 5: entire cell set is nonexistent"
compare_outputs("expected/many_non_ex_cell_exp.json", "output/many_non_ex_cell_out.json")

print "Test case 6: single cell and gene"
compare_outputs("expected/single_cell_exp.json", "output/single_cell_out.json")

# cell-gene-service
Repo for a REST service that fetches abundance valeus fro gene - cell line pairs


## Description
Service works through POST request with JSON body.

### Input JSON Format
```json
{
  "gene_name" : [
    "cell_line_name",
    "cell_line2_name"
  ],
  "gene_name" : [
    "cell_line_name",
    "cell_line2_name"
  ]
}
```

### Output JSON Format
```json
{
  "gene_name" : {
    "cell_line_name":abundance_val,
    "cell_line2_name": abundance_val
  },
  "gene_name" : {
    "cell_line_name":abundance_val,
    "cell_line2_name": abundance_val
  }
}
```
where abundance_val is a number

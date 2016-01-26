echo "Starting server..."
python CellGeneService.py &

# wait to load dataset before requesting
sleep 10s

# Test case 1: genes with duplicates cell lines, lowercase ( should have some nulls)
curl -H "Content-Type: application/json" --data @duplicate.json http://localhost:8080/context/expression/cell_line > duplicate_out.json
diff duplicate_out.json duplicate_exp.json

# Kill python process
pkill -f CellGeneService.py

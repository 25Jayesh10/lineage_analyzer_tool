import json

with open('index.json') as f:
    index=json.load(f)

with open('ast.json') as f:
    ast=json.load(f)

# Initialize the dictionary to store the outputs

lineage ={}

for proc,meta in index.items() :

    for table in meta.get("tables",[]):
        lineage.setdefault(table, []).append(proc)

    for callee in meta.get("calls", []):
        lineage.setdefault(proc, []).append(callee)

# Step 4: Enrich with ast.json (multiple procedures)
for proc_ast in  ast.get("procedures", []):
    proc_name = proc_ast.get("procedure")
    statements = proc_ast.get("statements", [])

    for stmt in statements:
        tokens = stmt.lower().replace(",", " ").replace("(", " ").replace(")", " ").split()
        for i, token in enumerate(tokens):
            if token in {"from", "into", "update", "join"} and i + 1 < len(tokens):
                table = tokens[i + 1]
                if table.isidentifier():
                   lineage.setdefault(table, []).append(proc_name)

for key in lineage:
    lineage[key] = list(set(lineage[key]))

# Step 6: Write Output
with open("lineage.json", "w") as f:
    json.dump(lineage, f, indent=2)

print("✅ lineage.json generated successfully.")

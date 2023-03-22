import pandas as pd
# Import BeautifulSoup
from bs4 import BeautifulSoup as bs
import os

content = []

# Read the XML file
with open("covid_strategy.pgmx", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
# Combine the lines in the list into a string
content = "".join(content)
bs_content = bs(content, "xml")

criterions = []
for node in bs_content.find("DecisionCriteria").find_all("Criterion"):
    #print (node.get("name"), node.get("unit"))
    criterions.append({"name": node.get("name"), "unit": node.get("unit")})
df = pd.DataFrame.from_records(criterions)
df.to_csv(os.path.join("pgmx_output", "pgmx_output_criterions.tsv"), sep="\t", index=False, na_rep='NULL')


non_util_nodes = []
for node in bs_content.find("Variables").find_all("Variable", role=lambda x: x != 'utility'):
    states = "; ".join([n.get("name") for n in node.find("States").find_all("State")])
    x = int(node.find("Coordinates").get("x"))
    y = int(node.find("Coordinates").get("y"))

    non_util_nodes.append({"name": node.get("name"), "type": node.get("type"), "role": node.get("role"), "states": states, "x": x, "y": y})
    #print (node)
df = pd.DataFrame.from_records(non_util_nodes)
df.to_csv(os.path.join("pgmx_output", "pgmx_output_non_util_nodes.tsv"), sep="\t", index=False, na_rep='NULL')


util_nodes = []
for node in bs_content.find("Variables").find_all("Variable", role=lambda x: x == 'utility'):
    property = node.find("AdditionalProperties")
    x = int(node.find("Coordinates").get("x"))
    y = int(node.find("Coordinates").get("y"))

    non_util_nodes.append({"name": node.get("name"), "type": node.get("type"), "role": node.get("role"), "states": states, "x": x, "y": y})
    #print (node)

links = []
for l in bs_content.find("Links").find_all("Link"):
    
    source, target = [x.get("name") for x in l.find_all("Variable", recursive=False)]
    temp = {"source": source, "target": target}
    
    role = ""
    type_ = ""
    values = ""
    for p in l.find_all("Potential"):
        role = p.get("role")
        type_ = p.get("type")
        ## variables should be the same as the outer loop
        values = p.find("Values").text
        #print (role, type_, values)
    
    if role != "":
        temp["role"] = role
    if type_ != "":
        temp["type"] = type_
    if values != "":
        temp["values"] = values

    revelation_name = ""
    for r in l.find_all("RevelationCondition"):
        for s in r.find_all("State"):
            revelation_name = s.get("name")

    if revelation_name != "":
        temp["revelation_name"] = revelation_name

    links.append(temp)
    
df = pd.DataFrame.from_records(links)
df.to_csv(os.path.join("pgmx_output", "pgmx_output_links.tsv"), sep="\t", index=False, na_rep='NULL')


potentials = []
for potential in bs_content.find("Potentials").find_all("Potential"):
    variables = "; ".join([n.get("name") for n in potential.find("Variables").find_all("Variable")])
    values = potential.find("Values").text
    potentials.append({"type": potential.get("type"), "role": potential.get("role"), "variables": variables, "values": values})
    
df = pd.DataFrame.from_records(potentials)
df.to_csv(os.path.join("pgmx_output", "pgmx_output_potentials.tsv"), sep="\t", index=False, na_rep='NULL')

import pandas as pd
from jinja2 import Environment, FileSystemLoader
import sys
import math

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('unicriterion_pgmx.txt')

def get_pgmx(non_util_nodes_df: pd.DataFrame, util_nodes_df: pd.DataFrame, 
             links_df: pd.DataFrame, potentials_df: pd.DataFrame,
             criterion_df: pd.DataFrame) -> str:
    """
    Args:
        non_util_nodes_df (pd.DataFrame): pandas dataframe with columns: name, type, role, states
        util_nodes_df (pd.DataFrame): pandas dataframe with columns: name, type, role, riterion, precision
        links_df (pd.DataFrame): pandas dataframe with columns: source, target
        potentials_df (pd.DataFrame): pandas dataframe with columns: type, role, variables, values
        criterion_df (pd.DataFrame): pandas dataframe with columns: name, unit, scale

    Returns:
        str: pgmx file
    """

    non_util_nodes_to_jinja = []
    for i, row in non_util_nodes_df.iterrows():
 
        states = [x.strip() for x in row.states.split(";")]
        x = 1+ i * 100
        y = 1+ i * 100

        if "x" in row and row["x"]:
            x = int(row["x"])
        if "y" in row and row["y"]:
            y = int(row["y"])


        non_util_nodes_to_jinja.append({"name": row["name"], "type": row.type, "role": row.role, "states": states, "x": x, "y": y})

    #name	type	role	x	y	criterion	precision
    util_nodes_to_jinja = []
    for i, row in util_nodes_df.iterrows():
        x = 1+ i * 100
        y = 1+ i * 100

        if "x" in row and row["x"]:
            x = int(row["x"])
        if "y" in row and row["y"]:
            y = int(row["y"])

        util_nodes_to_jinja.append({"name": row["name"], "type": row.type, "role": row.role, "x": x, "y": y, "criterion": row.criterion, "precision": row.precision})


    links_to_jinja = []
    #source	target	role	type	values	revelation_name
    for i, row in links_df.iterrows():
        temp = {"source": row["source"], "target": row.target}
        if "role" in row and row["role"]:
            temp["role"] = row.role
        if "type" in row and row["type"]:
            temp["type"] = row.type
        if "values" in row and row["values"]:
            temp["values_"] = row["values"]
        if "revelation_name" in row and not row["revelation_name"] != row["revelation_name"]:
            #print (row.revelation_name. type(row.revelation_name))
            temp["revelation_name"] = row.revelation_name
        #print (temp)

        links_to_jinja.append(temp)



    potentials_to_jinja = []
    #type	role	variables	values	utility_variable
    for i, row in potentials_df.iterrows():
        variables = [x.strip() for x in row.variables.split(";")]
        temp = {"type": row["type"], "role": row.role, "variables": variables, "value": row["values"]}

        if "utility_variable" in row and not row["utility_variable"] != row["utility_variable"]:
            temp["utility_variable"] = row.utility_variable

        potentials_to_jinja.append(temp)

    #name	unit	scale
    criterions_to_jinja = []
    for i, row in criterion_df.iterrows():
        criterions_to_jinja.append({"name": row["name"], "unit": row.unit, "scale": row.scale})


    output = template.render(non_util_nodes=non_util_nodes_to_jinja, links = links_to_jinja, 
                             potentials = potentials_to_jinja, util_nodes= util_nodes_to_jinja,
                             criterions = criterions_to_jinja)
    return (output)

if __name__ == "__main__":
    model = sys.argv[1]

    non_util_nodes = pd.read_csv("./source/pgmx_output_non_util_nodes.tsv", sep="\t")
    util_nodes = pd.read_csv("./source/pgmx_output_util_nodes.tsv", sep="\t")
    links = pd.read_csv("./source/pgmx_output_links.tsv", sep="\t")
    potentials = pd.read_csv("./source/pgmx_output_potentials.tsv", sep="\t")
    criterions = pd.read_csv("./source/pgmx_output_criterions.tsv", sep="\t")

    

    model_non_util_nodes = non_util_nodes[non_util_nodes['model'].notna()]
    mask = model_non_util_nodes['model'].str.split(";").apply(lambda x: model in [e.strip() for e in x])
    model_non_util_nodes = model_non_util_nodes[mask]

    model_util_nodes = util_nodes[util_nodes['model'].notna()]
    mask = model_util_nodes['model'].str.split(";").apply(lambda x: model in [e.strip() for e in x])
    model_util_nodes = model_util_nodes[mask]
    
    
    model_links = links[links['model'].notna()]
    mask = model_links['model'].str.split(";").apply(lambda x: model in [e.strip() for e in x])
    model_links = model_links[mask]

    model_potentials = potentials[potentials['model'].notna()]
    mask = model_potentials['model'].str.split(";").apply(lambda x: model in [e.strip() for e in x])
    model_potentials = model_potentials[mask]

    model_criterions = criterions[criterions['model'].notna()]
    mask = model_criterions['model'].str.split(";").apply(lambda x: model in [e.strip() for e in x])
    model_criterions = model_criterions[mask]
    #print (model_potentials.head())

    pgmx = get_pgmx(model_non_util_nodes, model_util_nodes, model_links, model_potentials, model_criterions)
    print (pgmx)
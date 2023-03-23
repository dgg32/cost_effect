import pandas as pd
import yaml
import sys
import tsv_to_pgmx

model = sys.argv[1]


with open("config.yaml", "r") as stream:
    try:
        PARAM = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

sheet_id = PARAM["google_sheet_id"]
non_util_nodes_sheet = PARAM["google_sheet_non_util_node"]
util_nodes_sheet = PARAM["google_sheet_util_node"]
criterion_sheet = PARAM["google_sheet_criterion"]
links_sheet = PARAM["google_sheet_link"]
potentials_name = PARAM["google_sheet_potentials"]

non_util_nodes_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={non_util_nodes_sheet}"
non_util_nodes = pd.read_csv(non_util_nodes_url)

util_nodes_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={util_nodes_sheet}"
util_nodes = pd.read_csv(util_nodes_url)

links_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={links_sheet}"
links = pd.read_csv(links_url)

potentials_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={potentials_name}"
potentials = pd.read_csv(potentials_url)

criterions_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={criterion_sheet}"
criterions = pd.read_csv(criterions_url)

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

pgmx = tsv_to_pgmx.get_pgmx(model_non_util_nodes, model_util_nodes, model_links, model_potentials, model_criterions)

print (pgmx)
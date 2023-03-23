import pandas as pd
import os


output_folder = "./neo4j"

def to_neo4j(non_util_nodes_df: pd.DataFrame, util_nodes_df:pd.DataFrame, links_df: pd.DataFrame):
    """
    Args:
        non_util_nodes_df (pd.DataFrame): pandas dataframe with columns: name, type, role, states
        links_df (pd.DataFrame): pandas dataframe with columns: source, target

    Returns:
    """

    node_labels = pd.unique(non_util_nodes_df['label'])

    for l in node_labels:
        temp_df = non_util_nodes_df[non_util_nodes_df['label'] == l][["name", "role", "description", "model"]]
        temp_df.to_csv(os.path.join(output_folder, l.lower() + ".tsv"), sep="\t", index=False, na_rep='NULL')

    node_labels = pd.unique(util_nodes_df['label'])

    for l in node_labels:
        temp_df = util_nodes_df[util_nodes_df['label'] == l][["name", "role", "description", "model"]]
        temp_df.to_csv(os.path.join(output_folder, l.lower() + ".tsv"), sep="\t", index=False, na_rep='NULL')

    link_labels = pd.unique(links_df['label'])

    for l in link_labels:
        temp_df = links_df[links_df['label'] == l][["source", "target", "model"]]
        temp_df.to_csv(os.path.join(output_folder, l.lower() + ".tsv"), sep="\t", index=False, na_rep='NULL')


if __name__ == "__main__":

    non_util_nodes = pd.read_csv("./source/pgmx_output_non_util_nodes.tsv", sep="\t")
    util_nodes = pd.read_csv("./source/pgmx_output_util_nodes.tsv", sep="\t")
    links = pd.read_csv("./source/pgmx_output_links.tsv", sep="\t")

    to_neo4j(non_util_nodes, util_nodes, links)
from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import rdflib
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from src.helpers import get_labels

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setTimeout(20)
schema = rdflib.Namespace("http://schema.org/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
ocs = rdflib.Namespace("https://w3id.org/ocs/ont/")



def get_graph(directory, ui):
    graph = Graph()
    graph.bind("ocs", ocs)
    no_files = len(os.listdir(directory))
    no_entities_added = 0
    with ui.Progress(min=0, max=no_files) as p:
        for i, filename in enumerate(os.listdir(directory)):
            p.set(i, message = f'Adding file {i} to the graph')
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                new_node = Graph()
                new_node.parse(f)
                graph += new_node
                no_entities_added +=1
    return graph, no_entities_added


def get_entities_to_find(g):
    enitites_to_find = pd.DataFrame(
        [(str(o), s) for s, p, o in g.triples((None, SKOS.closeMatch, None))],
        columns=["uri", "filename"],
    )
    return enitites_to_find


def get_translations(enitites_to_find, language, ui):
    names = ["(dbr:" + uri.split("/").pop() + ")" for uri in enitites_to_find["uri"]]
    names = [
        uri.split("/")
        .pop()
        .replace("*", "\*")
        .replace("(", "\(")
        .replace(")", "\)")
        .replace(",", "\,")
        .replace("'", "\\'")
        for uri in enitites_to_find["uri"]
    ]
    names = ["(dbr:" + uri + ")" for uri in names]

    labels = []
    no_names = len(names)
    with ui.Progress(min=0, max=no_names) as p:
        for idx_start in range(0, no_names, 10):
            idx_end = idx_start + 10
            p.set(idx_start, message = f'Adding translations for files {idx_start} to {idx_end}')
            labels.append(get_labels(names[idx_start:idx_end], language))
    labels_df = pd.concat(labels)
    return labels_df

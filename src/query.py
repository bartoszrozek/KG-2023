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


def get_graph(directory):
    g = Graph()
    g.bind("ocs", ocs)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            new_node = Graph()
            new_node.parse(f)
            g += new_node
    return g


def get_entities_to_find(g):
    enitites_to_find = pd.DataFrame(
        [(str(o), s) for s, p, o in g.triples((None, SKOS.closeMatch, None))],
        columns=["uri", "filename"],
    )
    return enitites_to_find


def get_translations(enitites_to_find, language):
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
    for idx_start in range(0, len(names), 10):
        idx_end = idx_start + 10
        labels.append(get_labels(names[idx_start:idx_end], language))
    labels_df = pd.concat(labels)
    return labels_df

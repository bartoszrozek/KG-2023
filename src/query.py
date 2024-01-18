import rdflib
from rdflib import Graph
from rdflib.namespace import SKOS
import rdflib
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setTimeout(20)
schema = rdflib.Namespace("http://schema.org/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
ocs = rdflib.Namespace("https://w3id.org/ocs/ont/")


def get_graph(directory, ui):
    """
    Loads entities from the .ttl files present in the given directory and creates graph out of them.
    The logging is performed using the provided ui.
    """
    graph = Graph()
    graph.bind("ocs", ocs)
    no_files = len(os.listdir(directory))
    no_entities_added = 0
    with ui.Progress(min=0, max=no_files) as p:
        for i, filename in enumerate(os.listdir(directory)):
            p.set(i, message=f"Adding file {i} to the graph")
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                new_node = Graph()
                new_node.parse(f)
                graph += new_node
                no_entities_added += 1
    return graph, no_entities_added


def get_entities_to_find(g):
    """
    Returns URIs and filenames of the entities from the graph that have a DBpedia match.
    """
    enitites_to_find = pd.DataFrame(
        [(str(o), s) for s, p, o in g.triples((None, SKOS.closeMatch, None))],
        columns=["uri", "filename"],
    )
    return enitites_to_find


def get_translations(enitites_to_find, language, ui):
    """
    Fetches the translations from DBpedia for provided entities in a provided language.
    This is done 10 entites at the time due to limitations of the RDFLib query, using the get_labels() function for every chunk.
    The logging is performed using the provided ui.
    """
    names = ["(<" + uri + ">)" for uri in enitites_to_find["uri"]]
    labels = []
    no_names = len(names)
    with ui.Progress(min=0, max=no_names) as p:
        for idx_start in range(0, no_names, 10):
            idx_end = idx_start + 10
            p.set(
                idx_start,
                message=f"Adding translations for files {idx_start} to {idx_end}",
            )
            labels.append(get_labels(names[idx_start:idx_end], language))
    labels_df = pd.concat(labels)
    return labels_df

def get_labels(uris, language):
    """
    Executes the RDFSlib query for provided URIs, fetching their labels in the provided language.
    """
    language_labels = []
    enitity_names = []
    bsl = "\n"
    query = f"""

    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT DISTINCT
        ?uri ?label 
    WHERE {{
        VALUES (?uri) {{{bsl.join(uris)}}}
        ?uri rdfs:label ?label
        FILTER (lang(?label) = '{language}')
    }}
    LIMIT 1000
    """
    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()

        for r in ret["results"]["bindings"]:
            language_labels.append(r["label"]["value"])
            enitity_names.append(r["uri"]["value"])
    except Exception as e:
        print(e)

    labels_df = pd.DataFrame({"uri": enitity_names, "label": language_labels})
    return labels_df

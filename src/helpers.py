from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import rdflib
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setTimeout(20)
schema = rdflib.Namespace("http://schema.org/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")


def get_labels(uris, language):
    language_labels = []
    enitity_names = []
    bsl = "\n"
    # needs to be divied into chunks due to limitations of the rdfslib query
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


def get_o(entity):
    return entity[2]

from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setTimeout(20)
schema = rdflib.Namespace("http://schema.org/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
ocs = rdflib.Namespace("https://w3id.org/ocs/ont/")


def save_graph(changed_enities, g, language, directory, ui):

    changed_enities_names = [str(entity) for entity in changed_enities["filename"]]
    graph_triples = {}
    for s, p, o in g.triples((None, None, None)):
        if str(s) in changed_enities_names:
            entity_name = s.split("/").pop()
            if entity_name not in graph_triples.keys():
                graph_triples[entity_name] = []
                # graph_triples[entity_name].bind("ocs", ocs)
            graph_triples[entity_name].append((s, p, o))
    graph = {}
    for key, value in graph_triples.items():
        # value.sort(key = get_o)
        g = Graph()
        g.bind("ocs", ocs)
        for s, p, o in value:
            g.add((s, p, o))
        graph[key] = g

    for _, row in changed_enities.iterrows():
        uri = row["filename"].split("/").pop()
        label = Literal(row["label"], lang=language)
        graph[uri].add((rdflib.term.URIRef(ocs[uri]), SKOS.prefLabel, label))

    for key, value in graph.items():
        value.serialize(destination=directory + key + ".ttl")

    m = ui.modal(
            "Translations saved successfully",
            title="Success",
            easy_close=True,
            footer=None,
        )
    ui.modal_show(m)

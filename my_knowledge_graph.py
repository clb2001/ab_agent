import spacy
import networkx as nx
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')

def extract_entities_relations(text):
    doc = nlp(text)
    entities = []
    relations = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    for token in doc:
        if token.dep_ in ('ROOT', 'relcl', 'ccomp'):
            subject = [w for w in token.lefts if w.dep_ == 'nsubj']
            object_ = [w for w in token.rights if w.dep_ in ('dobj', 'attr')]
            if subject and object_:
                relations.append((subject[0].text, token.lemma_, object_[0].text))
    return entities, relations

def build_knowledge_graph(entities, relations):
    G = nx.DiGraph()
    for entity, label in entities:
        G.add_node(entity, label=label)
    for subj, rel, obj in relations:
        G.add_edge(subj, obj, label=rel)
    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=5, node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=5)
    plt.savefig('./pics/graph.pdf', format='pdf')

with open("./docs/info.txt") as f:
    text = f.read()

if __name__=='__main__':
    entities, relations = extract_entities_relations(text)
    G = build_knowledge_graph(entities, relations)

    visualize_graph(G)

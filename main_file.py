import networkx as nx
import matplotlib.pyplot as plt
import random

class LLMConnector:
    def __init__(self, llm_name):
        self.llm_name = llm_name

    def get_keywords(self, subject):
        """Simulate an LLM response with related keywords and scores."""
        # Placeholder for actual API call
        sample_keywords = {
            "AI": ["Machine Learning", "Neural Networks", "Deep Learning", "NLP", "Computer Vision"],
            "Finance": ["Stocks", "Bonds", "Derivatives", "Risk Management", "XVA"],
            "Physics": ["Quantum Mechanics", "Relativity", "Thermodynamics", "Electromagnetism", "Optics"]
        }
        keywords = sample_keywords.get(subject, [f"{subject} Related {i}" for i in range(5)])
        return {kw: random.randint(1, 10) for kw in keywords}

class KeywordGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.keywords_store = set()  # To store processed keywords

    def add_keywords(self, source, keywords):
        for kw, weight in keywords.items():
            if kw not in self.keywords_store:
                self.graph.add_edge(source, kw, weight=weight)
                self.keywords_store.add(kw)
            else:
                self.graph[source][kw]['weight'] += weight
                
    def expand_graph(self, llm_connector, depth=1):
        for _ in range(depth):
            new_keywords = list(self.graph.nodes())
            for keyword in new_keywords:
                if keyword not in self.keywords_store:
                    kw_dict = llm_connector.get_keywords(keyword)
                    self.add_keywords(keyword, kw_dict)

    def display_graph(self, initial_subject):
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'weight')

        # Color nodes: initial subject in red, others in lightblue
        node_colors = ['red' if node == initial_subject else 'lightblue' for node in self.graph.nodes()]

        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color=node_colors, edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

# Example Usage
if __name__ == "__main__":
    llm = LLMConnector("FakeLLM")
    graph = KeywordGraph()

    subject = "AI"
    initial_keywords = llm.get_keywords(subject)
    graph.add_keywords(subject, initial_keywords)

    graph.expand_graph(llm, depth=1)
    graph.display_graph(subject)

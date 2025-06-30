# GraphViz export logic
import os
from graphviz import Digraph
os.environ["PATH"] = r"C:\Program Files\Graphviz-13.0.0-win32\bin" + os.pathsep + os.environ["PATH"]
import  re

def sanitize(text):
    clean = str(text).replace('"', "'").replace("\n", " ").strip()
    clean = re.sub(r"[<>\\]", "", clean)
    return clean[:120] + "..." if len(clean) > 120 else clean

def export_to_svg(graph_data, file_name="output_graph", output_dir="data/outputs"):
    dot = Digraph(format="svg")
    dot.attr(bgcolor="white")
    dot.attr("graph", rankdir="TB", ranksep="2.5", nodesep="1.5")
    dot.attr("node", shape="box", style="filled,setlinewidth(3)", width="2", height="1", fontsize="24",
             fillcolor="#FFF8DC", fontname="Helvetica-Bold", color="#FFB300", fontcolor="#000000")
    dot.attr("edge", color="#999999", arrowsize="1.4", penwidth="2.0")

    seen = set()
    for node in graph_data["nodes"]:
        name = sanitize(node["name"])
        if name and name not in seen:
            dot.node(name)
            seen.add(name)

    for edge in graph_data["edges"]:
        source = sanitize(edge["source"])
        target = sanitize(edge["target"])
        if source and target:
            dot.edge(source, target)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name)
    dot.render(output_path, format="svg", cleanup=True)
    return f"{output_path}.svg"

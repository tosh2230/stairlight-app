import streamlit as st
from graphviz import Digraph

from stairlight import StairLight


def get_dependency_map():
    stairlight = StairLight()
    return stairlight.mapped


def main():
    st.title("Table Dependency Map")
    dependency_map = get_dependency_map()
    graph = Digraph(format="png")

    for downstream_table, upstream_dict in dependency_map.items():
        graph.node(downstream_table)
        for upstream_table, upstream_details in upstream_dict.items():
            graph.node(upstream_table)
            graph.edge(upstream_table, downstream_table)
    st.graphviz_chart(graph)


if __name__ == "__main__":
    main()

import streamlit as st
from graphviz import Digraph

from stairlight import StairLight


@st.cache
def call_stairlight():
    return StairLight()


def create_graph(title, dependency_map):
    graph = Digraph(title, format="svg")
    graph.attr(
        bgcolor="#0e1117",
    )
    graph.attr(
        "node",
        shape="box",
        color="white",
        fontcolor="white",
    )
    graph.attr(
        "edge",
        color="white",
        fontcolor="white",
    )

    for downstream_table, upstream_dict in dependency_map.items():
        graph.node(downstream_table)
        for upstream_table, upstream_details in upstream_dict.items():
            graph.node(upstream_table)
            graph.edge(
                upstream_table,
                downstream_table,
                label=upstream_details.get("uri"),
                tooltip=upstream_details.get("uri"),
            )
    return graph


def main():
    st.set_page_config(layout="wide")
    title = "Table Dependency Map"
    st.title(title)
    stairlight = call_stairlight()
    st.graphviz_chart(create_graph(title, stairlight.mapped), use_container_width=True)

    with st.expander(label="Show details(JSON)", expanded=False):
        st.write(stairlight.mapped)


if __name__ == "__main__":
    main()

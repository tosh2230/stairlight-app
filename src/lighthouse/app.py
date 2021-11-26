import streamlit as st
from graphviz import Digraph

from stairlight import StairLight

TITLE = "Table Dependency Map"
BASE_COLOR = "white"
SELECTED_TABLE_COLOR = "green"
RELATIVE_TABLE_COLOR = "blue"


@st.cache(allow_output_mutation=True)
def call_stairlight():
    return StairLight()


def get_table_set(dependency_map):
    table_set = set("-")
    for downstream_table, upstream_dict in dependency_map.items():
        table_set.add(downstream_table)
        for upstream_table in upstream_dict:
            table_set.add(upstream_table)
    return sorted(table_set)


def create_relative_nodes(graph, downstream, upstream):
    graph.node(downstream[0], color=downstream[1])
    graph.node(upstream[0], color=upstream[1])


def create_graph(stairlight, selected_table):
    graph = Digraph(TITLE, format="svg")
    graph.attr(bgcolor="#0e1117")
    graph.attr("node", shape="box", color=BASE_COLOR, fontcolor=BASE_COLOR)
    graph.attr("edge", color=BASE_COLOR, fontcolor=BASE_COLOR)

    upstream_tables: list = stairlight.up(
        table_name=selected_table, recursive=True, verbose=False
    )
    downstream_tables: list = stairlight.down(
        table_name=selected_table, recursive=True, verbose=False
    )
    relative_tables: list = upstream_tables + downstream_tables

    for downstream_table, upstream_dict in stairlight.mapped.items():
        for upstream_table, upstream_details in upstream_dict.items():
            if downstream_table == selected_table:
                downstream_color = SELECTED_TABLE_COLOR
                upstream_color = RELATIVE_TABLE_COLOR
                create_relative_nodes(
                    graph,
                    (downstream_table, downstream_color),
                    (upstream_table, upstream_color),
                )
            elif upstream_table == selected_table:
                downstream_color = RELATIVE_TABLE_COLOR
                upstream_color = SELECTED_TABLE_COLOR
                create_relative_nodes(
                    graph,
                    (downstream_table, downstream_color),
                    (upstream_table, upstream_color),
                )
            elif upstream_table in relative_tables:
                downstream_color = upstream_color = RELATIVE_TABLE_COLOR
                create_relative_nodes(
                    graph,
                    (downstream_table, downstream_color),
                    (upstream_table, upstream_color),
                )

            graph.edge(
                upstream_table,
                downstream_table,
                label=upstream_details.get("uri"),
                tooltip=upstream_details.get("uri"),
            )
    return graph


def main():
    st.set_page_config(layout="wide")
    st.title(TITLE)

    stairlight = call_stairlight()

    # Side bar
    table_set = get_table_set(dependency_map=stairlight.mapped)
    selected_table = st.sidebar.selectbox("Select a table", list(table_set), index=0)

    # Main page
    st.graphviz_chart(
        create_graph(
            stairlight=stairlight,
            selected_table=selected_table,
        ),
        use_container_width=True,
    )

    with st.expander(label="Show details(JSON)", expanded=False):
        if selected_table == "-":
            st.write(stairlight.mapped)
        else:
            st.subheader("Upstream")
            st.write(
                stairlight.up(table_name=selected_table, recursive=True, verbose=True)
            )
            st.subheader("Downstream")
            st.write(
                stairlight.down(table_name=selected_table, recursive=True, verbose=True)
            )


if __name__ == "__main__":
    main()

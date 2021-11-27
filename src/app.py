import streamlit as st
from graphviz import Digraph
from stairlight import StairLight

TITLE = "Table Dependency Map"
BASE_COLOR = "#e8e1cc"
SELECTED_NODE_COLOR = "green"
RELATIVE_NODE_COLOR = "blue"
LABEL_COLOR = "#bab0ac"
TABLE_NOT_SELECTED = "-"


@st.experimental_memo
def call_stairlight():
    return StairLight()


def get_table_set(dependency_map):
    table_set = set(TABLE_NOT_SELECTED)
    for downstream_table, upstream_dict in dependency_map.items():
        table_set.add(downstream_table)
        for upstream_table in upstream_dict:
            table_set.add(upstream_table)
    return sorted(table_set)


def create_relative_nodes(graph, rendered_table_set, downstream, upstream):
    graph.node(downstream[0], color=downstream[1])
    graph.node(upstream[0], color=upstream[1])
    rendered_table_set.add(downstream[0])
    rendered_table_set.add(upstream[0])


def render_graph(stairlight, graph, selected_table, is_set_label):
    upstream_tables: list = stairlight.up(
        table_name=selected_table, recursive=True, verbose=False
    )
    downstream_tables: list = stairlight.down(
        table_name=selected_table, recursive=True, verbose=False
    )
    relative_tables: list = upstream_tables + downstream_tables

    rendered_table_set = set()
    for downstream_table, upstream_dict in stairlight.mapped.items():
        for upstream_table, upstream_details in upstream_dict.items():
            is_create = False

            label = None
            if is_set_label:
                label = upstream_details.get("uri")

            if downstream_table == selected_table:
                downstream_color = SELECTED_NODE_COLOR
                upstream_color = RELATIVE_NODE_COLOR
                is_create = True
            elif upstream_table == selected_table:
                downstream_color = RELATIVE_NODE_COLOR
                upstream_color = SELECTED_NODE_COLOR
                is_create = True
            elif upstream_table in relative_tables:
                downstream_color = upstream_color = RELATIVE_NODE_COLOR
                is_create = True
            elif (
                downstream_table not in rendered_table_set
                and upstream_table not in rendered_table_set
            ):
                downstream_color = upstream_color = BASE_COLOR
                is_create = True

            if is_create:
                create_relative_nodes(
                    graph=graph,
                    rendered_table_set=rendered_table_set,
                    downstream=(downstream_table, downstream_color),
                    upstream=(upstream_table, upstream_color),
                )

            graph.edge(
                upstream_table,
                downstream_table,
                label=label,
                tooltip=upstream_details.get("uri"),
            )


def create_graph(stairlight, selected_table, is_set_label):
    graph = Digraph(TITLE, format="svg")
    graph.attr(bgcolor="#0e1117")
    graph.attr("node", shape="box", color=BASE_COLOR, fontcolor=BASE_COLOR)
    graph.attr("edge", color=BASE_COLOR, fontcolor=LABEL_COLOR)

    render_graph(
        stairlight=stairlight,
        graph=graph,
        selected_table=selected_table,
        is_set_label=is_set_label,
    )
    return graph


def main():
    st.set_page_config(layout="wide")
    st.title(TITLE)
    st.markdown("This is a demo app using Stairlight.")

    stairlight = call_stairlight()

    # Side bar
    st.sidebar.subheader("Parameters")
    table_set = get_table_set(dependency_map=stairlight.mapped)
    selected_table = st.sidebar.selectbox("Table", list(table_set))

    is_set_label = st.sidebar.checkbox("Show file names", False)

    st.sidebar.subheader("GitHub Links")
    stairlight_link = "[stairlight](https://github.com/tosh2230/stairlight)"
    st.sidebar.markdown(stairlight_link, unsafe_allow_html=True)
    stairlight_app_link = "[stairlight-app](https://github.com/tosh2230/stairlight-app)"
    st.sidebar.markdown(stairlight_app_link, unsafe_allow_html=True)

    # Main page
    st.graphviz_chart(
        create_graph(
            stairlight=stairlight,
            selected_table=selected_table,
            is_set_label=is_set_label,
        ),
        use_container_width=True,
    )

    with st.expander(label="Show Details", expanded=False):
        if selected_table == TABLE_NOT_SELECTED:
            st.json(stairlight.mapped)
        else:
            st.subheader("Upstream")
            st.json(
                stairlight.up(table_name=selected_table, recursive=True, verbose=True)
            )
            st.subheader("Downstream")
            st.json(
                stairlight.down(table_name=selected_table, recursive=True, verbose=True)
            )


if __name__ == "__main__":
    main()

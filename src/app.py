import streamlit as st
from graphviz import Digraph
from stairlight import StairLight
from stairlight.source.config_key import MappingConfigKey


TITLE = "Table Dependency Graph"
BASE_COLOR = "#e8e1cc"
BACKGROUND_COLOR = "#0e1117"
SELECTED_NODE_COLOR = "green"
RELATIVE_NODE_COLOR = "blue"
LABEL_COLOR = "#bab0ac"
TABLE_NOT_SELECTED = "-"


@st.experimental_memo
def call_stairlight() -> StairLight:
    stairlight = StairLight()
    stairlight.create_map()
    return stairlight


def get_table_set(dependency_map: dict) -> set:
    table_set = set(TABLE_NOT_SELECTED)
    for downstairs, upstairs_dict in dependency_map.items():
        table_set.add(downstairs)
        for upstairs in upstairs_dict:
            table_set.add(upstairs)
    return sorted(table_set)


def create_node(
    graph: Digraph, table: str, color: str, rendered_table_set: set
) -> None:
    graph.node(table, color=color)
    rendered_table_set.add(table)


def render_graph(
    graph: Digraph, stairlight: StairLight, selected_table: str, is_set_label: bool
) -> None:
    upstairs_list: list = stairlight.up(
        table_name=selected_table, recursive=True, verbose=False
    )
    downstairs_list: list = stairlight.down(
        table_name=selected_table, recursive=True, verbose=False
    )
    relative_tables = upstairs_list + downstairs_list

    rendered_table_set = set()
    for downstairs, upstairs_dict in stairlight.mapped.items():
        for upstairs, upstairs_details in upstairs_dict.items():
            is_create = False
            label = None

            if is_set_label:
                label = upstairs_details.get(MappingConfigKey.Gcs.URI)

            if downstairs == selected_table:
                downstairs_color = SELECTED_NODE_COLOR
                upstairs_color = RELATIVE_NODE_COLOR
                is_create = True
            elif upstairs == selected_table:
                downstairs_color = RELATIVE_NODE_COLOR
                upstairs_color = SELECTED_NODE_COLOR
                is_create = True
            elif upstairs in relative_tables:
                downstairs_color = upstairs_color = RELATIVE_NODE_COLOR
                is_create = True
            elif (
                downstairs not in rendered_table_set
                and upstairs not in rendered_table_set
            ):
                downstairs_color = upstairs_color = BASE_COLOR
                is_create = True

            if is_create:
                create_node(
                    graph=graph,
                    table=downstairs,
                    color=downstairs_color,
                    rendered_table_set=rendered_table_set,
                )
                create_node(
                    graph=graph,
                    table=upstairs,
                    color=upstairs_color,
                    rendered_table_set=rendered_table_set,
                )

            graph.edge(
                upstairs,
                downstairs,
                label=label,
                tooltip=upstairs_details.get(MappingConfigKey.Gcs.URI),
            )


def create_graph(
    stairlight: StairLight, selected_table: str, is_set_label: bool
) -> Digraph:
    graph = Digraph(TITLE, format="svg")
    graph.attr(bgcolor=BACKGROUND_COLOR)
    graph.attr("node", shape="box", color=BASE_COLOR, fontcolor=BASE_COLOR)
    graph.attr("edge", color=BASE_COLOR, fontcolor=LABEL_COLOR)

    render_graph(
        graph=graph,
        stairlight=stairlight,
        selected_table=selected_table,
        is_set_label=is_set_label,
    )
    return graph


def main():
    st.set_page_config(page_title="Stairlight", layout="wide")
    st.title(TITLE)
    st.markdown("Stairlight demo app")

    stairlight = call_stairlight()

    # Side bar
    st.sidebar.subheader("Parameters")
    table_set = get_table_set(dependency_map=stairlight.mapped)
    selected_table = st.sidebar.selectbox("Node", list(table_set))

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

    with st.expander(label="Details", expanded=False):
        if selected_table == TABLE_NOT_SELECTED:
            st.json(stairlight.mapped)
        else:
            result_up = stairlight.up(
                table_name=selected_table, recursive=True, verbose=True
            )
            if result_up.get(selected_table):
                st.subheader("Upstairs")
                st.json(result_up)

            result_down = stairlight.down(
                table_name=selected_table, recursive=True, verbose=True
            )
            if result_down.get(selected_table):
                st.subheader("Downstairs")
                st.json(result_down)


if __name__ == "__main__":
    main()

from shiny import App, render, ui, reactive
import string
import random
import os
import pandas as pd
from src.query import get_translations, get_entities_to_find, get_graph
from src.save_graph import save_graph

app_ui = ui.page_fluid(
    ui.include_css("styles.css"),
    ui.div(ui.panel_title("OpenCS translation tool"), id="title-div"),
    ui.div(
        ui.div(ui.span("Options"), class_="title"),
        ui.div(
            ui.column(
                4,
                ui.input_text(id="load_opencs", label="OpenCS directory:"),
            ),
            ui.column(
                3,
                ui.input_select(id="opencs_folder", label="Select folder", choices=[]),
            ),
            ui.column(
                3,
                ui.input_text(
                    id="language_select", label="Select language:", value="pl"
                ),
            ),
            id="arrows-div",
        ),
        ui.div(
            ui.input_action_button("load_open_cs_folders", "Load OpenCS"),
            ui.input_action_button("query_labels", "Make query"),
            style="display: flex; justify-content: space-between;",
        ),
        id="load-div",
        class_="title_box",
        style="margin-bottom: 15px",
    ),
    ui.div(
        ui.div(ui.span("Translation"), class_="title"),
        ui.div(
            ui.input_action_button("previous_entity", "<"),
            ui.input_action_button("next_entity", ">"),
            id="switch_entities",
        ),
        ui.output_ui("entity_header"),
        ui.div(
            ui.span("Entity"),
            ui.output_text_verbatim("current_entity"),
            id="current_entity_div",
        ),
        ui.div(
            ui.span("Translation"),
            ui.output_ui("current_translation"),
            id="translation_div",
        ),
        ui.div(
            ui.input_action_button("save_new_translation", "Save translation"),
            style="display: flex; justify-content: right;",
        ),
        id="main_div",
        class_="title_box",
        style="margin-bottom: 15px",
    ),
    ui.div(
        ui.div(ui.span("Save\xa0results"), class_="title"),
        ui.div(
            ui.input_action_button(id="save_opencs", label="Save to OpenCS"),
            style="display: flex; justify-content: right;",
        ),
        id="save-div",
        class_="title_box",
        style="margin-bottom: 15px",
    ),
    style="padding: 0",
)


def server(input, output, session):
    entities = reactive.Value(
        [
            "".join([random.choice(string.ascii_letters) for i in range(10)])
            for i in range(100)
        ]
    )
    translations = reactive.Value(
        [
            "".join([random.choice(string.ascii_letters) for i in range(10)])
            for i in range(100)
        ]
    )

    which_entity = reactive.Value(1)
    enitites_to_find_rc = reactive.Value()
    graph_rc = reactive.Value()

    @reactive.Calc
    def directory_rc():
        return input.load_opencs() + input.opencs_folder() + "/"

    @reactive.Calc
    def curr_entity():
        return entities()[which_entity()]

    @reactive.Calc
    def curr_translation():
        return translations()[which_entity()]

    @reactive.Effect
    @reactive.event(input.previous_entity, ignore_init=True)
    def _():
        if which_entity() == 1:
            pass
        else:
            which_entity.set(which_entity() - 1)

    @reactive.Effect
    @reactive.event(input.next_entity, ignore_init=True)
    def _():
        if which_entity() == len(entities()):
            pass
        else:
            which_entity.set(which_entity() + 1)

    @reactive.Effect
    @reactive.event(input.load_open_cs_folders, ignore_init=True)
    def _():
        folders = [x[0].split("/").pop() for x in os.walk(input.load_opencs())]
        if len(folders) > 0:
            ui.update_select("opencs_folder", choices=folders, selected=folders[1])

    @reactive.Effect
    @reactive.event(input.query_labels, ignore_init=True)
    def _():
        graph = get_graph(directory_rc())
        enitites_to_find = get_entities_to_find(graph)
        enitites_to_find_rc.set(enitites_to_find)
        graph_rc.set(graph)
        translations_df = get_translations(enitites_to_find, input.language_select())
        entities.set(list(translations_df.uri))
        translations.set(list(translations_df.label))

    @reactive.Effect
    @reactive.event(input.save_new_translation, ignore_init=True)
    def _():
        with reactive.isolate():
            translations_to_change = translations()
            translations_to_change[which_entity()] = input.translation()
            translations.set(translations_to_change)

    @reactive.Effect
    @reactive.event(input.save_opencs, ignore_init=True)
    def _():
        with reactive.isolate():
            labels_df = pd.DataFrame({"uri": entities(), "label": translations()})
            enitites_to_find = enitites_to_find_rc()
            g = graph_rc()
            language = input.language_select()
            directory = directory_rc()
        changed_enities = labels_df.merge(enitites_to_find, on="uri", how="left")
        save_graph(changed_enities, g, language, directory)

    @output
    @render.ui
    def entity_header():
        h_tag = ui.h4(f"Entity {which_entity()}/{len(entities())}")
        return h_tag

    @output
    @render.ui
    def current_translation():
        h_tag = ui.input_text(
            id="translation", label="", value=curr_translation(), width="700px"
        )
        return h_tag

    @output
    @render.text
    def current_entity():
        return str(curr_entity())


app = App(app_ui, server)

from shiny import App, render, ui, reactive
import string
import random

app_ui = ui.page_fluid(
    ui.include_css("styles.css"),
    ui.div(ui.panel_title("OpenCS translation tool"), id="title-div"),
    ui.div(
        ui.div(ui.span("Load\xa0data"), class_="title"),
        ui.div(
            ui.input_file(id="load_opencs", label="Load OpenCS"),
            ui.input_file(id="load_dbpedia", label="Load DBPedia"),
            id="arrows-div",
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
            ui.download_button(id="save_opencs", label="Save OpenCS"),
            style="display: flex; justify-content: right;",
        ),
        id="save-div",
        class_="title_box",
        style="margin-bottom: 15px",
    ),
    style="padding: 0",
)


def server(input, output, session):
    entities = [
        "".join([random.choice(string.ascii_letters) for i in range(10)])
        for i in range(100)
    ]
    translations = [
        "".join([random.choice(string.ascii_letters) for i in range(10)])
        for i in range(100)
    ]

    which_entity = reactive.Value(1)
    curr_entity = reactive.Value(entities[0])
    curr_translation = reactive.Value(translations[0])

    @reactive.Effect
    @reactive.event(input.previous_entity, ignore_init=True)
    def _():
        if which_entity() == 1:
            pass
        else:
            which_entity.set(which_entity() - 1)
            curr_entity.set(entities[which_entity() - 1])
            curr_translation.set(translations[which_entity() - 1])

    @reactive.Effect
    @reactive.event(input.next_entity, ignore_init=True)
    def _():
        if which_entity() == len(entities):
            pass
        else:
            which_entity.set(which_entity() + 1)
            curr_entity.set(entities[which_entity() - 1])
            curr_translation.set(translations[which_entity() - 1])

    @output
    @render.ui
    def entity_header():
        h_tag = ui.h4(f"Entity {which_entity()}/{len(entities)}")
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

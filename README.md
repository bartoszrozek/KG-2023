# OpenCS Translation Tool

This Shiny application allows you to find DBpedia translations for entities in the OpenCS ontology, manually correct and save them.

It was developed as a project for Knowledge Graphs course (WUT MiNI 2023).


## Run the application

### Using Docker

To run the application in docker first clone the repository to your local drive

`git clone https://github.com/bartoszrozek/KG-2023`

Cd into the directory

`cd KG-2023`

Build docker image

`docker build -t kg_app .`

Run docker

`docker run -p 4000:8080 kg_app`

The application will be accessible at `http://127.0.0.1:4000`

You will also need to copy the OpenCS directory into the docker. To do so, first check your container's ID.

`docker ps`

You will find the CONTAINER ID in the line which has kg_app as IMAGE.

Then copy the directory with OpenCS into the container (assuming that OpenCS is in the current directory)

`docker cp OpenCS/ |YOUR CONTAINER ID|:/home/app`

After the work, copy the OpenCS directory back

`docker cp |YOUR CONTAINER ID|:/home/app/OpenCS OpenCS`

In the application, you should provide 

`/home/app/OpenCS/ontology/core/`

as the path to OpenCS

### Using the virtual environment
To run the application first clone the repository to your local drive

`git clone https://github.com/bartoszrozek/KG-2023`

Cd into the directory

`cd KG-2023`

Create a Python virtual environment

`python -m venv venv`

Use a newly created virtual environment

- Linux/MacOS:
`source venv/bin/activate`

- Windows in PowerShell:
`venv\Scripts\Activate.ps1`

Install all dependencies needed

`pip install -r requirements.txt`

Run the application

`shiny run --reload`

App should be accessible at `http://127.0.0.1:8000`

## User manual

1. Clone the OpenCS ontology repository to your device from https://github.com/OpenCS-ontology/OpenCS.
2. In the app, provide an OpenCS directory pulled from GitHub. The path up to the folder core (f.e. C:/.../OpenCS/ontology/core/) should be provided. Remember about the / at the end of the path.
3. Click "Load OpenCS" to load folders.
4. Select the folder to analyze in the dropdown.
5. Select language in appropriate text input. This string will be passed to
the SPARQL query so it has to be a proper language tag (f.e pl, en).
6. Click the button "Make query" to query external services for the proposi-
tion of the labels. Pop-out box in the right bottom corner will inform
about the progress. A big window will pop out at the end of the
process to present the statistics of the query.
7. Use arrows to go through the proposed labels and correct them if
needed. Use "Save translation" to replace the original translation with a
corrected one.
8. Click the "Save to OpenCS" button the save entities to the drive. A
pop-out window will inform you about the end of the process.
9. (Outside the tool) Create a pull request to contribute your translations to OpenCS



## Acknowledgement

We use the implementation of ConceptIRI class to ensure proper ordering when saving the OpenCS .ttl files. To achieve that, we use the codes from https://github.com/OpenCS-ontology/ci-worker/blob/main/opencs/concept_iri.py#L6 and https://github.com/OpenCS-ontology/ci-worker/blob/d982233fff3602cb33095ab8ece7594db2d4abd3/split_concepts.py#L47.



# User guide

> **Note:** For installation and setup instructions, see the [README](../README.md).

## Glossary

| Term | Meaning |
| --- | --- |
| Document | An imported text file and its metadata. |
| Concept | A predefined argument to search for in a document. |
| Golden standard | Human-coded reference annotations for comparison with model results. |
| Aitta | The external service through which the application calls language models. |

## Before you start

You need a running PostgreSQL database, imported data, and an Aitta API key. Start with the [installation instructions](../README.md#installing-the-application). The application currently has a terminal interface.

From the project root, run:

```sh
uv run src/index.py
```

You can also use `make app` if Make is installed.

## Menu commands

Enter a command number at the main menu. Analysis commands use the model displayed above the menu. Use command `3` before starting an analysis if you want to change it.

| Command | Action |
| --- | --- |
| `0` - Quit | Exit the terminal application. |
| `1` - Etsi valitut konseptit tiedostosta | Analyse one selected document using selected concepts. |
| `2` - Aitta prompti | Analyse the first loaded document using up to the first two concepts. |
| `3` - Vaihda tekoälymallia | Change the language model for this session. |
| `4` - Tulosta golden standard tiedostoille | View reference concepts for selected documents. |
| `5` - Suorita batch-prosessointi | Run the limited batch analysis. |
| `6` - F1 MVP | Calculate evaluation metrics using predefined test data. |
| `7` - Encoding test | Display the encoding of predefined test data. |

## Interpreting results

Results are displayed as JSON:

| Field | Meaning |
| --- | --- |
| `document_id` | The document's internal database ID  |
| `concept_id` | The concept's internal database ID. |
| `concept` | The concept text. |
| `present` | `true` if the model identifies the concept in the text; otherwise `false`. |
| `passage` | The supporting excerpt returned by the model, or `null` when the concept is absent. |
| `agreement` | `true` if the author endorses the argument, `false` if the author rejects it, or `null` when no stance is given. |

An argument can appear in a passage that rejects it, so `present: true` and `agreement: false` can occur together.

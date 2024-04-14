# notion_emojifier
Notion Emojifier is a Python tool that automatically assigns emojis to Notion pages in a 
database, based on their titles. GPT-4 is used to find fun, relevant emojis. 

Why have boring database tickets when you can have a nice, visual, themed database?

_________________

[![PyPI version](https://badge.fury.io/py/notion_emojifier.svg)](http://badge.fury.io/py/notion_emojifier)
[![Test Status](https://github.com/apockill/notion_emojifier/workflows/Test/badge.svg?branch=main)](https://github.com/apockill/notion_emojifier/actions?query=workflow%3ATest)
[![Lint Status](https://github.com/apockill/notion_emojifier/workflows/Lint/badge.svg?branch=main)](https://github.com/apockill/notion_emojifier/actions?query=workflow%3ALint)
[![codecov](https://codecov.io/gh/apockill/notion_emojifier/branch/main/graph/badge.svg)](https://codecov.io/gh/apockill/notion_emojifier)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
_________________

## Key Features
- **Automatic Emoji Assignment**: Applies relevant fitting emojis to page titles based on their content.
- **Selective Processing**: Only updates pages that do not already have an emoji, reducing unnecessary API calls.
- **Backup Capabilities**: Offers the option to backup page IDs that were modified during the emoji application process,
    in case you want to revert the changes in the future.

## Installation and Usage

```shell
# Install dependencies
poetry install
poetry run emojify_notion \
  --notion-key 'your_notion_api_key' \
  --openai-key 'your_openai_api_key' \
  --database-id 'your_notion_database_id' \
  --database-description 'A task database for a robotics company, with SWE and mechanical engineering tasks.'
```

While running, you might see logs like:
```shell
Applying emoji 🗓️ to page with title 'Make Wednesday TODO list'
Applying emoji 💡 to page with title 'Tune lighting parameters with the blinders'
Applying emoji 🔊 to page with title 'Get the sound working on the robot'
...
Emoji already exists for page url: {REMOVED}. Skipping...
...
Applying emoji 🚮 to page with title 'Delete the unused URDFs'
Applying emoji 🔄 to page with title 'Rebuild the calibration workflow'
Applying emoji 🔕 to page with title 'Disable alerts for the fastener query'
Applying emoji 🔁 to page with title 'See if toggling the node components improves robustness'
```


## Development

### Installing python dependencies
```shell
poetry install
```

### Running Tests
```shell
pytest .
```

### Formatting Code
```shell
bash .github/format
```

### Linting
```shell
bash .github/check_lint
```
# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import sys
from .config import settings
from .utilities import llm_soup_to_text, new_plato_text
import click
import fileinput


@click.command()
@click.option('--provider-api-key', envvar='PROVIDER_API_KEY',
              default='no_provider_key', help='Language Model API provider key.')
@click.option('--github-token', envvar='GITHUB_TOKEN',
              default='', help='GitHub API token for private repo access.')
def run(provider_api_key, github_token, mode):
    """
        $ text | ./run.py                   # Accepts text from the pipe
        $ ./run.py /home/user/file.txt      # Reads file.
        $ ./run.py < /home/user/file.txt    # Reads file.

        secrets come through the environment variables.
    """
    if provider_api_key:
        if provider_api_key.startswith('sk-proj-'):
            settings['provider'] = 'OpenAI'
            environ['OPENAI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('sk-ant-'):
            settings['provider'] = 'Anthropic'
            environ['ANTHROPIC_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('AIzaSy'):
            settings['provider'] = 'Gemini'
            environ['GEMINI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('gsk_'):
            settings['provider'] = 'Groq'
            environ['GROQ_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('xai-'):
            settings['provider'] = 'XAI'
            environ['XAI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('LLM|'):
            settings['provider'] = 'Meta'
            environ['META_API_KEY'] = provider_api_key
        else:
            if settings['provider'] == '':
                raise ValueError(f"Unrecognized API key prefix and no provider specified.")
    if github_token:
        environ['GITHUB_TOKEN'] = github_token

    raw_input = ''
    for line in fileinput.input(encoding="utf-8"):
        raw_input += line

    from .machine import machine

    try:
        thoughts, text = machine(raw_input)
        output = raw_input + '\n\n' + new_plato_text(thoughts, text, settings['name'])
        sys.stdout.write(output)
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f'Machine did not work {e}')
        sys.stderr.flush()
        sys.exit(0)


if __name__ == '__main__':
    run()

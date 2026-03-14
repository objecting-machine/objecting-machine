# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ, path
from .config import settings
from .githf import fetch_instructions
from .utilities import (plato_text_to_muj,
                        plato_text_to_mpuj,
                        llm_soup_to_text)


def machine(plato_text, **kwargs):
    """Core agent logic.

    1. Fetches the system prompt from a private GitHub repo.
    2. Calls Provider
    3. Returns a (thoughts, text) tuple.
    """
    # Fetch the confidential system prompt, name is for a checkup.
    name, system_prompt = fetch_instructions()

    # Load an appropriate library and query the API.
    provider = settings['provider']
    api_key  = settings['provider_api_key']
    if provider == 'OpenAI':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['OPENAI_API_KEY'] = api_key
        import opehaina
        thoughts, text = opehaina.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'Gemini':
        # Transform plato_text to MPUJ format
        messages = plato_text_to_mpuj(plato_text=plato_text,
                                     machine_name=name)
        # Call Gemini through castor-polux
        environ['GEMINI_API_KEY'] = api_key
        import castor_pollux
        thoughts, text = castor_pollux.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'Anthropic':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)

        # Call the Anthropic API via electroid
        environ['ANTHROPIC_API_KEY'] = api_key
        import electroid
        text, thoughts = electroid.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )
        return text, thoughts

    elif provider == 'Groq':
        ...
    elif provider == 'Xai':
        ...
    elif provider == 'Meta':
        ...


if __name__ == '__main__':
    machine([])

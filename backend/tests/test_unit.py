# test_module.py
import pytest
import asyncio

from utils.tools import (
    schema_validator,
    style_parser,
    prompt_censorer,
    generate_random_id,
)


@pytest.mark.asyncio
async def test_schema_validator():
    class FakeWebsocket:
        async def receive_json(self):
            return {
                "user_id": "adam",
                "prompt": "大象在潛水",
                "preset": "写实",
                "size": "16:9",
                "mode": "turbo",
            }

        async def send_text(self, text):
            return True

    fake_websocket = FakeWebsocket()
    data = await schema_validator(fake_websocket)
    assert data == {
        "user_id": "adam",
        "prompt": "大象在潛水",
        "preset": "写实",
        "size": "16:9",
        "mode": "turbo",
    }


@pytest.mark.asyncio
async def test_style_parser():
    prompt = "some prompt"
    nprompt = "some nprompt"
    style = "漫画"
    result = await style_parser(prompt, nprompt, style)
    assert result == "some prompt, anime --niji 5 --no some nprompt"


@pytest.mark.asyncio
async def test_prompt_censorer():
    # Test that banned words are removed
    prompt = "Wang"
    result = await prompt_censorer(prompt)
    assert result == ""  # All words should be removed

    # Test that allowed words are not removed
    prompt = "chubby"
    result = await prompt_censorer(prompt)
    assert result == "chubby"  # Words should not be removed


def test_generate_random_id():
    # asyncio.run is used to run an asyncio function from synchronous code
    random_id = asyncio.run(generate_random_id())
    assert len(random_id) == 10  # Check the length
    assert random_id.isalnum()  # Check if it contains only alphanumeric characters

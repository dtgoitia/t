from src.types import EntryChoice


def test_entry_choice_to_words():
    entry = EntryChoice(name="foo", project="bar")
    prompt_word = entry.to_prompt()
    assert prompt_word == "foo @ bar"

"""some tests need human interaction as a messagebox and filedialog are presented to the user
    test ar running from the project root folder
"""
import os
import glob
import pytest
from click.testing import CliRunner
from transcribetools import cli


def remove_output_files(pattern="*.txt"):
    # Find all .txt files in the data directory
    txt_files = glob.glob(f'data/{pattern}')

    # Remove each file
    for file in txt_files:
        os.remove(file)
        print(f"Removed: {file}")


@pytest.fixture
def translate_setup(text_nl="Dit is een voorbeeld tekst met een paar woorden",
                    text_en="This is a sample text with a few words"):
    # Find all .txt files in the data directory

    fname = "data/test.txt"
    with open(fname, 'w') as file:
        file.write(text_nl)
    yield text_en
    # Remove each file
    os.remove(fname)
    print(f"Removed: {fname}")


# Function to initialize setup
@pytest.fixture
def transcribe_setup(request):
    print("setup transcribe")
    remove_output_files()
    yield  # This yields None, which is fine for a setup/teardown fixture
    print("teardown")
    # remove_output_files()


# Function to initialize setup
@pytest.fixture
def translate_setup2(request):
    print("setup translate")
    remove_output_files()
    yield  # This yields None, which is fine for a setup/teardown fixture
    print("teardown")
    # remove_output_files()


# noinspection PyTypeChecker
def tst_config_create() -> None:
    runner = CliRunner()
    # strange type error, related to?
    # https://stackoverflow.com/questions/70467389/how-to-fix-mypy-error-when-using-clicks-pass-context
    result = runner.invoke(cli,
                           ['config', 'create'],
                           input='large\n\n')
    response = result.return_value
    print(f"{response=}")
    assert ": large" in result.stdout  # feedback model choice


# noinspection PyTypeChecker
def test_config_show() -> None:
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--configfilename', 'tests/transcribefolder.toml', 'config', 'show'])
    print(result.stdout)
    assert result.exit_code == 0
    assert ": large" in result.stdout  # feedback model choice


# noinspection PyTypeChecker,PyUnusedLocal
def test_process(transcribe_setup):
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--configfilename', 'tests/transcribefolder.toml', 'transcribe'])
    assert result.exit_code == 0
    assert "saved" in result.stdout


# noinspection PyTypeChecker
def test_translate(translate_setup):
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--configfilename', 'tests/transcribefolder.toml', 'deeple_translate'])
    assert result.exit_code == 0
    assert translate_setup in result.stdout

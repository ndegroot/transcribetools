"""some tests need human interaction as a messagebox and filedialog are presented to the user
    test ar running from the project root folder
"""
import os
import glob
import pytest
from click.testing import CliRunner
from transcribetools import cli


def remove_output_files():
    # Find all .txt files in the data directory
    txt_files = glob.glob('data/*.txt')

    # Remove each file
    for file in txt_files:
        os.remove(file)
        print(f"Removed: {file}")



# Function to initialize setup
@pytest.fixture
def transcribe_setup(request):
    print("setup")
    remove_output_files()
    yield  # This yields None, which is fine for a setup/teardown fixture
    print("teardown")
    # remove_output_files()


def tst_config_create():
    runner = CliRunner()
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
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


# noinspection PyTypeChecker
def test_process(transcribe_setup):
    # transcribe_setup()
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--configfilename', 'tests/transcribefolder.toml', 'transcribe'])
    assert result.exit_code == 0
    assert "saved" in result.stdout

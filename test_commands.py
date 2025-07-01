from click.testing import CliRunner
import transcribetools.local_whisper as commands
"""test needs human interaction as a messagebox and filedialog are presented to the user"""


def test_config_create():
    runner = CliRunner()
    # t = type(run)
    # t = is <class 'rich_click.rich_command.RichCommand'>
    # next line generates warning on 'run' arg 'Expected type 'BaseCommand' but it is 'Any'
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
    # noinspection PyTypeChecker
    # noinspection PyTypeChecker
    result = runner.invoke(commands.cli,
                           ['config', 'create'],
                           input='large\n\n')
    response = result.return_value
    print(f"{response=}" )
    # input='ndegroot\ntheol_credo')
    assert ": large" in result.stdout  # feedback model choice
    assert "(localwhisper.toml)" in result.stdout


# noinspection PyTypeChecker
def test_config_show():
    runner = CliRunner()
    # t = type(run)
    # t = is <class 'rich_click.rich_command.RichCommand'>
    # next line generates warning on 'run' arg 'Expected type 'BaseCommand' but it is 'Any'
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
    result = runner.invoke(commands.cli,
                           ['config', 'show'])
    # no user input
    assert result.exit_code == 0
    assert ": large" in result.stdout  # feedback model choice


# noinspection PyTypeChecker
def test_process():
    runner = CliRunner()
    # t = type(run)
    # t = is <class 'rich_click.rich_command.RichCommand'>
    # next line generates warning on 'run' arg 'Expected type 'BaseCommand' but it is 'Any'
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
    result = runner.invoke(commands.cli,
                           ['process'])
    # no user input
    assert result.exit_code == 0
    assert "string" in result.stdout




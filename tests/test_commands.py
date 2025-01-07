from click.testing import CliRunner
from transcribetools.local_whisper import cli


def test_config_create():
    runner = CliRunner()
    # t = type(run)
    # t = is <class 'rich_click.rich_command.RichCommand'>
    # next line generates warning on 'run' arg 'Expected type 'BaseCommand' but it is 'Any'
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
    result = runner.invoke(cli,
                           ['config', 'create'])
                           # input='ndegroot\ntheol_credo')
    assert result.exit_code == 0
    # assert 'Nico de Groot' in result.output
    # assert '4472' in result.output


def test_config_show():
    runner = CliRunner()
    # t = type(run)
    # t = is <class 'rich_click.rich_command.RichCommand'>
    # next line generates warning on 'run' arg 'Expected type 'BaseCommand' but it is 'Any'
    # https://stackoverflow.com/questions/77845322/unexpected-warning-in-click-cli-development-with-python
    result = runner.invoke(cli,
                           ['config', 'show'])
                           # input='ndegroot\ntheol_credo')
    assert result.exit_code == 0
    # assert 'Nico de Groot' in result.output
    # assert '4472' in result.output





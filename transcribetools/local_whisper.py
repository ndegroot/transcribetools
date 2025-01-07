from datetime import datetime
import logging
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox as mb
import toml
import whisper
import rich
from rich.prompt import Prompt
import rich_click as click
from result import Result, is_ok, is_err, Ok, Err
from .local_wisper_model import save_config_to_toml, get_config_from_toml, ask_choice, show_config

# logging.getLogger("python3").setLevel(logging.ERROR)
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# tk bug in sequoia
# import sys
# sys.stderr = open("log", "w", buffering=1)
# can't find the 'python3' logger to silence

MODEL = "large"
# LOCALPATH = ('/Users/ncdegroot/Library/CloudStorage/'
#              'OneDrive-Gedeeldebibliotheken-TilburgUniversity/'
#              'Project - Reflective cafe - data')
LOCALPATH = Path.cwd()
model = None


def process_file(path):
    output_path = path.with_suffix('.txt')
    try:
        print("Start processing...")
        result = model.transcribe(str(path), verbose=True)
        # false: only progressbar; true: all; no param: no feedback
    except Exception as e:
        print(f"Error while processing {path}: '{e}'. Please fix it")
    else:
        text_to_save = result["text"]
        print(text_to_save)

        # file_name = f"{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
        # file_name = output_path
        # Open the file in write mode
        with open(output_path, 'w') as file:
            # Write the text to the file
            file.write(text_to_save)

        print(f'Text has been saved to {output_path}')


@click.group(no_args_is_help=True,
             epilog='Check out the docs at https://gitlab.uvt.nl/tst-research/transcribetools for more details')
@click.version_option(package_name='transcribetools')
@click.pass_context  # our 'global' context
@click.option("--config",
              default="config.toml",
              help="Specify config file to use")
@click.option("--init",
              default=False,
              is_flag=True,
              help="Create config.toml file")
def cli(ctx: click.Context, config, init):
    global model
    # open config, ask for values is needed:
    #  Prompt.ask(msg)
    toml_path = Path("config.toml")
    if not toml_path.exists():
        save_config_to_toml(toml_path, LOCALPATH, MODEL)
    result = get_config_from_toml(toml_path)
    if is_err(result):
        print(f"Exiting due to {result.err}")
        exit(1)
    config = result.ok_value
    if config:
        print(f"Config filename: {toml_path}")
        print(f"Config folder path: {config.folder}")
        print(f"Config model name: {config.model}")

    ctx.obj = config
    # process_files(config)


# define multi commands/groups
@cli.group("config")
def config():
    pass


@cli.command("process", help="Using current configuration transcribe all soundfiles in the folder")
@click.option("--config",
              default="config.toml",
              help="Specify config file to use",
              show_default=True,
              metavar="FILE",
              type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
              show_choices=False,
              required=False,
              prompt="Enter config file name",
              )
@click.pass_obj
def process(config):
    global model
    config = config
    model = whisper.load_model(config.model)
    # internal_path = pathlib.Path('data')
    soundfiles_path = Path(config.folder)
    txt_files = [file for file in soundfiles_path.glob('*') if file.suffix.lower() == '.txt']
    file_stems = [file.stem for file in txt_files]
    # file_stem indicates mp3 has been processed already
    mp3_files = [file for file in soundfiles_path.glob('*') if file.suffix.lower() == '.mp3' and
                 file.stem not in file_stems]
    print(f"{len(mp3_files)} files to be processed")
    for file in mp3_files:
        print(f"Processing {file}")
        process_file(file)


@cli.command("create", help="Create new configuration file")
def create():
    msg = "Select folder to monitor containing the sound files"
    click.echo(msg)
    root = tk.Tk()
    root.focus_force()
    # Cause the root window to disappear milliseconds after calling the filedialog.
    # root.after(100, root.withdraw)
    tk.Tk().withdraw()
    # hangs: mb.showinfo("msg","Select folder containing the sound files")
    folder = askdirectory(title="Select folder to monitor containing the sound files", mustexist=True, initialdir='~')
    choices = ["tiny", "base", "small", "medium", "large"]
    # inx = ask_choice("Choose a model", choices)
    # model = choices[inx]
    model = Prompt.ask("Choose a model", choices=choices)
    config_name = Prompt.ask("Enter a name for the configuration file",
                             show_default=True, default="config.toml")
    config_path = Path(config_name)
    toml_path = config_path.with_suffix(".toml")
    while toml_path.exists():  # current dir
        result = get_config_from_toml(toml_path)
        rich.echo("[red]Already exists[/red]")
        show_config(result)
        overwrite = Prompt.ask("Overwrite?", choices=["y", "n"], default="n", show_default=True)
        if overwrite == "y":
            break
        else:
            return
    # Prompt.ask("Enter model name")
    save_config_to_toml(toml_path, folder, model)
    click.echo(f"{toml_path} saved")


@cli.command("show", help="Show current configuration file")
@click.pass_obj
def show(config):
    click.echo(f"Config folder path: {config.folder}")
    click.echo(f"Config model name: {config.model}")


config.add_command(create)
config.add_command(show)

if __name__ == "__main__":
    cli()

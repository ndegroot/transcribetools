from datetime import datetime
import logging
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
# from tkinter import messagebox as mb
import pymsgbox as msgbox
import toml
import whisper
import rich
from rich.prompt import Prompt
import rich_click as click
from result import Result, is_ok, is_err, Ok, Err
from .local_wisper_model import save_config_to_toml, get_config_from_toml, ask_choice, show_config, console

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
@click.option("--configfilename",
              default="localwhisper.toml",
              help="Specify config file to use",
              show_default=True,
              metavar="FILE",
              type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
              show_choices=False,
              required=False,
              prompt="Enter config filename",
              )
def cli(ctx: click.Context, configfilename):
    global model
    # open config, ask for values if needed:
    #  Prompt.ask(msg)
    home = Path.home()
    config_path = home / configfilename
    if not config_path.exists():
        save_config_to_toml(config_path, LOCALPATH, MODEL)
    result = get_config_from_toml(config_path)
    if is_err(result):
        click.echo(f"Exiting due to {result.err}")
        exit(1)
    config = result.ok_value
    if config:
        # click.echo("Config")
        click.echo(f"Config filename: {config_path}")
        # click.echo(f"Folder path for soundfiles: {config.folder}")
        # click.echo(f"Transcription model name: {config.model}")

    ctx.obj = config
    # process_files(config)


# the `cli` subcommand 'process'

@cli.command("process", help="Using current configuration, transcribe all soundfiles in the folder")
# @click.option("--filename",
#               default="localwhisper.toml",
#               help="Specify config file to use",
#               show_default=True,
#               metavar="FILE",
#               type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
#               show_choices=False,
#               required=False,
#               prompt="Enter config file name",
#               )
@click.pass_obj  # in casu the config obj
def process(config):
    global model
    # config = config
    model = whisper.load_model(config.model)
    soundfiles_path = Path(config.folder)
    txt_files = [file for file in soundfiles_path.glob('*') if file.suffix.lower() == '.txt']
    file_stems = [file.stem for file in txt_files]
    # a txt file_stem indicates mp3 has been processed already
    mp3_files = [file for file in soundfiles_path.glob('*') if file.suffix.lower() == '.mp3' and
                 file.stem not in file_stems]
    click.echo(f"{len(mp3_files)} files to be processed")
    for file in mp3_files:
        click.echo(f"Processing {file}")
        process_file(file)


# the `cli` command config
@cli.group("config")
def config():
    pass


# the `config` create subcommand
@click.command("create", help="Create new configuration file")
def create():
    msg = "Select folder to monitor containing the sound files"
    click.echo(msg)
    # root = tk.Tk()
    # root.focus_force()
    # Cause the root window to disappear milliseconds after calling the filedialog.
    # root.after(100, root.withdraw)
    # tk.Tk().withdraw()
    # hangs: mb.showinfo("msg","Select folder containing the sound files")
    msgbox.alert(msg, "info")
    # "title" only supported on linux ith wv ...
    folder = askdirectory(title="Select folder to monitor containing the sound files",
                          mustexist=True,
                          initialdir='~')
    choices = ["tiny", "base", "small", "medium", "large"]
    # inx = ask_choice("Choose a model", choices)
    # model = choices[inx]
    model = Prompt.ask("Choose a model",
                       console=console,
                       choices=choices,
                       show_default=True,
                       default="large")
    config_name = Prompt.ask("Enter a name for the configuration file",
                             show_default=True,
                             default="localwhisper.toml")
    config_path = Path(config_name)
    toml_path = config_path.with_suffix(".toml")
    while toml_path.exists():  # current dir
        result = get_config_from_toml(toml_path)
        click.secho("Already exists...", fg='red')
        show_config(result)
        overwrite = Prompt.ask("Overwrite?",
                               choices=["y", "n"],
                               default="n",
                               show_default=True)
        if overwrite == "y":
            break
        else:
            return
    # Prompt.ask("Enter model name")
    save_config_to_toml(toml_path, folder, model)
    click.echo(f"{toml_path} saved")


# the 'config' show subcommand
@click.command("show", help="Show current configuration file")
@click.pass_obj
def show(config):
    click.echo(f"Config folder path: {config.folder}")
    click.echo(f"Config model name: {config.model}")


# connect the subcommand to `config'
config.add_command(create)
config.add_command(show)

if __name__ == "__main__":
    cli()

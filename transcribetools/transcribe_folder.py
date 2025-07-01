import time
from pathlib import Path

# import tkinter as tk
from tkinter.filedialog import askdirectory

# from tkinter import messagebox as mb
import pymsgbox as msgbox

# import toml
import whisper

# import rich
from rich.prompt import Prompt
import rich_click as click
from result import Result, is_ok, is_err, Ok, Err  # noqa: F401
import soundfile as sf

from .transcribe_folder_model import (
    save_config_to_toml,
    get_config_from_toml,
    show_config,
    console,
)

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


def process_file(path, args):
    """open file, transcribe using args and save to file"""
    output_path = path.with_suffix(".txt")
    try:
        click.echo("Start processing...")
        result = model.transcribe(
            str(path),
            verbose=True,
            **args,
        )
        # false: only progressbar; true: all; no param: no feedback
    except Exception as e:
        click.echo(f"Error while processing {path}: '{e}'. Please fix it")
    else:
        text_to_save = result["text"]
        click.echo(text_to_save)

        # file_name = f"{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
        # file_name = output_path
        # Open the file in write mode
        with open(output_path, "w") as file:
            # Write the text to the file
            file.write(text_to_save)

        click.echo(f"Text has been saved to {output_path}")


def translate_it(input_path: Path, translator, args):
    """open the file on this path, translate using args and save to file"""
    output_path = input_path.with_stem(
        str(input_path.stem).replace(args["source_lang"], args["target_lang"])
    )
    # else
    if args["target_lang"] not in input_path.stem:
        output_path = input_path.with_stem(input_path.stem + "-" + args["target_lang"])

    # if doc(x) or other formatted files
    if input_path.suffix != ".txt":
        # Using translate_document_from_filepath() with file paths
        translator.translate_document_from_filepath(
            input_path, output_path, **args
        )
    else:  # txt
        with open(input_path, "r", encoding="utf-8") as infile:

            try:
                click.echo("Start translating...")
                result = translator.translate_text(
                    text=infile.read(),
                    **args,
                )
                # false: only progressbar; true: all; no param: no feedback
            except Exception as e:
                click.echo(f"Error while processing {input_path}: '{e}'. Please fix it")
            else:
                text_to_save = result.text
                click.echo(text_to_save)

                # file_name = f"{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
                # file_name = output_path
                # Open the file in write mode
                #
                # existing replace

                with open(output_path, "w") as outfile:
                    # Write the text to the file
                    outfile.write(text_to_save)

                    click.echo(f"Text has been saved to {output_path}")


@click.group(
    no_args_is_help=True,
    epilog="Use config --help or process --help to see options.\n"
    "Check out the docs at https://gitlab.uvt.nl/tst-research/transcribetools "
    "for more details",
)
@click.version_option(package_name="transcribetools")
@click.option(
    "--debug/--no-debug",
    "-d/-n",
    help="Print debug messages and timing information",
    default=False,
)
@click.pass_context  # our 'global' context
@click.option(
    "--configfilename",
    "-c",
    default=Path.home() / "localwhisper.toml",
    help="Specify config file to use",
    # show_default=True,
    metavar="FILE",
    type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
    show_choices=False,
    required=False,
    # prompt="Enter new config filename or accept default",
)
def cli(ctx: click.Context, debug, configfilename):
    global model
    # open config, ask for values if needed:
    #  Prompt.ask(msg)
    home = Path.home()
    config_path = home / configfilename
    if debug:
        click.echo(f"Config_path: {config_path}")
    if not config_path.exists():
        save_config_to_toml(config_path, LOCALPATH, MODEL)
    result = get_config_from_toml(
        config_path
    )  # has the default values (homedir, large)
    if is_err(result):
        click.echo(f"Exiting due to {result.err}")
        exit(1)
    config = result.ok_value
    if config:
        # click.echo("Config")
        click.echo(f"Config filename: {config_path}")
        # click.echo(f"Folder path for soundfiles: {config.folder}")
        # click.echo(f"Transcription model name: {config.model}")
    config.debug = debug
    ctx.obj = config
    # process_files(config)


# the `cli` subcommand 'process'


@cli.command(
    "transcribe",
    help="Using current configuration, transcribe all soundfiles in the folder",
)
@click.option(
    "--language",
    "-l",
    default="AUTO",
    type=click.Choice(
        ["nl", "en", "AUTO"],
        case_sensitive=False,
    ),
)
@click.option(
    "--select_folder",
    "-s",
    default=False,
    flag_value=True,
    help="Override the path to the soundfiles from config, select a folder",
)
@click.option(
    "--prompt",
    "-p",
    help='-p "" You can add special prompts and words (spelling) (max 224 chars) see '
    "https://cookbook.openai.com/examples/whisper_prompting_guide",
)
@click.pass_obj  # in casu the config obj
def transcribe(config, select_folder, prompt, language):
    global model
    # config = config
    if config.debug:
        click.echo(f"Load model: {config.model}")
    model = whisper.load_model(config.model)
    soundfiles_path = Path(config.folder)
    if config.debug:
        click.echo(f"Folder path for soundfiles: {soundfiles_path}")
        click.echo(f"{language=}, {prompt=} ")

    if select_folder:
        soundfiles_path = Path(
            askdirectory(
                title="Select folder containing the sound files",
                mustexist=True,
                initialdir="~",
            )
        )

    txt_files = [
        file for file in soundfiles_path.glob("*") if file.suffix.lower() == ".txt"
    ]
    file_stems = [file.stem for file in txt_files]
    # a txt file_stem indicates mp3 has been processed already (skip file with nio suffix
    soundfiles = [
        file
        for file in soundfiles_path.glob("*")
        if file.suffix.lower()
        in (".mp3", "mp3", ".mp4", ".mpweg", ".mpga", ".m4a", ".wav", ".webm")
        and file.stem not in file_stems
    ]
    click.echo(f"{len(soundfiles)} files to be processed")
    duration = 0
    start = time.perf_counter()

    for file in soundfiles:
        f, samplerate = sf.read(file)
        duration += len(f) / samplerate
        click.echo(f"Processing {file}")
        args = dict()
        if language != "AUTO":
            args["language"] = language
        if prompt:
            args["prompt"] = prompt
        process_file(file, args)
    if soundfiles:
        process_time = time.perf_counter() - start
        click.echo(
            f"Total sound duration: {duration:.1f} seconds, \n"
            f"processing time: {process_time:.1f} seconds, \n"
            f"realtime factor: {(process_time / duration):.2f}"
        )


@cli.command(
    "deeple_translate",
    help="Using current configuration, translate all txt/doc/docx files in the folder",
)
@click.option(
    "--source_language",
    "-sl",
    default="NL",
    show_default=True,
    type=click.Choice(
        ["NL", "EN-GB", "EN-US", "AUTO"],
        case_sensitive=False,
    ),
)
@click.option(
    "--target_language",
    "-tl",
    default="EN-GB",
    type=click.Choice(
        ["EN-GB", "EN-US", "NL"],
        case_sensitive=False,
    ),
)
@click.option(
    "--select_folder",
    "-s",
    default=False,
    flag_value=True,
    help="Override the path to the files from config, select a folder",
)
@click.option(
    "--prompt",
    "-p",
    help='-p "" You can add special prompts see https://www.deepl.com/en/pro-api',
)
@click.pass_obj  # in casu the config obj
def deeple_translate(config, select_folder, prompt, source_language, target_language):
    import deepl
    import keyring as kr

    if source_language == target_language:
        raise click.BadParameter(f"Nothing to do {source_language} -> {target_language}")

    valid_choices = ["EN-GB", "EN-US", "NL"]

    if target_language not in valid_choices:
        raise click.BadParameter(f"Invalid {target_language=} should be in {valid_choices}")

    service_name = "DeeplAPI"
    key = "auth_key"
    # time.sleep(30)

    auth_key = kr.get_password(service_name=service_name, username=key)
    if auth_key is None:
        key = Prompt.ask("Paste your auth key here")
        kr.set_password(service_name=service_name, username=key, password=key)

    translator = deepl.Translator(auth_key)

    sourcefiles_path = Path(config.folder)
    if config.debug:
        click.echo(f"Folder path for sourcefiles: {sourcefiles_path}")
        click.echo(f"{source_language=} -> {target_language=}, {prompt=} ")

    if select_folder:
        sourcefiles_path = Path(
            askdirectory(
                title="Select folder containing the source files",
                mustexist=True,
                initialdir="~",
            )
        )

    translated_files = [
        file
        for file in sourcefiles_path.glob("*")
        if f"{target_language}" in file.stem and file.suffix.lower() == ".txt"
    ]
    file_stems = [file.stem for file in translated_files]
    # file has been processed already (skip file with no suffix
    translate_file_paths = [
        file
        for file in sourcefiles_path.glob("*")
        if file.suffix.lower() in (".txt", ".doc", ".docx")
        and file.stem not in file_stems
    ]
    # candidates heave text-like suffix and no translation yet (no file in folder with target language code
    click.echo(f"{len(translate_file_paths)} files to be processed")

    for file in translate_file_paths:
        if "~$" in file.name:
            click.echo(f"Skipping {file}")
            continue
        click.echo(f"Processing {file}")
        args = dict()
        args['target_lang'] = target_language
        if source_language != "AUTO":
            args["source_lang"] = source_language
        if prompt:
            args["prompt"] = prompt
        translate_it(file, translator, args)


# the `cli` command config
@cli.group("config", help="configuration")
def config():
    pass


# the `config` create subcommand
@click.command("create", help="Create new configuration file")
def create():
    msg = "Select folder to containing the sound files"
    click.echo(msg)
    # root = tk.Tk()
    # root.focus_force()
    # Cause the root window to disappear milliseconds after calling the filedialog.
    # root.after(100, root.withdraw)
    # tk.Tk().withdraw()
    # hangs: mb.showinfo("msg","Select folder containing the sound files")
    msgbox.alert(msg, "info")
    # "title" only supported on linux ith wv ...
    folder = askdirectory(
        title="Select folder to monitor containing the sound files",
        mustexist=True,
        initialdir="~",
    )
    choices = ["tiny", "base", "small", "medium", "large", "turbo"]
    # inx = ask_choice("Choose a model", choices)
    # model = choices[inx]
    model = Prompt.ask(
        "Choose a model",
        console=console,
        choices=choices,
        show_default=True,
        default="large",
    )
    config_name = Prompt.ask(
        "Enter a name for the configuration file",
        show_default=True,
        default="localwhisper.toml",
    )
    config_path = Path(config_name)
    toml_path = config_path.with_suffix(".toml")
    while toml_path.exists():  # current dir
        result = get_config_from_toml(toml_path)
        click.secho("Already exists...", fg="red")
        show_config(result)
        overwrite = Prompt.ask(
            "Overwrite?", choices=["y", "n"], default="n", show_default=True
        )
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

import toml
from result import is_ok, is_err, Ok, Err, Result
from attrs import define
from rich.console import Console

console = Console(width=120, force_terminal=True)


@define
class Config:
    folder: str
    model: str


def save_config_to_toml(filepath,
                        folder_name="",
                        model_name=""):
    try:
        data = {"folder": folder_name, "model": model_name}
        with open(filepath, 'w') as toml_file:
            # noinspection PyTypeChecker
            toml.dump(data, toml_file)
    except Exception as e:
        print(f"Error saving config to TOML file: {e}")


def get_config_from_toml(filepath) -> Result:
    try:
        with open(filepath, 'r') as toml_file:
            data = toml.load(toml_file)
    except FileNotFoundError:
        Err("TOML file not found.")
    except toml.TomlDecodeError:
        Err("Error decoding TOML file.")
    except Exception as e:
        Err(f"Unexpected error: {e}")
    else:
        config = Config(**data)  # as data is flat, it's ok
        return Ok(config)


def ask_choice(msg: str, choices) -> int:

    # Print het keuzemenu
    console.print(
            f"[bold magenta]{msg}[/bold magenta]\n"
            "[yellow]Kies een van de volgende opties:[/yellow]"
    )
    for i, choice in enumerate(choices, start=1):
        console.print(f"{i}. {choice}")

    # Vraag input van de gebruiker
    user_input = Prompt.ask(
        "Voer het nummer van je keuze in",
        choices=[str(i) for i in range(1, len(choices) + 1)]
    )

    # Verwerk de keuze
    chosen_option = choices[int(user_input) - 1]  # Converteer input naar index
    console.print(f"[green]Je hebt gekozen voor:[/green] {chosen_option}")

    return chosen_option


def show_config(result: Result):
    if is_err(result):
        print(f"Exiting due to {result.err}")
        return False
    config = result.ok_value
    if config:
        print(f"Config folder path: {config.folder}")
        print(f"Config model name: {config.model}")
    return True

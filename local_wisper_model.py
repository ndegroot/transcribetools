import toml
from result import is_ok, is_err, Ok, Err, Result
from attrs import define

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

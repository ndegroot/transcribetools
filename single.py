from transcribetools import cli


def main():
    cli(["-d", "transcribe", "-f", "data/minimal.m4a"])


if __name__ == "__main__":

    main()

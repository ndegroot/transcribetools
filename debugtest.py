import click

@click.command()
@click.option('--my_arg', default=1, help='a number')
def my_command(my_arg):
    click.echo("my_arg='%d'" % my_arg)


if __name__ == '__main__':
    my_command(['--my_arg', '3'])

import click

from project_builder import ProjectBuilder


@click.command()
@click.argument("project_name")
@click.option("--dyna", is_flag=True, help="Install Dynaconf.")
@click.option(
    "--poetry", is_flag=True, help="Install virtual environment with Poetry."
)
@click.option(
    "--pip", is_flag=True, help="Install virtual environment with Pip."
)
@click.option("--ptbr", is_flag=True, help="Set project language to pt-br.")
def main(project_name, dyna, poetry, pip, ptbr):
    click.echo("\n### Django Poject Builder ###\n")
    rendered_name = click.style(f"{project_name}", fg="blue", bold=True)
    click.echo(f"- Project name: {rendered_name}")

    project = ProjectBuilder(project_name, dyna, poetry, pip, ptbr)

    click.echo("- Creating the directories ...")
    project.create_directories()

    click.echo("- Writing the files ...")
    project.create_files()

    click.echo("\nAll done!")


main()

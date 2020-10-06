import click


from data_ingest.external_services.newspaper import load_news
from data_ingest.regs.va import load_va_regulations


@click.group()
def main():
    pass


@click.command("run-ingest")
def run_ingest():
    print("Loading news ...")
    load_news()
    print("Loading VA regs ...")
    load_va_regulations()


main.add_command(run_ingest)


if __name__ == "__main__":
    main()

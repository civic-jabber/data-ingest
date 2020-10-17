import click
import pandas as pd


from data_ingest.external_services.newspaper import load_news
from data_ingest.external_services.open_states import get_all_people
from data_ingest.regs.va import load_va_regulations


@click.group()
def main():
    pass


@click.command("run-ingest")
def run_ingest():
    """Runs all of the ingest commands that are current implemented. Currently, this
    includes:

    1. News
    2. Regulations for VA
    """
    print("Loading news ...")
    load_news()
    print("Loading VA regs ...")
    load_va_regulations()


main.add_command(run_ingest)


@click.command("people-to-csv")
@click.option("--state")
@click.option("--outfile")
def people_to_csv(state, outfile):
    """Finds a list of legislators for a state and saves the results as a CSV file."""
    people = get_all_people(state, per_page=25, links=True)

    data = {"name": [], "party": [], "role": [], "district": [], "link": []}
    for person in people:
        data["name"].append(person["name"])
        data["party"].append(person["party"])
        data["role"].append(person["current_role"]["title"])
        data["district"].append(person["current_role"]["district"])

        if person["links"]:
            data["link"].append(person["links"][0]["url"])
        else:
            data["link"].append(None)

    people_data = pd.DataFrame(data)
    people_data.to_csv(outfile, index=False)


main.add_command(people_to_csv)


if __name__ == "__main__":
    main()
from collections import Counter
import datetime
from tabulate import tabulate
import os
import sys
import pickle
import urllib.parse

import requests


# Repositories being monitored.
REPOS = [
    "enthought/traits",
    "enthought/traitsui",
    "enthought/pyface",
    "enthought/enable",
    "enthought/chaco",
    "enthought/envisage",
    "enthought/mayavi",
]

# Only analyze runs that are not older than this long
AS_RECENT_AS = datetime.timedelta(days=7)
INCLUDE_RUNS_SINCE = datetime.datetime.now() - AS_RECENT_AS

# Only runs triggered by this event type will be reported
EVENT = "schedule"


def parse_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


def cached(func):
    """ Decorator to cache results so we are not hitting the web API all
    the time when we experiment with the code. This is purely a development
    tool.
    """

    def decorated(repo, event):

        pickled_file = (
            urllib.parse.quote_plus(f"{repo}_{event}") + ".pickle"
        )
        if os.path.exists(pickled_file):
            with open(pickled_file, "rb") as fp:
                data = pickle.load(fp)
        else:
            data = func(repo, event)
            with open(pickled_file, "wb") as fp:
                pickle.dump(data, fp)
        return data

    return decorated


# Uncomment decorator to cache responses
# @cached
def get_response(repo, event):
    """ Return the JSON data for the GitHub organization/repo runs triggered
    by the given event. The most recent and at most 100 runs will be returned.

    Parameters
    ----------
    repo: str
        Name for a GitHub repository, including organization
        e.g. 'python/cpython'
    event: str
        Name of the event to monitor, e.g. 'schedule'
        See GitHub Actions Web API references.

    Returns
    -------
    response : dict
        JSON response

    Raises
    ------
    urllib2.HTMLError
        If the response indicates errors.
    """
    response = requests.get(
        f"https://api.github.com/repos/{repo}/actions/runs?event={event}",
    )
    if response.ok:
        return response.json()
    response.raise_for_status()


def get_latest_runs(data, since):
    """ Given the full response, filter runs such that only the latest runs
    for each workflow id are returned.

    Parameters
    ----------
    data : dict
        JSON response, e.g. output of get_response
    since : datetime
        Only runs created since this datetime are returned.

    Returns
    -------
    last_runs : list
        List of run records where each one corresponds to the latest run for
        a given workflow.
    """
    id_to_latest = {}
    id_to_last_run = {}
    for run in data["workflow_runs"]:
        workflow_id = run["workflow_id"]
        created_time = parse_timestamp(run["created_at"])
        if created_time <= since:
            continue
        latest = id_to_latest.setdefault(
            workflow_id, datetime.datetime(1, 1, 1)
        )
        if created_time > latest:
            id_to_latest[workflow_id] = created_time
            id_to_last_run[workflow_id] = run
    return list(id_to_last_run.values())


def record_summary(record):
    """ For a given job run record, return the formatted entries to be
    reported in (rich) text format.

    Parameters
    ----------
    record : dict
        A single run record

    Returns
    -------
    summary : dict
        Filtered and formatted data.
    """
    name = record["name"]
    conclusion = record["conclusion"]
    updated_at_timestamp = record["updated_at"]
    marker = "✅" if conclusion == "success" else "❌"
    time_delta = (
        datetime.datetime.now() - parse_timestamp(updated_at_timestamp)
    )
    ndays_since = time_delta.days + time_delta.seconds / 86400.0
    return {
        "Name": name,
        "Conclusion": f"{marker} {conclusion}",
        "Updated": updated_at_timestamp + f"  ({ndays_since:.0f} days ago)",
        "URL": f'[Details]({record["html_url"]})',
    }


def to_table(repo_records):
    """ For a list of job run records, collect the summary and create
    a table in text format.
    """
    table = []
    keys = []
    for record in repo_records:
        summary = record_summary(record)
        keys = list(summary.keys())
        table.append(list(summary.values()))
    return tabulate(table, headers=keys, tablefmt="github")


def get_repo_records():
    return {
        repo: get_latest_runs(get_response(repo, EVENT), INCLUDE_RUNS_SINCE)
        for repo in REPOS
    }


def get_short_summary(repo_to_records):
    """ Given a mapping from repositories to its list of job run records,
    return a short sentence as a summary.

    Parameters
    ----------
    repo_to_records : dict(str, list(dict))
        Keys are repo names. Values are list of run job records.

    Returns
    -------
    summary : str
    """
    # Get overall success/failure counts
    conclusion_counter = Counter()
    for records in repo_to_records.values():
        conclusion_counter.update(record["conclusion"] for record in records)
    sadness = sum(
        count for key, count in conclusion_counter.items() if key != "success"
    )
    return "There is some sadness." if sadness > 0 else "Happy Day!"


def create_report_tables(repo_to_records, file=sys.stdout):
    """ Given a mapping from repositories to its list of job run records,
    print the report table to a stream.

    Parameters
    ----------
    repo_to_records : dict(str, list(dict))
        Keys are repo names. Values are list of run job records.
    file : file-like
        Output stream to print reports to.
    """
    print("Generated on: ", datetime.date.today().isoformat(), file=file)
    print(file=file)

    print("Include runs triggered by: ", EVENT, file=file)
    print(file=file)

    print("Include runs in the last: ", str(AS_RECENT_AS), file=file)
    print(file=file)

    # Print each table
    for repo, records in repo_to_records.items():
        print(f"**{repo}**", file=file)
        print(to_table(records), file=file)
        print(file=file)


def main():
    repo_to_records = get_repo_records()

    with open("results.md", "w", encoding="utf-8") as fp:
        create_report_tables(repo_to_records, file=fp)

    print(get_short_summary(repo_to_records))


main()

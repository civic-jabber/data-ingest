## Contributing

### Introduction

Hello! Thank you for your interest in participating. The Civic Jabber project seeks to
make state and local public policy issues more accessible for everyday citizens. A key
area component of public policy that is not currently very transparent for most citizens
is the process for making rules. After a legislature passes a law, state exeutive
agencies publish rules which interpret and act upon those laws. When an agency publishes
a rule, it appears in a publication known as a state register. Rules have the force of
law. Today, state agencies produce many times more rules and regulations than
legislatures do laws. Therefore, public understanding of and participation in the rule
making process is vital. While publicly available, all 50 states publish their registers
in different locations and they are in different formats, making it difficult to
understand the regulator environment across all 50 states. The goal of this project is to
bring rules and regulations from across all 50 states into a single location and develop
a common schema that makes it possible to compare regulations between states.
Eventually, we would like to make all of this data searchable in a user interface.

### Project Board

You can find the unified Civic Jabber project board [here](https://github.com/orgs/civic-jabber/projects/1).
There are several columns on the board:

1. To Do - these issues have been triaged and are ready to pick up
2. In Progress - these are issues someone is currently working on. If you start working
   on an issue, please move it to In Progress and assign to yourself.
3. Under Review - these are issues that are awaiting PR review. A PR requires approval
   from a code owner before merging.
4. Staged - these issues are complete and merged, but have not been released yet. Once your work is
   merged into master, move the issue to Staged and close out the issue.
5. Done - these issues are complete and have been released.

Feel free to pick up any work that looks interesting you. You aren't limited to what's
in To Do, but issues in To Do help best support ongoing priorities. If there's nothing
left in To Do.


### Pull Requests

To contribute code, you will need to work on a feature branch and raise a pull request
(PR) into `master`. Best practice is to use `{name}/{description}` as the name of your
branch (i.e. `robinson/va-regulation ingest`. When you open a PR, be sure to link to the
associated issue from the board. All PRs should have a brief description of what the PR
is intended to do and instructions on how to test. Please include unit tests with any
PR. You can use [this PR](https://github.com/civic-jabber/data-ingest/issues/7) as an
example.


### Tests and Linting

Linting and tests run against all PRs to `master`. To run tests locally, you can run
`make test` from the root directory of the project. For the linter, run `make lint`. You
can also use `make tidy` to apply the `black` code formatter. That should get your code
fairly close to passing `make lint`. Note, both `pytest` and the linters are in the test
dependencies, so you'll need to install those before running the lint commands.

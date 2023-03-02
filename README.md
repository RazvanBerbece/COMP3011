# COMP3011
Monorepo which holds the code and documentation for CWs 1 and 2 of the COMP3011 module.

# Contribution Guidelines
Contributions will be made following this flow: branch out > pull request > merge

*The contribution workflow looks like this:*
1. Pull the `main` branch from upstream into the local machine `main` branch
2. Merge local `main` into local development branch
3. Make code or documentation changes on local development branch
4. Stage, commit with a useful message, push to remote development branch
5. Open up a Pull Request to `main` branch from remote development branch
6. Reviewers will check the PR and the changes in it
7. The PR is merged or squashed into `main` if the review passes

**Important:** All changes are made on local dev branches and never on the main branch. The main branch is only used to update local branches with the latest versions of code and documentation.

## Branch Naming
In order to keep everything consistent and intuitive, new branches should follow a simple standardised naming structure.

For instance, a developer might want to work on the Payment service and implement caching. The developer would then create a new branch with the name `payment/caching`.

In general, a branch name would follow this structure: `<service name>/<feature hint>` or `<service name>/<documentation change hint>`.

## Pull Requests
When opening a pull request, try and explain in a few words what the changes are (e.g.: added X feature, updated Y documentation with Z, etc.) in the PR description so that the reviewers can easily match the description to the file changes.

Additionally, please try and keep PRs relatively small. It's better to merge multiple smaller PRs than one big PR. This is because the bigger the PR, the greater the chance of breaking changes, and also that reviewers will have a hard time to review all the changes and put them into context to give the green light for merging into the main branch.

# Contribution
## Branching Policy
We are using a shrunk form of the common [Git Flow](https://www.git-tower.com/learn/git/ebook/en/desktop-gui/advanced-topics/git-flow).

The central repo holds two main branches with an infinite lifetime: **master** and **dev**.

* The **master** branch is the branch where the source code always reflects a production-ready state.
* The **dev**elop branch is the branch where the source code always reflects a state with the latest delivered development changes for the next release.
Feature branches are used to develop new features for the upcoming release. They are derived from the issue board. Every feature-branch is always created from the dev branch and will solely be remerged into dev.

A feature-branch's lifetime should be as short as possible.

**Please be very carefull with commits into the master** - always prefer a pull request and affirmation from your teammembers.

## Further information
* Create code,commits and assets in English (only).
* Note the number of your issue in your commit-messages to take full advtantage of the issueboard.
* Assign yourself to an issue in the issue board.
* If you are stuck at an issue, consider adding the Label Help Wanted.
* Consider pushing your feature branches remote, so others can help or pick up your work. Tidy up when the issue is closed.
* Close the issue only if your changes are visible to others (a remote branch is fine). 

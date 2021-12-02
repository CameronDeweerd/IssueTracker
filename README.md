# IssueTracker

This is an issue tracker created to allow a team of people to submit, track, and manage bugs.

## Description

This issue tracker was designed with the following process flow in mind:

1. A Submitter finds a bug and submits a new ticket
2. A Project Manager reviews that ticket and assigns it to a Developer
3. The Developer works on repairing the bug, adding comments to the ticket as they go
4. The Developer closes out the completed ticket

It also includes these additional feature:

- A dashboard that shows important tracking information such as "Open Tickets by Category"
- A user profile section
- A role assignment section only accessible by Admin users
- A history section where all tickets can be viewed

The login screen currently allows anyone to login as a demo user under any of these roles. This is to allow easy viewing
of the features but would be removed if this project were to be used in a formal capacity.

## Future items to implement

The next feature to be implemented in the future would be a projects section. This section would allow the Project
Manager to assign tickets to a given project rather than a specific Developer. Developers would then be assigned to
projects and could see all the tickets that belong to that project; open or closed

## Design Choices

This was created as a two person project between [TSennema](https://github.com/Tsennema)
and [CameronDeweerd](https://github.com/CameronDeweerd). We decided to do this project collaboratively as a way for us
to improve our knowledge of Git, reading and working with team member's code, and to practice delegating and scheduling
tasks.

The Issue Tracker was created using a Python (Flask) backend with an HTML, CSS, JS frontend and an SQLite database.
These were chosen as they were the languages we both confidently knew. This allowed us to collaborate better and ensured
we could easily discuss any changes we made and that either one of us could handle each element of the project.

# Project 12 - Django Social Team Builder

It's time to build a single, large project that pull everything together!

You've decided to start a small side project to scratch your own itch. Sometimes it's really hard to find people to help you with projects or projects that could benefit from your particular set of skills. No, not tracking down smugglers, but coding, designing, writing, and other programming-related talents.

You're going to build a site where people can sign up to find projects that need help or post their own projects for other people to join. Users should be able to create a brief profile for themselves after they sign up with an avatar, a bio, and pick their skills from a list. Users can post a project, too, giving it a title and description. They should also list the positions they need filled for that job with a brief description of what the position will be responsible for. Users should be able to find a project and ask to join it. If you're a project owner, you can approve or deny the person asking to join. Finally, make sure you have login and logout links, too.


## Project Instructions 

[ ] **Use the supplied files as static assets and example templates for your web site.**
***

[ ] **As a user of the site, I should be able to sign up for an account.**
***

[ ] **As a user of the site, I should be able to log into my account.**
***

[ ] **As a user of the site, I should be able to edit my profile.**
***

[ ] **As a user of the site, I should be able to upload an avatar image for my profile.**
***

[ ] **As a user of the site, I should be able to pick my skills for my profile.**
***

[ ] **As a user of the site, I should be able to create a project that I need help on.**
***
[ ] **As a user of the site, I should be able to specify the positions my project needs help in with a name, a description, and related skill.**
***
[ ] **As a user of the site, I should be able to see all of the applicants for my project's positions.**
***

[ ] **As a user of the site, I should be able to approve an applicant for a position in my project.**
***

[ ] **As a user of the site, I should be able to reject an applicant for a position in my project.**
***

[ ] **As a user of the site, I should get a notification if I've been rejected or approved for a position.**
***

[ ] **As a user of the site, I should be able to search for projects based on words in their titles or descriptions.**
***
[ ] **As a user of the site, I should be able to filter projects by the positions they need filled.**
***
[ ] **As a user of the site, I should be able to apply for a position in a project.**
***
[ ] **As a user of the site, I should be able to log out.**
***

## Project Structure
***

### Apps

1. **Profile app**
    - manages the user profiles, signup, login, logou etc..
    - profile includes: 
        - avatar, bio, skillsets from a pick list (table join, add new skills)

    ***Models***

    1. User Model
        - email
        - username
        - display_name (preffered name)
        - bio (short cv)
        - avatar (image)
        - date_joined 
        - projects (user can work on many projects)
        - past projects 
        - project ranking
        - skillsets (user can have many skills)
        - is_active
        - is_admin (staff, runs site)

2. **Projects app**
    - manages the projects, post new project, title and decsription
    - positions required to fill the project (skills?), with a brief decsription of what is required, what the position is responsible for
    - people can ask to signup to a project
    - owners can either approve or deny signup

    ***Models***

    - Project Model
        - project name
        - project description
        - required skills - can be multiple
        - estimated duration
        - project responsibilites per skillset?
        - who is working on project - multiple 
        approved users 
        - created_by (project owner)
        - project positon
        - project responsibilities

3. **Project Updates**
    - post updates against a project
    - should be able to handle code snippets
    - gets responses to updates

    **Models**

    - Post Updates Model
    


## Project capabilities
***

1. Ability to sign up for project via an email
2. Ability to rank a user on a project
3. Ability to view all current and past projects by type (front-end, back-end), skill set, user, 
4. Ability to search all projects by user, skillset, type, position
5.  As a user of the site, I should get an email verification after sign up.
6. As a user of the site, a position should be marked as filled once I accept someone for it.
7. As a user of the site, I should filled positions should be hidden or marked as filled so I don't apply for them.
8. As a user of the site, I should be able to use Markdown in the "about me" part of my profile.
9. As a user of the site, I should be able to list any skill on my profile, not just pre-selected ones.
10. As a user of the site, my profile should list projects I've been involved with.
11. As a user of the site, I should be able to use Markdown in my project description.
12. As a user of the site, I should be able to use Markdown in the position descriptions.
13. As a user of the site, I should be able to provide a listed length of involvement for a position (e.g. Designer: 10 hours/week).
14. As a user of the site, I should be able to filter applicants by their status (approved, denied, undecided).
15. As a user of the site, I should be able to approve or deny applicants directly from the list of applicants.
16. As a user of the site, I should be given a list of projects that need my skill set.

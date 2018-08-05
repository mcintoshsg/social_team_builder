# Project 12 - Django Social Team Builder

It's time to build a single, large project that pull everything together!

You've decided to start a small side project to scratch your own itch. Sometimes it's really hard to find people to help you with projects or projects that could benefit from your particular set of skills. No, not tracking down smugglers, but coding, designing, writing, and other programming-related talents.

You're going to build a site where people can sign up to find projects that need help or post their own projects for other people to join. Users should be able to create a brief profile for themselves after they sign up with an avatar, a bio, and pick their skills from a list. Users can post a project, too, giving it a title and description. They should also list the positions they need filled for that job with a brief description of what the position will be responsible for. Users should be able to find a project and ask to join it. If you're a project owner, you can approve or deny the person asking to join. Finally, make sure you have login and logout links, too.


## Project Instructions 

[X] **Use the supplied files as static assets and example templates for your web site.**
***

[X] **As a user of the site, I should be able to sign up for an account.**
***

[X] **As a user of the site, I should be able to log into my account.**
***

[X] **As a user of the site, I should be able to edit my profile.**
***

[X] **As a user of the site, I should be able to upload an avatar image for my profile.**
***

[X] **As a user of the site, I should be able to pick my skills for my profile.**
***

[X] **As a user of the site, I should be able to create a project that I need help on.**
***
[X] **As a user of the site, I should be able to specify the positions my project needs help in with a name, a description, and related skill.**
***
[X] **As a user of the site, I should be able to see all of the applicants for my project's positions.**
***

[X] **As a user of the site, I should be able to approve an applicant for a position in my project.**
***

[X] **As a user of the site, I should be able to reject an applicant for a position in my project.**
***

[X] **As a user of the site, I should get a notification if I've been rejected or approved for a position.**
***

[X] **As a user of the site, I should be able to search for projects based on words in their titles or descriptions.**
***
[X] **As a user of the site, I should be able to filter projects by the positions they need filled.**
***
[X] **As a user of the site, I should be able to apply for a position in a project.**
***
[X] **As a user of the site, I should be able to log out.**
***
[] **Add in error pages - 404 etc**

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

    - Poistion Model

    - Application Model

    - Skill Model

    - UserSkill Model


3. **Project Updates**
    - post updates against a project
    - should be able to handle code snippets
    - gets responses to updates

*** Fixes
***
[] **Fix all_ projects pagination**
***
[] **Fix delete project modal**
***
[X] **Fix save empty image**
***
[] **Fix load image button**
***
[] **Fix add / remove skills**
***
[] **Fix DRY - add a mixin for context_data**
***
[] **Use get_absolute_url**
***
[X] **Fix what actions an non-logged in user can do**
***
[X] **Remove delete and edit buttons if projects owner is not logged in user**
***
[X] **Fix search with no input**
***
[X] **De-duplicate Project Needs on applicactions page**
***
[X] **Fix accept / reject on project detail page**
***
[X] **Fix project needs | issue on index page**
***
[] **Fix showing completed projects on all project view**
***
[] **Implement logging for serious errors**
***
[] **Implement differentiated settings.py**
***
[] **Remove the ability to add the same position**
***
[] **Fix messages placement**
***
[X] **Add in project completed Project**
***
[] **Change worked_on_projects to completed_projects**
***
[] **Speed up project**
***
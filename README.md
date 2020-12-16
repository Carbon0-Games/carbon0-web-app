![Brand image](https://i.postimg.cc/pTycYvPJ/Screen-Shot-2020-10-16-at-10-37-00-AM.png)

# Carbon0 Games
 [![Build Status](https://img.shields.io/travis/Carbon0-Games/carbon0-web-app.svg?style=flat)](https://travis-ci.com/github/Carbon0-Games/carbon0-web-app/) ![Website Status](https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Fcarbon0.herokuapp.com) ![Django Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/zainrazatheupstart/carbon0-web-app_django_1?label=Django%20Build%20Size) ![React Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/zainrazatheupstart/carbon0-web-app_react_1?label=React%20Build%20Size) ![PostgreSQL Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/zainrazatheupstart/carbon0-web-app_postgresdb?label=PostgreSQL%20Build%20Size) ![NGINX Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/zainrazatheupstart/carbon0-web-app_nginx_1?label=NGINX%20%20Build%20Size)

Carbon0 Games helps people create carbon negative lifestyles for themselves and their communities, through our web application.

This repository contains the source code for Carbon0, a gamified solution to save the planet!

<br />

## Table of Contents

- [About This Project](#about-this-project)
- [Tech Stack](#tech-stack) 
- [How to Run Locally](#how-to-run-locally)
- [Creating a Pull Request](#creating-a-pull-request)
- [Contributing to Carbon0](#contributing-to-carbon0) 
- [Release Schedule](#release-schedule)
- [Adding Environment Variables](#adding-environment-variables)
- [License](#license)
<br /><br /> 

## About this Project

800 million people played Pokemon Go. What if they were playing a different game, a game to reduce their carbon footprint?

This game is called *[Carbon0](https://playcarbon0.com)*! Here's a [short product demo](https://youtu.be/UoZv2MljbE4) for more info.

Carbon0 shows players their impacts using a gamified carbon calculator, and rewards those who take steps to reduce their footprint by awarding them "Zeron" characters.
It creates connections, communities and economically empowers environmentally-friendly businesses and charities.
All while having fun!
 
<br />

## Tech Stack
- [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/) - for programming the backend web server using Python 3
- [Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/) - for building a mobile-friendly UI for web browsers
- [PostgreSQL](https://www.postgresql.org/) - for installing PostgreSQL on your local machine. Please use [Postgres.app](https://postgresapp.com/) for macOS, or check here for [Windows installers](https://www.postgresql.org/download/windows/) of PostgreSQL.
- [Git](https://git-scm.com/doc) and [GitHub](https://www.github.com) - for Version Control and Team Collaboration
- [WebXR](https://developers.google.com/web/updates/2018/05/welcome-to-immersive) - for displaying AR characters in the browser, with no external hardware required
- [Chart.js](https://www.chartjs.org/) - for making visualizations the carbon footprints of the players

<br /><br />

## How to Run Locally
Please follow these steps to be able to run the project:

### Option 1: Using Docker and Docker-Compose

#### Prerequisite:

Make sure you have the latest version of [Docker](https://www.docker.com/get-started) installed. If you are not on macOS or experience any trouble installing Docker Compose, check out the [Docker documentation](https://docs.docker.com/compose/install/).

#### Instructions

1. Once you have done so and have also cloned the repository locally, you can run the project using `docker-compose` in the root directory:

        docker-compose up

2. Then you can view the project at [http://localhost:8000](http://localhost:8000).

3. If you ever want to run the automated Django tests from within the Docker container, first go to the `carbon0/entrypoint.sh` file, and uncomment the tests command on line 27:
```
        # python manage.py test  # remove the first "#" to uncomment this line
```
Then you may run the Docker containers again, using the command below to clear out the old versions of the containers on your machine:

```
        docker-compose down
```

With that, feel free to run the command in Step 1 once more!

4. At any time you can also open up Docker Desktop, and view the health of the `carbon0-web-app` container on a panel that will look something like below:

![Screenshot from Docker Desktop](https://i.postimg.cc/wvGHhhD8/Screen-Shot-2020-11-20-at-10-27-24-AM.png)

### Option 2: Using `virtualenv`: 
#### __Initial Setup__

1. In the folder of your choice, type `git clone https://github.com/Carbon0-Games/carbon0-web-app.git` into the command line.
2. Setup the folder as you wish while following these instructions
    - Create a new db called “carbon0” using this SQL command in your Terminal (and you can [install Postgres.app here](https://postgresapp.com/) if you don’t have it yet): `CREATE DATABASE carbon0;`
    - Start a new virtual env, and install Django - this [tutorial](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) is a good way to start if you need help to install and setup a virtual env
    - From this point on, stay in the virtual env
    - Within the outer `carbon0/` directory, enter the following to install all the dependencies through your command line: `python -m pip install -r requirements.txt` 
    - Also run the command `npm install` in this directory, to install all the dependencies for Node.js.
    - Do any db migrations that might be needed, using `python manage.py migrate`
    - Also migrate the initial data for the database, using the `loaddata` command:
        ```
        python manage.py loaddata carbon_quiz/fixtures/mission_link_data.json carbon_quiz/fixtures/question_data.json
        ```

### __Running Locally__

1. Make sure all settings are installed and migrations completed, especially after pulling the latest version from master
2. Navigate to the application folder `carbon0/`, and run this command to set your `DJANGO_SETTINGS_MODULE` environment variable. This will tell Django to use the local settings while you work on the project. It only needs to be done once, on the first time before you run the project locally:

        $ export DJANGO_SETTINGS_MODULE=carbon0.settings.local

3. Now, you can use the command to run the project locally:

        $ python3 manage.py runserver
        

4. Something similar to the following will be returned in the command prompt:

        Performing system checks...

        System check identified no issues (0 silenced).

        September 15, 2020 - 15:50:53
        Django version 3.1, using settings 'carbon0.settings.local'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        

5. You can then enter the url into your browser to navigate to the launched project.


### __Creating a Pull Request__
When you would like to contribute to the codebase, the following steps are key to keeping the code clean and functional.
*Recommended*: when doing development work, use `virtualenv`, `Pipenv`, or some other tool for Python virtual environments as you run the code locally. Docker is great because it's easy to get up and running, but you may find it harder to do some things such as keeping track of the version numbers for new Python packages you install. 

1. *Non-collaborators*: please first make a Fork of this repository, by clicking on the top left button on this page that says "Fork":
![Image of Fork button](https://i.postimg.cc/XJkWQtG1/Screen-Shot-2020-10-16-at-5-25-30-PM.png)
2. Once you have pull the code onto your local machine, use the command `git checkout -b name_of_your_branch` (this both creates your branch and 'moves'; you to that branch to work on. Make sure that when coding that you are working on your branch. You can see which branch your on in the terminal, depending on your terminal setup with oh-my-zsh. You can also see it in the lower left corner in VSCode and lower right Atom)
    - To travel between branches simply use `git checkout branch_name`
3. code as usual
4. When your commits are made, use `git push origin name_of_your_branch` to make sure to push to your branch.
5. Occasionally check on other peoples branch as well in github by clicking the branch:master button under the commit count in the repo and you can switch branches and see others branches 
On GitHub, navigate to the main page of the repository.
6. In the "Branch" menu, choose the branch that contains your commits.
7. Above the list of files, click  __Pull request__.
8. Use the base branch dropdown menu to select the branch you'd like to merge your changes into, then use the compare branch drop-down menu to choose the topic branch you made your changes in.
9. Type a title and description for your pull request.
10. To create a pull request that is ready for review, click **Create Pull Request.**
![Pull Request button](https://docs.github.com/assets/images/help/pull_requests/pull-request-start-review-button.png)

*From [Creating a Pull Request via Github](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)

## Contributing to Carbon0
We look forward to seeing your work! Once your PR has been merged, we invite you to add yourself to the [CONTRIBUTORS](CONTRIBUTORS.md) file.

On this file, we would love for you to list your name, and perhaps share some details with the community such as:
```
- Name: who you are
- About Me: where you're from, what your goals are, how you found out about Carbon0, etc.
- Technologies you work with
- and a Fun Fact doesn't hurt!
```

## Release Schedule
This can be found on [Releases.md](Releases.md).

## License
We are currently using the MIT License. More details on [LICENSE](LICENSE).

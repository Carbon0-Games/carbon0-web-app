# Carbon0 Games
The code for Carbon0, the game to save the planet!

##### Tech Stack
- Django
- Python

### Contributing
This is a step by step instruction created by our team member __, to allow other to be able to contribute to the project:

1. In the folder of your choice, type `git clone https://github.com/UPstartDeveloper/carbon0-web-app.git` into the terminal
2. setup folder as you wish locally (use Zains instructions)
    - Edit
    - Edit
3. `git checkout -b name_of_your_branch` (this both creates your branch and 'moves'; you to that branch to work on. Make sure that when coding that you are working on your branch. You can see which branch your on in the terminal, depending on your terminal setup with oh-my-zsh. You can also see it in the lower left corner in VSCode and lower right Atom)
4. code as usual
5. `git push origin name_of_your_branch` (please do not git push origin MASTER) make sure to push to your branch.
6. Occasionally check on other peoples branch as well in github by clicking the branch:master button under the commit count in the repo and you can switch branches and see others branches

### Running Locally

1. Make sure all settings are installed and migrations completed, especially after pulling the latest version from master
2. Once you've navigated to the application folder, run the command:

        $ python3 manage.py runserver
        

3. The following will be returned in the command prompt:

        Performing system checks...

        System check identified no issues (0 silenced).

        You have unapplied migrations; your app may not work properly until they are applied.
        Run 'python manage.py migrate' to apply them.

        September 15, 2020 - 15:50:53
        Django version 3.1, using settings 'mysite.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        

4. You can then enter the url into your browser to navigate to the launched project.
5. (Extra - for faster access) Using `cntrl+click` on  `http://127.0.0.1:8000/` which will open up a menu, from there select the option to navigate to the url.


### Create Superuser
#### Creating superuser for localhost:

1. Open your terminal and change directory to your project
2. Start the program as you would in the above instructions for running the program locally
3. Once running, use the command `python3 manage.py createsuperuser`
4. From here, you will be prompted for **username**, **email**, **password** (which will need to be entered twice)
5. Once this has been finished, feel free to launch the application, and enter this `http://127.0.0.1:8000/admin/` url.

#### Creating superuser for hosted site:

1. Head to the [site]()
2. (Work in Progress) Contact Zain for more details and permissions

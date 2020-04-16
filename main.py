# Import Pyton Libraries ---------------------------------------------------
import os
import subprocess

# Logging ------------------------------------------------------------------
q0 = input('''
You have executed a function that will check the status of every git repository in this directory.
Do you want to proceed?  ''')

# If the user wants to proceed:
if q0 == ('Yes', 'yes'):

    # Define Directories -------------------------------------------------------
    cwd = os.getcwd()


    # Step 1:  Get List of All Git Repositories In CWD Tree ____________________

    # List Obj For Paths2 Git Repositories
    git_repos = []

    def GetAllGitReposCwd(cwd_=None):
        ' Note:  Must pass None to function'
        # If iter == 1
        if cwd_ is None:
            # Return cwd
            GetAllGitReposCwd(os.getcwd())
        # If iter > 1
        else:
            # Expand CWD
            candidates = os.listdir(cwd)

            # Check to see if cwd is a repo
            if '.git' in candidates:
                git_repos.append(cwd)

            # If not a git repository, check subdirectories
            else:
                # For each possible directory
                for c in candidates:
                    # create the full path as cwd + possible dir
                    fullpath = cwd + '/' + c
                    # Check if fullpath is a directory
                    if os.path.isdir(fullpath) is True:
                        # Return as cwd and recursively check if git repo
                        GetAllGitReposCwd(fullpath)

    # Call Function & Build List of Paths 2 Git Repos
    GetAllGitReposCwd()


    # Logging
    print('\n The following git repositories have been found => {}'.format(git_repos))



    # Step 2:  Check Status of All Git Repos _________________________________

    # Check if list is empty
    if not git_repos:
        print('No git repositories found in cwd directory tree.  Ending process')

    # Otherwise, proceed
    else:
        # Iterate List of Repository Paths
        for repo in git_repos:
            # Change CWD to Repo Path
            os.chdir(repo)
            print('\n***************************************************')

            # Obj to catch git status msg
            git_status_msg = ''
            msg = "branch is up to date"

            # Redirect Stdout
            cmd = ['git', 'status']
            git_output = subprocess.check_output(cmd)

            # Check if Repository Is Not up-to-date
            if msg not in str(git_output.decode('utf-8')):

                # Logging
                print('Repository => {} is not up to date.  Returning git status'.format(repo))
                print('\n', git_status_msg)


                # Ask user If he/she wants to stage changes
                print('\n')
                q1 = input('Do you want to stage changes? ')
                if q1 in ('Yes','yes'):
                    os.system('git add .gitignore')
                    os.system('git add *')

                    # Ask user if he/she wants to add a commit message
                    q2 = input('Do you want to add a commit message? ')
                    if q2 in ('Yes', 'yes'):
                        a1 = input('Input message here =>  ')
                        os.system('commit -m {}'.format(a1))
                    else:
                        os.system('commit -m -q')

                    # Execute Git Push Command
                    os.system('git push')

                    # Execute Clear Terminal Command
                    os.system('clear')

                # Because the user did not want to commit changes, clear terminal
                else:
                    # Clear Terminal
                    os.system('clear')

            # If msg was not found in the git status report, then repo is up to date.
            else:
                print('Repository is up to date.  Moving on to next repo')




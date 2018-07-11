# jsa-brandeis
Website for Brandeis JSA

## Note to self
* Push to branch, merge, change to master and pull, push to heroku <br />
* If there's a problem, force push: `git push -f heroku master`<br />
* Pull from master before you start working!

## Instructions
1. Clone this repo
2. Create your own branch
3. Download [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
4. Connect to heroku using `heroku git:remote -a jsa-brandeis` or `git remote add heroku git@heroku.com:project.git` (Ask for username and password)
5. Run locally with `python3 jsabrandeis.py` (Ask for credentials if you need to test the forms or check heroku and create your own .env file) Also install packages with `pip install` if you need to.
6. After running your code and checking that it works locally, deploy to [git](https://git-scm.com/docs)
7. If there are no conflicts, you can just merge to master by yourself
8. Deploy to heroku with `git push heroku master`
9. Pull from master before you start working everytime!!

## TODO
* Login system
* DB
* Update information
* Buy domain

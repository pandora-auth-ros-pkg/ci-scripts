import requests
from string import Template

commit_url = Template('https://api.github.com/repos/$owner/$repo/commits/$sha')

def get_commit_author(repo_owner, repo_name, commit_sha):

  url = commit_url.substitute(owner=repo_owner, repo=repo_name, sha=commit_sha)

  req = requests.get(url)

  if req.ok:
    
    payload = req.json()
    name = payload['commit']['author']['name']
    email = payload['commit']['author']['email']

    return '%s <%s>' % (name, email)

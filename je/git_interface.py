import os
import git


class GitIntrerface(object):

    def __init__(self, repos_root_dir):
        self.repos_root_dir = repos_root_dir

    def get_repo(self, repo):
        """
        Returns the repo dir if exists, None o/w.
        :param repo: the repo to check
        :return:
        """
        if os.path.isabs(repo):
            repo_to_check = repo
        else:
            repo_to_check = os.path.join(self.repos_root_dir, repo)

        return git.Repo(repo_to_check)

    def get_log(self, repo, including_method, from_date):
        repo = self.get_repo(repo)
        return repo.git.log(S=including_method, since=from_date,
                            no_merges=True)

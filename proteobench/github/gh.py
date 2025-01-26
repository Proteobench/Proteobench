import os
from typing import Optional

import pandas as pd
from git import Repo, exc
from github import Github


class GithubProteobotRepo:
    """
    A class to interact with GitHub repositories related to Proteobot and Proteobench,
    allowing cloning, committing, and creating pull requests.

    Attributes:
        token (str | None): GitHub access token (for authenticated access).
        clone_dir (str): Directory where the repository will be cloned.
        clone_dir_pr (str): Directory for cloning pull request repositories.
        proteobench_repo_name (str): Name of the Proteobench repository.
        proteobot_repo_name (str): Name of the Proteobot repository.
        username (str): GitHub username for authentication.
        repo (Repo | None): The local repository object after cloning.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        clone_dir: str = None,
        clone_dir_pr: str = None,
        proteobench_repo_name: str = "Proteobench/Results_quant_ion_DDA",
        proteobot_repo_name: str = "Proteobot/Results_quant_ion_DDA",
        username: str = "Proteobot",
    ):
        """
        Initializes the GithubProteobotRepo class with required parameters for cloning and managing repositories.

        Args:
            token (str | None, optional): GitHub access token for authenticated access. Defaults to None.
            clone_dir (str): Directory where the repository will be cloned.
            clone_dir_pr (str): Directory for cloning pull request repositories.
            proteobench_repo_name (str, optional): Name of the Proteobench repository. Defaults to "Proteobench/Results_quant_ion_DDA".
            proteobot_repo_name (str, optional): Name of the Proteobot repository. Defaults to "Proteobot/Results_quant_ion_DDA".
            username (str, optional): GitHub username for authentication. Defaults to "Proteobot".
        """
        self.token = token
        self.clone_dir = clone_dir
        self.clone_dir_pr = clone_dir_pr
        self.proteobot_repo_name = proteobot_repo_name
        self.proteobench_repo_name = proteobench_repo_name
        self.username = username
        self.repo = None

    def get_remote_url_anon(self) -> str:
        """
        Returns the remote URL of the repository to be cloned anonymously (public access).

        Returns:
            str: The public GitHub URL of the Proteobench repository.
        """
        remote = f"https://github.com/{self.proteobench_repo_name}.git"
        return remote

    @staticmethod
    def clone(remote_url: str, clone_dir: str) -> Repo:
        """
        Clones the repository from the given remote URL to the specified directory.

        Args:
            remote_url (str): The URL of the remote GitHub repository.
            clone_dir (str): The directory where the repository will be cloned.

        Returns:
            Repo: The local repository object.

        Raises:
            exc.NoSuchPathError: If the specified directory does not exist.
            exc.InvalidGitRepositoryError: If the directory is not a valid Git repository.
        """
        try:
            repo = Repo(clone_dir)
        except (exc.NoSuchPathError, exc.InvalidGitRepositoryError):
            repo = Repo.clone_from(remote_url.rstrip("/"), clone_dir)
        return repo

    def clone_repo_anonymous(self) -> Repo:
        """
        Clones the Proteobench repository anonymously (without authentication).

        Returns:
            Repo: The local repository object.
        """
        remote_url = self.get_remote_url_anon()
        repo = self.clone(remote_url, self.clone_dir)
        return repo

    def read_results_json_repo_single_file(self) -> pd.DataFrame:
        """
        Reads the `results.json` file from the cloned Proteobench repository and returns the data as a DataFrame.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the results from `results.json`.
        """
        f_name = os.path.join(self.clone_dir, "results.json")

        if not os.path.exists(f_name):
            raise FileNotFoundError(f"File '{f_name}' does not exist.")

        all_datapoints = pd.read_json(f_name)
        return all_datapoints

        def read_results_json_repo(self) -> pd.DataFrame:
            """
            Reads all JSON result files from the cloned Proteobench repository.

            Returns:
                pd.DataFrame: A Pandas DataFrame containing aggregated results from multiple JSON files.
            """
            data = []
            if not os.path.exists(self.clone_dir):
                raise FileNotFoundError(f"Clone directory '{self.clone_dir}' does not exist.")

            for file in os.listdir(self.clone_dir):
                if file.endswith(".json") and file != "results.json":
                    file_path = os.path.join(self.clone_dir, file)
                    with open(file_path, "r") as f:
                        data.append(pd.read_json(f, typ="series"))
            if not data:
                raise ValueError("No valid JSON data found in the repository.")

            return pd.DataFrame(data)

    def clone_repo(self) -> Repo:
        """
        Clones the Proteobench repository using either an anonymous or authenticated GitHub access token.

        If `token` is provided, it will use authenticated access; otherwise, it will clone anonymously.

        Returns:
            Repo: The local repository object.
        """
        if self.token is None or self.token == "":
            self.repo = self.clone_repo_anonymous()
        else:
            remote = f"https://{self.username}:{self.token}@github.com/{self.proteobench_repo_name}.git"
            self.repo = self.clone(remote, self.clone_dir)
        return self.repo

    def clone_repo_pr(self) -> Repo:
        """
        Clones the Proteobot repository (for pull request management) using either an anonymous or authenticated GitHub access token.

        If `token` is provided, it will use authenticated access; otherwise, it will clone anonymously.

        Returns:
            Repo: The local repository object for the pull request.
        """
        if self.token is None or self.token == "":
            self.repo = self.clone_repo_anonymous()
        else:
            remote = f"https://{self.username}:{self.token}@github.com/{self.proteobot_repo_name}.git"
            self.repo = self.clone(remote, self.clone_dir_pr)
        return self.repo

    def create_branch(self, branch_name: str) -> Repo.head:
        """
        Creates a new branch and checks it out.

        Args:
            branch_name (str): The name of the new branch to be created.

        Returns:
            Repo.head: The newly created branch object.
        """
        # Fetch the latest changes from the remote
        origin = self.repo.remote(name="origin")
        origin.fetch()

        # Create and checkout the new branch
        current_branch = self.repo.create_head(branch_name)
        current_branch.checkout()
        return current_branch

    def commit(self, commit_name: str, commit_message: str) -> None:
        """
        Stages all changes, commits them with the given commit name and message, and pushes the changes to the remote repository.

        Args:
            commit_name (str): The name of the commit.
            commit_message (str): The commit message.
        """
        # Stage all changes, commit, and push to the new branch
        self.repo.git.add(A=True)
        self.repo.index.commit("\n".join([commit_name, commit_message]))
        self.repo.git.push("--set-upstream", "origin", self.repo.active_branch)

    def create_pull_request(self, commit_name: str, commit_message: str) -> int:
        """
        Creates a pull request on GitHub using the PyGithub API.

        Args:
            commit_name (str): The title of the pull request.
            commit_message (str): The body of the pull request.

        Returns:
            int: The pull request number assigned by GitHub.
        """
        g = Github(self.token)
        repo = g.get_repo(self.proteobot_repo_name)
        base = repo.get_branch("master")
        head = f"{self.username}:{self.repo.active_branch.name}"

        pr = repo.create_pull(
            title=commit_name,
            body=commit_message,
            base=base.name,
            head=head,
        )

        pr_number = pr.number
        return pr_number

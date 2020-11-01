import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reinit')))

import unittest
from unittest.mock import patch, Mock
import tempfile

from reinit import git_ops
import pygit2

class TestGitOps(unittest.TestCase):
    
    def setUp(self):
        self.__tempdir = tempfile.TemporaryDirectory()
        self.__local_git_repo = git_ops.GitOps(
            'testuser',
            'pass',
            self.__tempdir.name,
            'temprepo'
        )


    def tearDown(self):
        self.__tempdir.cleanup()


    def test_clone(self):
        with patch('git_ops.pygit2.clone_repository') as mocked_clone, patch('git_ops.pygit2.Repository.init_submodules') as mock_init_submodules, patch('git_ops.pygit2.Repository.update_submodules') as mock_update_submodules:
            mock_init_submodules = None
            mock_update_submodules = None
            mocked_clone.return_value = pygit2.Repository()
            self.assertIsInstance(self.__local_git_repo.clone('github_url'), pygit2.Repository)

            mocked_clone.side_effect = Exception()
            self.assertIsNone(self.__local_git_repo.clone('github_url'))

    
    def test_create_commit(self):
        pygit2.init_repository(os.path.join(self.__tempdir.name, 'temprepo'))
        
        commit = self.__local_git_repo.create_commit('refs/heads/new', 'Init Commit')
        self.assertIsInstance(commit, pygit2.Oid)

        with patch('git_ops.pygit2.Repository.create_commit') as mocked_clone:
            mocked_clone.side_effect = Exception()
            self.assertIs(self.__local_git_repo.create_commit('refs/heads/new', 'Init Commit'), False)

        
    def test_set_new_remote(self):
        pygit2.init_repository(os.path.join(self.__tempdir.name, 'temprepo'))
        
        self.assertTrue(self.__local_git_repo.set_new_remote('origin', 'some_url'))
        
        with patch('pygit2.remote.RemoteCollection.create') as mocked_clone:
            mocked_clone.side_effect = Exception()
            self.assertFalse(self.__local_git_repo.set_new_remote('origin', 'some_url'))


    def test_push_repo(self):
        pygit2.init_repository(os.path.join(self.__tempdir.name, 'temprepo'))
        
        with patch('pygit2.Remote.push') as mocked_clone:
            mocked_clone.side_effect = pygit2.GitError
            self.assertFalse(self.__local_git_repo.push_repo('refs/heads', 'origin'))


    def test_reset_git(self):
        pygit2.init_repository(os.path.join(self.__tempdir.name, 'temprepo'))

        self.assertTrue(self.__local_git_repo.reset_git())


class TestGitHubOps(unittest.TestCase):

    def setUp(self):
        self.__github_repo = git_ops.GithubOps('testuser', 'pass')


    def tearDown(self):
        pass


    def test_new_github_repo(self):
        with patch('git_ops.requests.post') as mocked_clone:
            mocked_clone.return_value.status_code = 201
            self.assertTrue(self.__github_repo.new_github_repo('test'))

            mocked_clone.return_value.status_code = 403
            self.assertFalse(self.__github_repo.new_github_repo('test'))

    
    def test_delete_github_repo(self):
        with patch('git_ops.requests.delete') as mocked_clone:
            mocked_clone.return_value.status_code = 204
            self.assertTrue(self.__github_repo.delete_github_repo('test'))

            mocked_clone.return_value.status_code = 403
            self.assertFalse(self.__github_repo.delete_github_repo('test'))
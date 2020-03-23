#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gitlab
from utils.get_config import get_conf

class GitLabAPI():

    def __init__(self):
        # self.gitlab_url = 'http://git.xs.jf'
        # self.gitlab_token = 'vV9F9eFJNcg9jPHkxs_B'
        self.gitlab_url = get_conf('gitlab','url')
        self.gitlab_token = get_conf('gitlab','token')
        self.gl = gitlab.Gitlab(self.gitlab_url,private_token=self.gitlab_token,api_version=3)
    def get_all_users(self):
        re = []
        users = self.gl.users.list(all=True)
        for user in users:
            re.append({'gitusername':user.username})
        return re
    def get_all_projects(self):
        re = []
        projects = self.gl.projects.list(all=True)
        for project in projects:
            re.append({'pid':project.id,'pname':project.path_with_namespace})
        return re
    def get_all_groups(self):
        re = []
        groups = self.gl.groups.list(all=True)
        for group in groups:
            re.append({'gid':group.id,'gname':group.name})
        return re
    def get_user_id(self, username):
        user = self.gl.users.get_by_username(username)
        return user.id
    def get_project_id(self, project):
        projectinfo = self.gl.projects.get(project)
        return projectinfo.id
    
    
    
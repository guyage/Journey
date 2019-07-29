#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gitlab
from api.get_config import get_conf

class GitLabAPI():

    def __init__(self):
        # self.gitlab_url = 'http://git.xs.jf'
        # self.gitlab_token = 'vV9F9eFJNcg9jPHkxs_B'
        self.gitlab_url = get_conf('gitlab','url')
        self.gitlab_token = get_conf('gitlab','token')
        self.gl = gitlab.Gitlab(self.gitlab_url,private_token=self.gitlab_token,api_version=3)
    def get_all_projects(self):
        re = []
        projects = self.gl.projects.list(all=True)
        for project in projects:
            re.append({'pid':project.id,'pname':project.path_with_namespace})
        return re
    def get_user_id(self, username):
        user = self.gl.users.get_by_username(username)
        return user.id
    def get_project_id(self, project):
        projectinfo = self.gl.projects.get(project)
        return projectinfo.id
    def set_project_member(self, gitlab_set_info):
        git_user = gitlab_set_info['git_user']
        git_projects = gitlab_set_info['git_project'].split(',')
        git_permission = gitlab_set_info['git_permission']
        user_id = self.get_user_id(git_user)
        if (git_permission == 'None'):
            for project in git_projects:
                projectinfo = self.gl.projects.get(project)
                try:
                    projectinfo.members.delete(user_id)
                    status = 'ok'
                except Exception as e:
                    status = 'fail'
        else:
            if (git_permission == 'Developer'):
                project_permission = gitlab.DEVELOPER_ACCESS
            elif (git_permission == 'Reporter'):
                project_permission = gitlab.REPORTER_ACCESS
            for project in git_projects:
                projectinfo = self.gl.projects.get(project)
                try:
                    member = projectinfo.members.create({'user_id': user_id, 'access_level': project_permission})
                    member.access_level = project_permission
                    member.save()
                    status = 'ok'
                except Exception as e:
                    status = 'fail'
        return status
    
    
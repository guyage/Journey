#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gitlab
import sys
import json

gitlab_url = 'http://git.xs.jf'
gitlab_token = 'vV9F9eFJNcg9jPHkxs_B'

gl = gitlab.Gitlab(gitlab_url,private_token=gitlab_token,api_version=3)

content = (json.loads(sys.argv[1]))
# content = '{"git_user":["guyage"],"git_project_group":"xs-guayge-test-group-a","git_project":"aaaaa","git_permission":"New"}'
# readmefile = '{"file_path": "readme.txt","branch_name": "master","content": "readme","commit_message": "Create readme.txt"}'
# content = (json.loads(content))
def get_user_id(username):
    user = gl.users.get_by_username(username)
    return user.id

def git_script(content):
    git_user = content['git_user']
    git_project = content['git_project']
    git_permission = content['git_permission']
    if (git_permission == 'Reporter' or git_permission == 'Developer' or git_permission == 'None'):
        for user in git_user:
            user_id = get_user_id(user)
            if (git_permission == 'Reporter' or git_permission == 'Developer'):
                if (git_permission == 'Reporter'):
                    project_permission = gitlab.DEVELOPER_ACCESS
                elif (git_permission == 'Reporter'):
                        project_permission = gitlab.REPORTER_ACCESS
                for project in git_project:
                    projectinfo = gl.projects.get(project)
                    try:
                        member = projectinfo.members.create({'user_id': user_id, 'access_level': project_permission})
                        member.access_level = project_permission
                        member.save()
                        status = 'success'
                    except Exception as e:
                        status = 'fail'
            elif (git_permission == 'None'):
                for project in git_project:
                    projectinfo = gl.projects.get(project)
                    try:
                        projectinfo.members.delete(user_id)
                        status = 'success'
                    except Exception as e:
                        status = 'fail'
    elif (git_permission == 'Create'):
        git_project_group = content['git_project_group']
        try:
            # 创建项目
            group_id = gl.groups.search(git_project_group)[0].id
            new_project = gl.projects.create({'name': git_project, 'namespace_id': group_id})
            # 创建readme
            project = git_project_group + '/' + git_project
            projectfileinfo = gl.projects.get(project)
            f = projectfileinfo.files.create({'file_path': 'readme.txt','branch_name': 'master','content': 'readme','commit_message': 'Create readme'})
            # 用户加权限
            project_permission = gitlab.DEVELOPER_ACCESS
            for user in git_user:
                user_id = get_user_id(user)
                projectinfo = gl.projects.get(project)
                member = projectinfo.members.create({'user_id': user_id, 'access_level': project_permission})
                member.access_level = project_permission
                member.save()
                status = 'success'
        except Exception as e:
            status = 'fail'
    elif (git_permission == 'New'):
        print ('1111')
        git_project_group = content['git_project_group']
        try:
            # 创建项目组
            print ('qqqq',git_project_group)
            new_group = gl.groups.create({'name': git_project_group, 'path': git_project_group})
            print ('2222',new_group)
            # 创建项目
            project_group_id = new_group.id
            new_project = gl.projects.create({'name': git_project, 'namespace_id': project_group_id})
            # 创建readme
            project = git_project_group + '/' + git_project
            projectfileinfo = gl.projects.get(project)
            print ('3333',projectfileinfo)
            f = projectfileinfo.files.create({'file_path': 'readme.txt','branch_name': 'master','content': 'readme','commit_message': 'Create readme'})
            # 用户加权限
            project_permission = gitlab.DEVELOPER_ACCESS
            for user in git_user:
                user_id = get_user_id(user)
                projectinfo = gl.projects.get(project)
                member = projectinfo.members.create({'user_id': user_id, 'access_level': project_permission})
                member.access_level = project_permission
                member.save()
                status = 'success'
        except Exception as e:
            print (e)
            status = 'fail'
    else:
        status = 'fail'


                
    print (status)

git_script(content)




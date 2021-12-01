"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from IssueTrackingSystem.views import ProjectViewSet, IssuesViewSet, ContributorViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
# --- generates :
# /projects/
# /projects/{project_pk}

project_issue = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_issue.register(r'issues', IssuesViewSet, basename='project-issue')
# ---generates :
# /projects/{project_pk}/issues
# /projects/{project_pk}/issues/{issue_pk}

contributors_of_project = routers.NestedSimpleRouter(router, r'projects', lookup='project')
contributors_of_project.register(r'users', ContributorViewSet, basename='contrib-of-project')
# --- generates :
# /projects/{project_pk}/users
# /projects/{project_pk}/users/{user_pk}

urlpatterns = [
    path('admin/', admin.site.urls),
    # Registration path, auth with token and refresh token
    path('', include('authentication.urls')),
    # Projects, Issues and Comments
    path('', include(router.urls)),
    path('', include(project_issue.urls)),

    # Add, display or delete a user in a project
    path('', include(contributors_of_project.urls)),

]

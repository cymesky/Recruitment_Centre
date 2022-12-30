from django.urls import path
from .views import PostRecruitListAPIView, PostRecruitDetailAPIView, \
    RecruitListAPIView, RecruitDetailAPIView, GroupedSkillzListAPIView, \
    GroupedSkillzDetailAPIView, SkillListAPIView, SkillDetailAPIView, SearchBySkillLevelListApiView, \
    AllSkillsListApiView

urlpatterns = [
    path('PostRecruits/', PostRecruitListAPIView.as_view(), name='postrecruit-list'),
    path('PostRecruit/<int:pk>/', PostRecruitDetailAPIView.as_view(), name='postrecruit-detail'),
    path('Recruits/', RecruitListAPIView.as_view(), name='recruit-list'),
    path('Recruit/<int:pk>/', RecruitDetailAPIView.as_view(), name='recruit-detail'),
    path('GroupedSkillzs/', GroupedSkillzListAPIView.as_view(), name='groupedskillz-list'),
    path('GroupedSkillz/<int:pk>/', GroupedSkillzDetailAPIView.as_view(), name='groupedskillz-detail'),
    path('Skills/', SkillListAPIView.as_view(), name='skill-list'),
    path('Skill/<int:pk>/', SkillDetailAPIView.as_view(), name='skill-detail'),
    path('AllSkills/', AllSkillsListApiView.as_view(), name='all-skills-list'),
    path('Search/', SearchBySkillLevelListApiView.as_view(), name='search'),
]

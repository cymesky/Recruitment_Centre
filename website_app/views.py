from .models import PostRecruit, Recruit, GroupedSkillz, Skill
from .serialializers import PostRecruitSerializer, RecruitSerializer, \
    GroupedSkillzSerializer, SkillSerializer
from rest_framework import generics


# Create your views here.
class PostRecruitListAPIView(generics.ListAPIView):
    queryset = PostRecruit.objects.all()
    serializer_class = PostRecruitSerializer


class PostRecruitDetailAPIView(generics.RetrieveAPIView):
    queryset = PostRecruit.objects.all()
    serializer_class = PostRecruitSerializer


class RecruitListAPIView(generics.ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer


class RecruitDetailAPIView(generics.RetrieveAPIView):
    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer


class GroupedSkillzListAPIView(generics.ListAPIView):
    queryset = GroupedSkillz.objects.all()
    serializer_class = GroupedSkillzSerializer


class GroupedSkillzDetailAPIView(generics.RetrieveAPIView):
    queryset = GroupedSkillz.objects.all()
    serializer_class = GroupedSkillzSerializer


class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDetailAPIView(generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

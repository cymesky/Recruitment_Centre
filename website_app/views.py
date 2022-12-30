from .models import PostRecruit, Recruit, GroupedSkillz, Skill
from .serializers import PostRecruitSerializer, RecruitSerializer, \
    GroupedSkillzSerializer, SkillSerializer, AllSkillsSerializer
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


# API returns all recruits from db that meet the specified conditions
# skill name = skill level
# example:
# /api/Search/Caldari+Battleship=5&Marauders=5&Drones=4
class SearchBySkillLevelListApiView(generics.ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer

    def get_queryset(self):
        first_query = True
        recruits_satysfying = []

        skills_to_search = self.request.GET
        if skills_to_search is not None:
            for k, v in skills_to_search.items():
                recruits = Recruit.objects.filter(
                    skills__skill_name=k, skills__skill_trained_level=v)

                if first_query:
                    recruits_satysfying = recruits
                    first_query = False
                else:
                    recruits_satysfying = recruits_satysfying & recruits

                if len(recruits_satysfying) == 0:
                    return Recruit.objects.none()

        return recruits_satysfying


class AllSkillsListApiView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = AllSkillsSerializer

    def get_queryset(self):
        recruit = Recruit.objects.last()

        skills = Skill.objects.filter(recruit=recruit)

        return skills

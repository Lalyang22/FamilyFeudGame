from django.db import models


class FamilyFeudGameProperRight(models.Model):
    team_1_score = models.IntegerField()

class FamilyFeudGameProperLeft(models.Model):
    team_2_score = models.IntegerField()

class FamilyFeudGameProperCenter(models.Model):
    id = models.AutoField(primary_key=True)
    questions = models.TextField()
    answer = models.TextField()
    status = models.CharField(max_length=255)

class FamilyFeudGameProperMaam(models.Model):
    id = models.AutoField(primary_key=True)
    questions = models.TextField()

from django.db import models

class FeudQuestion(models.Model):
    """Model to store questions"""
    question = models.TextField()

    def __str__(self):
        return self.question

class FeudAnswer(models.Model):
    """Model to store answers associated with a question"""
    question = models.ForeignKey(FeudQuestion, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.text} ({self.points} points)"

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

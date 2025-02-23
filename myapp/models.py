from django.db import models

class RoundGameQuestion(models.Model):
    """Model to store questions"""
    question = models.TextField()
    flag = models.BooleanField(default=False)  # ✅ Flag default is False (0)

    def __str__(self):
        return self.question
    
class RoundGameAnswer(models.Model):
    """Model to store answers associated with a question"""
    question = models.ForeignKey(RoundGameQuestion, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.text} ({self.points} points)"
    
class FastMoneyQuestion(models.Model):
    """Model to store Fast Money questions"""
    question = models.TextField()
    flag = models.BooleanField(default=False)  # Track if the question is used

    def __str__(self):
        return self.question

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)  # Ensure it's an AutoField
    game_name = models.CharField(max_length=255)
    game_winner = models.CharField(max_length=50)
    team_1_points = models.IntegerField()
    team_2_points = models.IntegerField()
    total_rounds = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    round_points_team1 = models.IntegerField(default=0)
    round_points_team2 = models.IntegerField(default=0)
    round_winner = models.CharField(max_length=50)
    round_life_team1 = models.IntegerField(default=3)
    round_life_team2 = models.IntegerField(default=3)

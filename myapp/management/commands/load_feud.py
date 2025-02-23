import json
import os
from django.core.management.base import BaseCommand
from myapp.models import FastMoneyQuestion, RoundGameQuestion, RoundGameAnswer
from django.conf import settings

class Command(BaseCommand):
    help = "Load feud questions from multiple JSON files into separate tables"

    def handle(self, *args, **kwargs):
        json_dir = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'json')

        # ✅ Load Game Round Questions
        questions_path = os.path.join(json_dir, "questions.json")
        if os.path.exists(questions_path):
            self.load_game_round_questions(questions_path)
        else:
            self.stdout.write(self.style.ERROR(f"❌ questions.json file not found: {questions_path}"))

        # ✅ Load Fast Money Questions
        fastmoney_path = os.path.join(json_dir, "fastmoney.json")
        if os.path.exists(fastmoney_path):
            self.load_fast_money_questions(fastmoney_path)
        else:
            self.stdout.write(self.style.ERROR(f"❌ fastmoney.json file not found: {fastmoney_path}"))

        self.stdout.write(self.style.SUCCESS("✅ All data successfully inserted into the database!"))

    def load_game_round_questions(self, filepath):
        """Load standard game round questions into RoundGameQuestion and RoundGameAnswer"""
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            question_text = item.get("question", "Unknown Question")
            answers = item.get("answers", [])

            # ✅ Create a new RoundGameQuestion
            question = RoundGameQuestion.objects.create(question=question_text)

            # ✅ Add answers related to this question
            for answer in answers:
                RoundGameAnswer.objects.create(
                    question=question,
                    text=answer["text"],
                    points=answer["points"]
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Added Round Question: {question_text} ({len(answers)} answers)"))

    def load_fast_money_questions(self, filepath):
        """Load Fast Money questions into FastMoneyQuestion"""
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            question_text = item.get("question", "Unknown Fast Money Question")

            # ✅ Create a FastMoneyQuestion entry
            FastMoneyQuestion.objects.create(question=question_text)

            self.stdout.write(self.style.SUCCESS(f"✅ Added Fast Money Question: {question_text}"))

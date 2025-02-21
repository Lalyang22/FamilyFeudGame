import json
import os
from django.core.management.base import BaseCommand
from myapp.models import FeudQuestion, FeudAnswer
from django.conf import settings

class Command(BaseCommand):
    help = "Load feud questions from JSON file into the database"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'json', 'questions.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found: {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            question_text = item.get("question", "Unknown Question")
            answers = item.get("answers", [])

            # Create the question
            question = FeudQuestion.objects.create(question=question_text)

            # Add multiple answers for this question
            for answer in answers:
                FeudAnswer.objects.create(
                    question=question,
                    text=answer["text"],
                    points=answer["points"]
                )

            print(f"✅ Added: {question_text} ({len(answers)} answers)")

        self.stdout.write(self.style.SUCCESS("✅ Data successfully inserted into the database!"))

from django.core.management.base import BaseCommand
from myapp.models import Game  # Replace 'myapp' with your actual app name

class Command(BaseCommand):
    help = "Load feud game data into the database"

    def handle(self, *args, **kwargs):
        if not Game.objects.exists():
            self.stdout.write(self.style.SUCCESS("📌 No games found. Creating default game..."))

            game = Game.objects.create(
                game_name="Default Feud Game",
                game_winner="team1",
                team_1_points=0,
                team_2_points=0,
                total_rounds=3
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Game Created! game_id: {game.game_id}"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Game data already exists. No new data added."))

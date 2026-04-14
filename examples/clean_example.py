class UserRepository:
    """Handles data persistence for users."""
    def save(self, name: str, email: str) -> None:
        with open("db.txt", "a") as f:
            f.write(f"{name},{email}\n")

class NotificationService:
    """Handles communication with users."""
    def send_welcome_email(self, email: str) -> None:
        print(f"Sending email to {email}")

def register_user(name: str, email: str) -> bool:
    """Orchestrates user registration following SRP."""
    repo = UserRepository()
    notifier = NotificationService()
    
    repo.save(name, email)
    notifier.send_welcome_email(email)
    return True

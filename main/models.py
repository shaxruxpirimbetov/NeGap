from user.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_receiver")
    text = models.TextField()
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} #{self.id}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class Answer(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="answer_message")
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_message_sender", blank=True, null=True)
    text = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to {self.message}"

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

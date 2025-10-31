from django.db import models


class Note(models.Model):
    """
    Note model representing a to-do note.
    Fields:
      - id: Auto-generated primary key
      - title: Required short title for the note
      - description: Optional detailed text
      - is_completed: Boolean flag indicating completion
      - created_at: Auto-added timestamp on create
      - updated_at: Auto-updated timestamp on save
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # set on insert
    updated_at = models.DateTimeField(auto_now=True)      # set on each save

    def __str__(self) -> str:
        return f"{self.title} ({'done' if self.is_completed else 'open'})"

from rest_framework import serializers
from .models import Note


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model with basic validation enforcing required title."""
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Note
        fields = ["id", "title", "description", "is_completed", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_title(self, value: str) -> str:
        """Ensure title is provided and not empty/whitespace."""
        if value is None or str(value).strip() == "":
            raise serializers.ValidationError("This field may not be blank.")
        return value

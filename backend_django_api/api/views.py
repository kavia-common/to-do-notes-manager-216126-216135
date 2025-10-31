from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import Note
from .serializers import NoteSerializer


@api_view(['GET'])
def health(request):
    """Simple health check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_id="notes_list",
    operation_summary="List notes",
    operation_description="Returns a list of all to-do notes.",
    responses={200: NoteSerializer(many=True)},
    tags=["notes"],
)
@swagger_auto_schema(
    method='post',
    operation_id="notes_create",
    operation_summary="Create note",
    operation_description="Create a new to-do note. Title is required.",
    request_body=NoteSerializer,
    responses={201: NoteSerializer, 400: "Validation Error"},
    tags=["notes"],
)
@api_view(['GET', 'POST'])
def notes_collection(request):
    """
    Handle listing all notes and creating a new note.
    GET: 200 OK with array of notes.
    POST: 201 Created with created note, or 400 Bad Request for validation errors.
    """
    if request.method == 'GET':
        queryset = Note.objects.all().order_by('-created_at')
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        note = serializer.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


note_id_param = openapi.Parameter('id', openapi.IN_PATH, description="Note ID", type=openapi.TYPE_INTEGER, required=True)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_id="notes_retrieve",
    operation_summary="Retrieve note",
    operation_description="Retrieve a specific to-do note by ID.",
    manual_parameters=[note_id_param],
    responses={200: NoteSerializer, 404: "Not Found"},
    tags=["notes"],
)
@swagger_auto_schema(
    method='put',
    operation_id="notes_update",
    operation_summary="Update note",
    operation_description="Update a note by replacing all fields.",
    manual_parameters=[note_id_param],
    request_body=NoteSerializer,
    responses={200: NoteSerializer, 400: "Validation Error", 404: "Not Found"},
    tags=["notes"],
)
@swagger_auto_schema(
    method='patch',
    operation_id="notes_partial_update",
    operation_summary="Partially update note",
    operation_description="Partially update a note with provided fields.",
    manual_parameters=[note_id_param],
    request_body=NoteSerializer,
    responses={200: NoteSerializer, 400: "Validation Error", 404: "Not Found"},
    tags=["notes"],
)
@swagger_auto_schema(
    method='delete',
    operation_id="notes_delete",
    operation_summary="Delete note",
    operation_description="Delete a note by ID.",
    manual_parameters=[note_id_param],
    responses={204: "No Content", 404: "Not Found"},
    tags=["notes"],
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def notes_detail(request, id: int):
    """
    Retrieve, update (PUT/PATCH), or delete a note by ID.
    - GET: 200 OK with note data or 404 if not found.
    - PUT/PATCH: 200 OK with updated note or 400/404.
    - DELETE: 204 No Content or 404 if not found.
    """
    note = get_object_or_404(Note, id=id)

    if request.method == 'GET':
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = NoteSerializer(instance=note, data=request.data, partial=partial)
        if serializer.is_valid():
            note = serializer.save()
            return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    note.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

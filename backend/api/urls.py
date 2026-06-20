from django.urls import path
from .views import NoteListCreate, NoteDelete,PublicChordDetail,PublicChordList,UserChordDetailUpdateDestroy,UserChordListCreate, VectorSearchSongView

urlpatterns = [
    path("notes/", NoteListCreate.as_view(), name="Note"),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="Delete_Note"),
    path("chords/public/", PublicChordList.as_view(), name="Public_Chord_List"),
    path("chords/public/details/<int:pk>/", PublicChordDetail.as_view(), name="Public_Chord_Detail"),
    path("chords/user/", UserChordListCreate.as_view(), name="User_Chord"),
    path("chords/user/update/<int:pk>/", UserChordDetailUpdateDestroy.as_view(),name="Chord_Update"),
    path('api/songs/search-vector/', VectorSearchSongView.as_view(), name='search-vector-songs'),
]
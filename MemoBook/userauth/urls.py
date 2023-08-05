from django.urls import path
from .views import register, home, loginuser, tasks, delete_memo, edit_memo

urlpatterns = [
    path("", home, name='home'),
    path("register/", register, name='register'),
    path("login/", loginuser, name='login'),
    path("notes/", tasks, name='notes'),
    path('delete/<uuid:memo_id>', delete_memo, name='delete_memo'),
    path('edit/<uuid:memo_id>', edit_memo, name='edit_memo')
]

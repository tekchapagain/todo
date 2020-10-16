from django.contrib import admin
from django.urls import path
from todoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('login/',views.loginuser,name = 'loginuser'),
    path('logout/',views.logoutuser,name = 'logoutuser'),
    path('signup/',views.signupuser,name = 'signupuser'),

    #TODO
    path('create/',views.create,name = 'create'),
    path('completed/',views.completed,name = 'completed'),
    path('home/',views.home,name = 'home'),
    path('todo/<int:todo_pk>',views.viewtodo,name = 'viewtodo'),
    path('todo/<int:todo_pk>/complete',views.completetodo,name = 'completetodo'),
    path('todo/<int:todo_pk>/delete',views.deletetodo,name = 'deletetodo'),
]

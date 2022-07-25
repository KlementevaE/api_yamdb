from django.contrib import admin

from .models import User, Category, Genre, TitleGenre, Title, Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'bio',
                    'first_name', 'last_name')


admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


admin.site.register(Genre, GenreAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'discription', 'category')


admin.site.register(Title, TitleAdmin)


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'genre_id')


admin.site.register(TitleGenre, TitleGenreAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')


admin.site.register(Comment, CommentAdmin)

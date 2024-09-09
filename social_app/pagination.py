from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    """
    Postlarni sahifalash uchun klass.
    Har bir sahifada 10 ta post ko'rsatiladi.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

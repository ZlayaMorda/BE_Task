from rest_framework.pagination import PageNumberPagination


class PageListPaginationClass(PageNumberPagination):
    page_size = 10

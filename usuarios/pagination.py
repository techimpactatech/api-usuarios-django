from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil

class ZeroBasedPageNumberPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 20
    max_page_size = 100

    def get_page_number(self, request, paginator):
        raw = request.query_params.get(self.page_query_param, 0)
        try:
            page0 = int(raw)
        except (TypeError, ValueError):
            page0 = 0
        return max(page0 + 1, 1)  # DRF é 1-based internamente

    def get_paginated_response(self, data):
        curr_page0 = max(self.page.number - 1, 0)
        size = self.get_page_size(self.request) or self.page.paginator.per_page
        total = self.page.paginator.count
        total_pages = ceil(total / size) if size else 0
        return Response({
            "content": data,
            "page": curr_page0,
            "size": size,
            "totalElements": total,
            "totalPages": total_pages
        })
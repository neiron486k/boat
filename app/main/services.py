class DefaultService:
    @staticmethod
    def paginate(query, page: int = 1, limit: int = 10):
        paginated_data = query.paginate(per_page=limit, page=page)
        meta = dict(
            total=paginated_data.total,
            page=paginated_data.page,
            pages=paginated_data.pages,
            limit=paginated_data.per_page
        )
        return dict(data=paginated_data.items, meta=meta)

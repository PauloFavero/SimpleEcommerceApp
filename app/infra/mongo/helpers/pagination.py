from typing import Dict, Any


def build_pagination_query(page, limit) -> Dict[str, Any]:
    page = 1 if page is None or page == 0 else page
    skip = (page - 1) * limit
    return [
        {
            "$facet": {
                "metadata": [{"$count": "total"}],
                "data": [{"$addFields": {"_id": "$_id"}}],
            }
        },
        {"$project": {"data": 1, "total": {"$arrayElemAt": ["$metadata.total", 0]}}},
        {
            "$project": {
                "data": {"$slice": ["$data", skip, {"$ifNull": [limit, "$total"]}]},
                "pagination": {
                    "total": {"$ifNull": ["$total", 0]},
                    "limit": {"$literal": limit},
                    "page": {"$literal": ((skip / limit) + 1)},
                    "pages": {
                        "$ifNull": [{"$ceil": {"$divide": ["$total", limit]}}, 0]
                    },
                },
            }
        },
    ]

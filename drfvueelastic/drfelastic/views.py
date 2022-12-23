from rest_framework import viewsets
from rest_framework.response import Response
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def search(self, request):
        search_type = request.GET.get('searchType')
        query = request.GET.get('search')
        if search_type == 'full-text':
            search = Search(index='articles').query('match', title=query)
        elif search_type == 'boolean':
            search = Search(index='articles').query('bool', must=[Q('match', title=query), Q('match', content=query)])
        elif search_type == 'fuzzy':
            search = Search(index='articles').query('fuzzy', title=query)
        elif search_type == 'wildcard':
            search = Search(index='articles').query('wildcard', title=f"*{query}*")
        elif search_type == 'regex':
            search = Search(index='articles').query('regexp', title=f"/{query}/")
        search.execute()
        serializer = ArticleSerializer(search, many=True)
        return Response(serializer.data)

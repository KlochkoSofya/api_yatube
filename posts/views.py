from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions, serializers


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly,]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
   
          
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = CommentSerializer
    # queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = post.comments.all()
        serializer_class = CommentSerializer(queryset, many=True)
        return post.comments
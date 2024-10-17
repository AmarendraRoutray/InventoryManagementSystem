from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from AuthApp.customAuth import CustomAuthentication
from django.core.cache import cache
from django.conf import settings

class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        """Create a new item."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        """Retrieve an item by ID."""
        # Define a cache key based on the item ID
        cache_key = f'item_{pk}'
        
        # Check if the item is in cache
        item = cache.get(cache_key)
        if item:
            return Response(item)  # Return cached item if available

        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)

            # Store the item in the cache for future requests
            cache.set(cache_key, serializer.data, timeout=settings.CACHE_TIMEOUT)

            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)

    def update(self, request, pk=None):
        """Update an item by ID."""
        try:
            item = Item.objects.get(pk=pk)
            serializer = self.get_serializer(item, data=request.data, partial=True)  # Allow partial updates
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Invalidate the cache for this item since it has been updated
            cache_key = f'item_{pk}'
            cache.delete(cache_key)

            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)

    def destroy(self, request, pk=None):
        """Delete an item by ID."""
        try:
            item = Item.objects.get(pk=pk)
            item.delete()

            # Invalidate the cache for this item
            cache_key = f'item_{pk}'
            cache.delete(cache_key)

            return Response({"message": "Item deleted successfully"}, status=204)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)

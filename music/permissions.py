from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create/update/delete music.
    Read-only access is allowed for authenticated users.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class IsSubscribed(permissions.BasePermission):
    """
    Custom permission to only allow subscribed users to access music content.
    This is a placeholder. You need to implement the actual subscription check
    based on your 'subscriptions' app's models.
    """
    def has_permission(self, request, view):
        # For now, just check if authenticated. You need to replace this
        # with actual subscription logic (e.g., checking user.is_subscribed or similar).
        # Example: return request.user and request.user.is_authenticated and request.user.is_subscribed
        return request.user and request.user.is_authenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
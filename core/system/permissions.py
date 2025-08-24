from rest_framework.permissions import BasePermission

class IsSuperAdminOrAgent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print('username : ', request.user.username)
        print('group : ', [g.name for g in request.user.groups.all()])
        return request.user.groups.filter(name__in=["SuperAdmin", "Agent"]).exists()
    
def IsModelPermissionFactory(model_or_serializer):
    class _IsModelPermission(BasePermission):
        def has_permission(self, request, view):
            # print('User:', request.user)
            # print('group : ', [g.name for g in request.user.groups.all()])
            # print('Request method:', request.method)
            # print('View:', view)
            
            if not request.user or not request.user.is_authenticated:
                print('Not authenticated!')
                return False

            if hasattr(model_or_serializer, "Meta") and hasattr(model_or_serializer.Meta, "model"):
                model = model_or_serializer.Meta.model
            else:
                model = model_or_serializer

            # print('Checking model:', model)

            app_label = model._meta.app_label
            model_name = model._meta.model_name
            # print('app_label:', app_label, 'model_name:', model_name)

            if request.method == "POST":
                perm = f"{app_label}.add_{model_name}"
            elif request.method in ["PUT", "PATCH"]:
                perm = f"{app_label}.change_{model_name}"
            elif request.method == "DELETE":
                perm = f"{app_label}.delete_{model_name}"
            else:  # GET
                perm = f"{app_label}.view_{model_name}"

            print('Permission to check:', perm, 'User has perm:', request.user.has_perm(perm))
            return request.user.has_perm(perm)

    return _IsModelPermission




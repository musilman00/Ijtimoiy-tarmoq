from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat obyekt egasiga yozish (o'zgartirish yoki o'chirish) ruxsatini beradi,
    boshqa foydalanuvchilarga faqat o'qish ruxsati beriladi.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD yoki OPTIONS so'rovlariga umumiy ruxsat
        if request.method in permissions.SAFE_METHODS:
            return True

        # Faqat obyekt egasi yozish (o'zgartirish yoki o'chirish) ruxsatiga ega
        return obj.user == request.user

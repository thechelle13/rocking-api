from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rockapi.models import Rock, Type



class RockView(ViewSet):
    """Rock view set"""
    # permission_classes = (permissions.AllowAny,)
    
    # def get_permissions(self):
    #     """
    #     Override the get_permissions method to set permissions dynamically.

    #     GET requests do not require a token
    #     POST, PUT, DELETE require a token
    #     """
    #     method = self.request.method
    #     if method == "GET":
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]  # Default permission for other methods
    #     return [permission() for permission in permission_classes]

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
    # Get an object instance of a rock type
        chosen_type = Type.objects.get(pk=request.data['typeId'])

        # Create a rock object and assign it property values
        rock = Rock()
        rock.user = request.auth.user
        rock.weight = request.data['weight']
        rock.name = request.data['name']
        rock.type = chosen_type
        rock.save()

        serialized = RockSerializer(rock, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
        # You will implement this feature in a future chapter
       # return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
       # Get query string parameter
        owner_only = self.request.query_params.get("owner", None)

        try:
            # Start with all rows
            rocks = Rock.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's rocks
                rocks = rocks.filter(user=request.auth.user)

            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rock = Rock.objects.get(pk=pk)
            # Explicitly check if the user is authenticated
         
                

                # Handle the case where rock.user is None (if allowed by your model)
            if rock.user and rock.user.id == request.auth.user.id:
                    rock.delete()
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                    return Response({'message': 'You do not own that rock'}, status=status.HTTP_403_FORBIDDEN)
        
        except Rock.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RockOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = User
        fields = ( 'first_name','last_name', )

class RockTypeSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Type
        fields = ( 'label', )

class RockSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    type = RockTypeSerializer(many=False)
    user = RockOwnerSerializer(many=False)

    class Meta:
        model = Rock
        fields = ( 'id', 'name', 'weight', 'type', 'user', )

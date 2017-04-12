from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from assets.models import Asset, AssetDetail
from assets.serializers import AssetSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def asset_list(request):
    """
    List all assets, or create a new one
    
    :param request: HTTP request object
    :return: JSON response
    """
    if request.method == 'GET':
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Check that admin user is creating objects
        user = request.META.get('HTTP_X_USER', 'anon')
        if user != 'admin':
            print([user for user in sorted(request.META.keys())])
            return Response('Only admin user can create assets', status=status.HTTP_401_UNAUTHORIZED)

        data = JSONParser().parse(request)
        serializer = AssetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def asset_classfilter(request, class_name):
    """
    List assets filtered by the provided class string
    :param request: Django HTTP request
    :param class_name: The name of the class to perform filtering
    :return: Response with appropriate assets
    """
    if request.method == 'GET':
        assets = Asset.objects.filter(asset_class=class_name)
        if not assets:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AssetSerializer(assets, many=True)
            return Response(serializer.data)

@api_view(['GET'])
def asset_typefilter(request, type_name):
    """
    List assets filtered by the provided type string
    :param request: Django HTTP 
    :param type_name: The name of the type to perform filtering
    :return: Response with appropriate assets
    """
    if request.method == 'GET':
        assets = Asset.objects.filter(asset_type=type_name)
        if not assets:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AssetSerializer(assets, many=True)
            return Response(serializer.data)

@api_view(['GET'])
def asset_detail(request, pk):
    """
    Retrieve an asset with its corresponding details
    Updating and deleting assets is not allowed in this API
    
    :param request: HTTP request object
    :param pk: Asset's primary key, which is its unique name
    :return: JSON response
    """
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



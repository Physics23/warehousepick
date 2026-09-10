from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import random
from rest_framework import generics, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Station, Item, Tote, PickSession, PickTask
from .serializers import (
    StationSerializer, ItemSerializer, ToteSerializer,
    PickSessionSerializer, PickTaskSerializer, StationStatsSerializer
)

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

# AUTH
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "operator": username}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        station_id = request.data.get('station_id')
        if station_id:
            PickSession.objects.filter(station__station_id=station_id, is_active=True).update(
                is_active=False, end_time=timezone.now()
            )
        logout(request)
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)


# CRUD VIEWSETS
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]


class ToteViewSet(viewsets.ModelViewSet):
    queryset = Tote.objects.all()
    serializer_class = ToteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]


class PickSessionViewSet(viewsets.ModelViewSet):
    queryset = PickSession.objects.all()
    serializer_class = PickSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @action(detail=False, methods=['post'], url_path='start')
    def start_session(self, request):
        station = Station.objects.filter(station_id='ToteASRS4159').first()
        if not station:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)

        session, _ = PickSession.objects.get_or_create(
            station=station,
            operator_name=request.user.username,
            is_active=True,
            defaults={'start_time': timezone.now()}
        )

        source_tote = Tote.objects.filter(tote_id='BIN-01').first() or Tote.objects.create(tote_id='BIN-01')
        dest_tote = Tote.objects.filter(tote_id='TOTE-42').first() or Tote.objects.create(tote_id='TOTE-42')

        random_id = random.randint(1000, 9999)

        new_items = []
        for i in range(1, 21):
            sku = f'SIGNIN-{random_id}-{i:04d}'
            item, _ = Item.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': f'Sign-in Item {i}',
                    'description': f'Auto-generated item for fresh session. SKU: {sku}',
                    'image': f'https://picsum.photos/seed/{sku}/300/300'
                }
            )
            new_items.append(item)

        tasks_created = 0
        for item in new_items:
            task, created = PickTask.objects.get_or_create(
                session=session,
                item=item,
                source_tote=source_tote,
                destination_tote=dest_tote,
                defaults={'status': PickTask.Status.PENDING}
            )
            if created:
                tasks_created += 1

        return Response({"message": f"Created {tasks_created} new tasks with pictures!"}, status=status.HTTP_201_CREATED)


class PickTaskViewSet(viewsets.ModelViewSet):
    queryset = PickTask.objects.all()
    serializer_class = PickTaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = [choice[0] for choice in PickTask.Status.choices]
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        task.status = new_status
        if new_status == PickTask.Status.PICKED:
            task.picked_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


    @action(detail=False, methods=['post'], url_path='re-seed')
    def re_seed(self, request):
        station = Station.objects.filter(station_id='ToteASRS4159').first()
        if not station:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)

        session = PickSession.objects.filter(station=station, is_active=True).first()
        if not session:
            return Response({"error": "Active session not found"}, status=status.HTTP_404_NOT_FOUND)

        source_tote = Tote.objects.filter(tote_id='BIN-01').first() or Tote.objects.create(tote_id='BIN-01')
        dest_tote = Tote.objects.filter(tote_id='TOTE-42').first() or Tote.objects.create(tote_id='TOTE-42')

        random_id = random.randint(1000, 9999)
        new_items = []
        for i in range(1, 21):
            sku = f'RE-{random_id}-{i:04d}'
            item, _ = Item.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': f'Re-seeded Item {i}',
                    'description': f'Auto-generated item. SKU: {sku}',
                    'image': f'https://picsum.photos/seed/{sku}/300/300'
                }
            )
            new_items.append(item)

        tasks_created = 0
        for item in new_items:
            task, created = PickTask.objects.get_or_create(
                session=session,
                item=item,
                source_tote=source_tote,
                destination_tote=dest_tote,
                defaults={'status': PickTask.Status.PENDING}
            )
            if created:
                tasks_created += 1

        return Response({"message": f"Created {tasks_created} new pending tasks!"}, status=status.HTTP_201_CREATED)


# CUSTOM ENDPOINTS
class CurrentTaskView(generics.GenericAPIView):
    serializer_class = PickTaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, station_id):
        station = Station.objects.filter(station_id=station_id).first()
        if not station:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)

        session = PickSession.objects.filter(station=station, is_active=True).first()
        if not session:
            return Response({"task": None, "message": "No active session"}, status=status.HTTP_200_OK)

        current_task = PickTask.objects.filter(session=session, status=PickTask.Status.PENDING).first()
        if not current_task:
            return Response({"task": None, "message": "All tasks completed"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(current_task)
        return Response({"task": serializer.data})


class StationStatsView(generics.GenericAPIView):
    serializer_class = StationStatsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, station_id):
        station = Station.objects.filter(station_id=station_id).first()
        if not station:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)

        session = PickSession.objects.filter(station=station, is_active=True).first()
        if not session:
            return Response({"stats": {}}, status=status.HTTP_200_OK)

        picked_tasks = PickTask.objects.filter(session=session, status=PickTask.Status.PICKED)
        total_units = picked_tasks.count()

        if session.end_time:
            session_seconds = (session.end_time - session.start_time).total_seconds()
        else:
            session_seconds = (timezone.now() - session.start_time).total_seconds()

        timestamps = list(picked_tasks.order_by('picked_at').values_list('picked_at', flat=True))
        cycle_time_secs = 0
        if len(timestamps) > 1:
            total_delta = sum((timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1))
            cycle_time_secs = round(total_delta / (len(timestamps) - 1), 2)

        uph = 0
        if session_seconds > 0:
            uph = round((total_units / session_seconds) * 3600, 2)

        data = {
            "rate_uph": uph,
            "cycle_time_secs": cycle_time_secs,
            "session_time_secs": round(session_seconds, 2),
            "total_units_picked": total_units,
            "operator_name": session.operator_name,
        }
        serializer = self.get_serializer(data)
        return Response({"stats": serializer.data})


# METHOD 3: UPLOAD WITH PICTURE
class CreateItemWithImageView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
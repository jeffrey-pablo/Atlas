from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from invoices.models import Invoice
from .models.sessions import Session
from .models.time_sheets import TimeSheet
from .serializers import TimeSheetSerializer, SessionSerializer

from datetime import datetime, timedelta, time

from django.db.models import Min, Max


# Create your views here.
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        return queryset

    @action(detail=False, methods=['get'], url_path='current-session')
    def current_session(self, request):
        active_session = self.get_queryset().filter(time_out=None, active=True)
        assert active_session.count() <= 1, "There should be only one active session"
        first_name = request.user.first_name
        if active_session:
            serializer = SessionSerializer(active_session[0])
        else:
            serializer = SessionSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @current_session.mapping.patch
    def pause_current_session(self, request):
        session_id = request.data['id']
        pause_timestamp = request.data.get('pause_timestamp', None)
        continue_timestamp = request.data.get('continue_timestamp', None)
        end_timestamp = request.data.get('end_timestamp', None)
        _action = request.data['action']

        if _action == 'pause':
            active_session = self.get_queryset().filter(id=session_id)
            assert active_session.count() == 1, "There should be only one active session"

            active_session.update(paused=True, pause_start=pause_timestamp)
            serializer = SessionSerializer(active_session[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        if _action == "continue":
            active_sessions = self.get_queryset().filter(id=session_id)
            assert active_sessions.count() == 1, "There should be only one active session"
            active_session = active_sessions.first()

            # parse continue_timestamp to datetime object and calculate the total pause duration and increment it to the
            # total pause duration
            continue_dt = parse_datetime(continue_timestamp)

            increment_value = continue_dt - active_session.pause_start
            active_session.paused = False
            active_session.total_pause_duration += increment_value
            active_session.paused_end = continue_timestamp
            active_session.save()

            serializer = SessionSerializer(active_session)

            return Response(serializer.data, status=status.HTTP_200_OK)

        if _action == "end":
            active_sessions = self.get_queryset().filter(id=session_id)
            assert active_sessions.count() == 1, "There should be only one active session"
            active_session = active_sessions.first()

            end_dt = parse_datetime(end_timestamp)

            # Calculate the total duration of the session
            active_session.time_out = end_dt
            active_session.session_time = end_dt - active_session.time_in - active_session.total_pause_duration
            active_session.active = False
            active_session.save()

            serializer = SessionSerializer(active_session)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @current_session.mapping.post
    def post_current_session(self, request):
        """Method for creating a new Session object, this method is called from the frontend function:

        startButtonAction()
        """
        time_in = request.data['time_in']
        active = request.data['active']
        user = request.user

        # TODO: Check if there is an active session

        serializer = SessionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()

        # Serialize the session object
        serialized_data = SessionSerializer(session)

        # Extract session data
        session_data = serialized_data.data

        # Convert session data to the desired format
        session_data["date"] = session.time_in.date()
        session_data["time_in_hour"] = session.time_in.time().strftime("%I:%M %p")
        session_data["time_out_hour"] = session.time_out.time().strftime("%I:%M %p") if session.time_out else None


        time_options = ['12:00 AM', '12:30 AM', '01:00 AM', '01:30 AM', '02:00 AM', '02:30 AM', '03:00 AM', '03:30 AM', '04:00 AM', '04:30 AM', '05:00 AM', '05:30 AM', '06:00 AM', '06:30 AM', '07:00 AM', '07:30 AM', '08:00 AM', '08:30 AM', '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM', '08:00 PM', '08:30 PM', '09:00 PM', '09:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']

        context = {
            'session': session_data,
            'time_options':time_options,
        }

        return render(request, 'sessions_timesheets/sessions_detail.html', context)


    def perform_create(self, serializer):
        user = self.request.user
        time_in = serializer.validated_data['time_in']
        week_number = time_in.isocalendar()[1]
        monday = time_in - timedelta(days=time_in.weekday())
        if monday.year < time_in.year or monday.isocalendar()[1] != week_number:
            monday = monday + timedelta(days=7)
        week_of_value = datetime.combine(monday, time(), tzinfo=time_in.tzinfo)
        timesheet_instances = TimeSheet.objects.filter(sessions__user=user).filter(week_of=week_of_value).distinct()

        if timesheet_instances:
            timesheet = timesheet_instances[0]
        else:
            timesheet = TimeSheet.objects.create(name=f"Week of {week_of_value}", week_of=week_of_value)

        serializer.save(time_sheet=timesheet, user=user, time_in=time_in)


@login_required(login_url='/accounts/login/')
def sessions_form_view(request):
    if request.method == 'POST':
        invoice = Invoice()
        invoice.task = request.POST.get('task')
        invoice.description = request.POST.get('description')
        invoice.total_hours = request.POST.get('total_hours')
        invoice.save()
    user = request.user
    first_name = user.first_name
    return render(request, 'sessions_timesheets/sessions_form.html', context={'first_name': first_name})

@login_required(login_url='/accounts/login/')
def sessions_index_view(request):
    return render(request, 'sessions_timesheets/sessions_index.html')

@login_required(login_url='/accounts/login/')
def sessions_detail_view(request):
    filter_by = request.GET.get('filter_by')
    filter_date = request.GET.get('filter_date')

    user = request.user
    sessions = Session.objects.filter(user=user)

    if filter_by == 'day' and filter_date:
        # Filter sessions for a specific day
        sessions = sessions.filter(time_in__date=filter_date)

    elif filter_by == 'week' and filter_date:
        # Calculate the start and end date of the week based on the selected date
        selected_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
        weekday_num = (selected_date.weekday() + 1) % 7  # Adjusting for Sunday as 0 and Saturday as 6
        start_date = selected_date - timedelta(days=weekday_num)
        end_date = start_date + timedelta(days=6)

        # Filter sessions for the week
        sessions = sessions.filter(time_in__date__range=[start_date, end_date])

    elif filter_by == 'month' and filter_date:
        # Calculate the start and end date of the month based on the selected date
        selected_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
        start_date = selected_date.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Filter sessions for the month
        sessions = sessions.filter(time_in__date__range=[start_date, end_date])

    context = {
        'sessions': sessions,
        'filter_by': filter_by,
        'filter_date': filter_date,
    }
    return render(request, 'sessions_timesheets/sessions_detail.html', context)

def total_hours_to_float(total_hours):
    # Convert timedelta to total hours as float
    return total_hours.total_seconds() / timedelta(hours=1).total_seconds()

@login_required(login_url='/accounts/login/')
def timesheets_table_view(request):
    selected_week = request.GET.get('week_number')
    # Filter the Session objects based on the selected week
    sessions = Session.objects.filter(time_in__week=selected_week)

    # Find the earliest time_in, latest time_out, and calculate total hours
    start_time = sessions.aggregate(Min('time_in'))['time_in__min']
    end_time = sessions.aggregate(Max('time_out'))['time_out__max']
    total_hours = sum(total_hours_to_float(session.total_hours_worked) for session in sessions)

    # Prepare the context to pass to the template
    context = {
        'sessions': sessions,
        'start_time': start_time,
        'end_time': end_time,
        'total_hours': total_hours,
    }

    return render(request, 'sessions_timesheets/timesheets_table.html', context)

@login_required(login_url='/accounts/login/')
def timesheets_index_view(request):
    return render(request, 'sessions_timesheets/timesheets_index.html')


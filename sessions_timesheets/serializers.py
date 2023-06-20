from rest_framework import serializers
from .models.sessions import Session
from .models.time_sheets import TimeSheet

class SessionSerializer(serializers.ModelSerializer):

    session_in_hours = serializers.SerializerMethodField()
    time_in_hourly = serializers.SerializerMethodField()
    time_out_hourly = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ("id","time_in", "active","time_out","session_time","session_in_hours","time_in_hourly","time_out_hourly", "paused", "pause_start", "pause_end", "total_pause_duration")

    def get_time_in_hourly(self,obj):
        if obj.time_out:
            return obj.time_out.time().strftime("%I:%M %p")
        else:
            return "None"

    def get_time_out_hourly(self,obj):
        if obj.time_out:
            return obj.time_out.time().strftime("%I:%M %p")
        else:
            return "None"

    def get_session_in_hours(self,obj):
        if obj.session_time:
            hours = round(obj.session_time.total_seconds() / 3600, 1)
            return str(hours) + " hours"
        else:
            return "N/A"


    def create(self, validated_data):
        user = self.context['request'].user
        time_in = validated_data.get('time_in')
        time_out = validated_data.get('time_out')
        if time_out:
            validated_data['session_time'] = time_out - time_in
        validated_data['user'] = user
        instance = super().create(validated_data)
        return instance


class TimeSheetSerializer(serializers.ModelSerializer):

    sessions = SessionSerializer(many=True,read_only=True)

    class Meta:
        model = TimeSheet
        fields = ("id","name","sessions","week_of")
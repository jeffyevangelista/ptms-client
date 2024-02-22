from rest_framework import serializers
from .models import RequestForm
from businessUnit.models import BusinessUnit
from user.models import User
class RequestForm_Serializer(serializers.ModelSerializer):
    business_unit_name =  serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    encoder_name = serializers.CharField(source='encoded_by.first_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    approved = serializers.CharField(source='approved_by.first_name', read_only=True)
    release = serializers.CharField(source='release_by.first_name', read_only=True)
    class Meta:
        model = RequestForm
        fields = (
                'id',
                'voucher_no',
                'activity',
                'profit_center',
                'covered_from',
                'covered_to',
                'date_requested',
                'descriptions',
                'quantity',
                'uom',
                'price',
                'amount',
                'business_unit',
                'encoded_by',
                'reviewed_by',
                'approved_by',
                'release_by',
                'business_unit_name',
                'encoder_name',
                'reviewer_name',
                'approved',
                'release',

        )

class Request_Serializer(serializers.Serializer):
    voucher_no = serializers.CharField(read_only=True)
    business_unit = serializers.PrimaryKeyRelatedField(queryset=BusinessUnit.objects.all())
    activity = serializers.CharField(max_length=50)
    profit_center = serializers.CharField(max_length=50)
    covered_from = serializers.DateField()
    covered_to = serializers.DateField()
    date_requested = serializers.DateField()

    descriptions = serializers.CharField(max_length=50)
    quantity = serializers.IntegerField()
    uom = serializers.CharField(max_length=50)
    price = serializers.IntegerField()
    amount = serializers.IntegerField()

    encoded_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    reviewed_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None, allow_null=True)
    approved_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None, allow_null=True)
    release_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None, allow_null=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['encoded_by'] = user
        return RequestForm.objects.create(**validated_data)
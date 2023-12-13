from collections import OrderedDict


class PurchaseOrderStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    FieldStr = OrderedDict({
        PENDING: 'Pending',
        COMPLETED: 'Completed',
        CANCELED: 'Canceled'
    })

    @classmethod
    def choices(cls):
        return cls.FieldStr.items()

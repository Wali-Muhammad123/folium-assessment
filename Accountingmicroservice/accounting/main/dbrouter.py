class AccountingRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'warehouse' or model._meta.app_label == 'sales':
            return 'shared_db'
        return 'default'


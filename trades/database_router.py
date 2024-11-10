class StockRouter:
    """
    Routes database operations for the Stock model to SQLite
    and Watchlist, User, and all other models to MySQL.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'trades':
            if model.__name__ == 'Stock':
                return 'sqlite'  # Direct Stock reads to SQLite
            elif model.__name__ in ['Watchlist', 'User']:
                return 'default'  # Direct Watchlist and User reads to MySQL
        elif model._meta.app_label == 'contenttypes':
            return 'default'  # Ensure ContentType is read from MySQL
        return 'default'  # Default to MySQL for other models

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'trades':
            if model.__name__ == 'Stock':
                return 'sqlite'  # Direct Stock writes to SQLite
            elif model.__name__ in ['Watchlist', 'User']:
                return 'default'  # Direct Watchlist and User writes to MySQL
        elif model._meta.app_label == 'contenttypes':
            return 'default'  # Ensure ContentType is written to MySQL
        return 'default'  # Default to MySQL for other models

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between models within the 'trades' app,
        and allow relations involving ContentType.
        """
        if obj1._meta.app_label == 'trades' and obj2._meta.app_label == 'trades':
            return True
        # Allow relations with ContentType
        if obj1._meta.app_label == 'contenttypes' or obj2._meta.app_label == 'contenttypes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Direct migrations: Stock to SQLite, Watchlist and User to MySQL,
        ContentType to MySQL, and all other models to MySQL.
        """
        if app_label == 'trades':
            if model_name == 'stock':
                return db == 'sqlite'  # Migrate Stock to SQLite
            elif model_name in ['watchlist', 'user']:
                return db == 'default'  # Migrate Watchlist and User to MySQL
        elif app_label == 'contenttypes':
            return db == 'default'  # Migrate ContentType to MySQL
        return db == 'default'  # Migrate all other models to MySQL

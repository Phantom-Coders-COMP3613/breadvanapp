# blue prints are imported 
# explicitly instead of using *
from .user_views import user_views
from .index import index_views
from .auth import auth_views
from .driver_views import driver_views
from .resident_views import resident_views
from .common_views import common_views
from .driver_stock_views import driver_stock_views
from .admin import setup_admin


views = [user_views, index_views, auth_views, common_views, driver_views, resident_views, driver_stock_views]
# blueprints must be added to this list
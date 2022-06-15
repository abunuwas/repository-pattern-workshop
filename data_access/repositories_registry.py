class RepositoriesRegistry:
    def __init__(self, bookings_repository=None, restaurant_repository=None, user_repository=None, voucher_repository=None):
        self.bookings_repository = bookings_repository
        self.restaurant_repository = restaurant_repository
        self.user_repository = user_repository
        self.voucher_repo = voucher_repository

from authentication.models import CustomUser
from book.models import Book
from django.db import DataError, models


class Order(models.Model):
    """
    This class represents an Order. \n
    Attributes:
    -----------
    param book: foreign key Book
    type book: ForeignKey
    param user: foreign key CustomUser
    type user: ForeignKey
    param created_at: Describes the date when the order was created. Can't be changed.
    type created_at: int (timestamp)
    param end_at: Describes the actual return date of the book. (`None` if not returned)
    type end_at: int (timestamp)
    param planned_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
    type planned_end_at: int (timestamp)
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name="Returned on"
    )
    planned_end_at = models.DateTimeField(verbose_name="Planned return on")

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        if self.end_at == None:
            return (
                f" User: {self.user!s},"
                f" Book: {self.book!s},"
                f" Created at: '{self.created_at}',"
                f" Planned return on: '{self.planned_end_at}',"
                f" Actual return on: {self.end_at if self.end_at is not None else '-'}"
            )

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        """
        :return: order id, book id, user id, order created_at, order end_at, order planned_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8',
        |   'created_at': 1509393504,
        |   'end_at': 1509393504,
        |   'planned_end_at': 1509402866,
        | }
        """
        pass

    @staticmethod
    def create(user, book, planned_end_at):
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count <= 0:
            return None
        try:
            order = Order(user=user, book=book, planned_end_at=planned_end_at)
            order.save()
            book.count -= 1
            book.save()
            return order
        except ValueError:
            return None
        except DataError:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except:
            return None

    def update(self, planned_end_at=None, end_at=None):
        if planned_end_at != None:
            self.planned_end_at = planned_end_at
        if end_at != None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()

    @staticmethod
    def delete_by_id(order_id):
        try:
            a = Order.objects.get(pk=order_id)
        except:
            return False
        else:
            a.delete()
            return True

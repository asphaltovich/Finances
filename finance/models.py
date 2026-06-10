from django.db import models
class Client(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Email')
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    def __str__(self):
        return self.full_name
class Wallet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название кошелька')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='wallets',
        verbose_name='Клиент'
    )
    class Meta:
        verbose_name = 'Кошелёк клиента'
        verbose_name_plural = 'Кошельки клиентов'
    def __str__(self):
        return f"{self.name} ({self.client.username})"
class Expense(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Клиент'
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Кошелёк',
        null=True, blank=True
    )
    category = models.CharField(max_length=100, verbose_name='Категория расходов', default='Без категории')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма расходов')
    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
    def __str__(self):
        return f"Расход: {self.amount} руб. ({self.category}) - {self.client.username}"
class Income(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='incomes',
        verbose_name='Клиент'
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='incomes',
        verbose_name='Кошелёк',
        null=True, blank=True
    )
    category = models.CharField(max_length=100, verbose_name='Категория доходов', default='Без категории')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма доходов')
    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'
    def __str__(self):
        return f"Доход: {self.amount} руб. ({self.category}) - {self.client.username}"
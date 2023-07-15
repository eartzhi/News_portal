from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех статей и новостей по выбранным категориям'
    missing_args_message = 'Введите категорию'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполняется при вызове вашей команды
        # self.stdout.write(str(options['argument']))
        self.stdout.write('Вы действительно хотите удалить новости '
                          'и заметки по выбранным категориям? yes/no')
        answer = input()
        if answer == 'yes':
            categories = options['argument']
            for c in categories:
                posts = Post.objects.filter(
                    category=Category.objects.filter(category=c).first()
                                           ).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Статьи и заметки удалены'))


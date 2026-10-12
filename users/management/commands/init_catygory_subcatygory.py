from django.core.management.base import BaseCommand
from category.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Initialize categories and subcategories'

    def handle(self, *args, **kwargs):
        categories_data = {
            'Informatique': {
                'description': 'Produits informatiques, ordinateurs, accessoires',
                'subcategories': [
                    'Ordinateurs portables',
                    'Ordinateurs de bureau',
                    'Composants PC',
                    'Périphériques',
                    'Stockage et sauvegarde',
                    'Réseau et connectivité',
                    'Logiciels',
                    'Accessoires informatiques'
                ]
            },

            # ضع باقي categories_data هنا كما هي عندك
        }

        self.stdout.write('Starting category and subcategory initialization...')

        SubCategory.objects.all().delete()
        Category.objects.all().delete()

        created_categories = 0
        created_subcategories = 0

        for category_name, category_data in categories_data.items():
            category, cat_created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': category_data['description']}
            )

            if cat_created:
                created_categories += 1
                self.stdout.write(
                    f'Category created: {category_name}'
                )

            for subcategory_name in category_data['subcategories']:
                subcategory, sub_created = SubCategory.objects.update_or_create(
                    name=subcategory_name,
                    defaults={'category': category}
                )

                if sub_created:
                    created_subcategories += 1
                    self.stdout.write(
                        f'  Subcategory created: {subcategory_name} under {category_name}'
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nInitialization complete: {created_categories} categories '
                f'and {created_subcategories} subcategories created.'
            )
        )

        self.stdout.write('\nSummary by category:')

        for category in Category.objects.all():
            subcat_count = SubCategory.objects.filter(
                category=category
            ).count()

            self.stdout.write(
                f'  {category.name}: {subcat_count} subcategories'
            )
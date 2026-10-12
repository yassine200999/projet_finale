from django.core.management.base import BaseCommand
from category.models import Category, SubCategory


class Command(BaseCommand):
    help = "Create or update the default product categories and subcategories."

    categories_data = {
        "Informatique": {
            "description": "Produits informatiques, ordinateurs et accessoires",
            "subcategories": [
                "Ordinateurs portables", "Ordinateurs de bureau",
                "Composants informatiques", "Périphériques",
                "Accessoires informatiques", "Réseaux",
                "Stockage", "Imprimantes et scanners",
                "Écrans", "Logiciels",
            ],
        },
        "Sport": {
            "description": "Équipements et accessoires de sport",
            "subcategories": [
                "Football", "Basketball", "Tennis", "Fitness",
                "Musculation", "Course à pied", "Cyclisme",
                "Natation", "Sports de combat", "Sports collectifs",
            ],
        },
        "Décoration": {
            "description": "Articles de décoration intérieure et extérieure",
            "subcategories": [
                "Décoration murale", "Vases", "Cadres", "Luminaires",
                "Bougies", "Tapis", "Rideaux", "Miroirs",
                "Objets décoratifs", "Décoration saisonnière",
            ],
        },
        "Maison": {
            "description": "Articles et équipements pour la maison",
            "subcategories": [
                "Cuisine", "Rangement", "Literie", "Salle de bain",
                "Meubles", "Éclairage", "Nettoyage", "Linge de maison",
                "Ustensiles", "Organisation",
            ],
        },
        "Véhicules": {
            "description": "Véhicules, pièces et accessoires automobiles",
            "subcategories": [
                "Pièces automobiles", "Accessoires auto", "Motos",
                "Vélos", "Entretien automobile", "Éclairage automobile",
                "Pneus", "Équipements de sécurité", "Audio auto",
                "Accessoires moto",
            ],
        },
        "Vêtements": {
            "description": "Vêtements et accessoires vestimentaires",
            "subcategories": [
                "Vêtements homme", "Vêtements femme", "Vêtements enfant",
                "T-shirts", "Pantalons", "Vestes", "Manteaux",
                "Vêtements de sport", "Sous-vêtements", "Accessoires",
            ],
        },
        "Biscuiterie": {
            "description": "Biscuits, confiseries et produits de biscuiterie",
            "subcategories": [
                "Biscuits sucrés", "Biscuits salés", "Gaufrettes",
                "Cookies", "Crackers", "Gâteaux secs", "Madeleines",
                "Biscuits fourrés", "Biscuits sans gluten", "Assortiments",
            ],
        },
        "Électronique": {
            "description": "Appareils électroniques et accessoires",
            "subcategories": [
                "Téléphones", "Tablettes", "Téléviseurs", "Audio",
                "Appareils photo", "Chargeurs", "Câbles",
                "Accessoires mobiles", "Objets connectés", "Batteries",
            ],
        },
        "Beauté": {
            "description": "Produits de beauté et accessoires de soin",
            "subcategories": [
                "Soins du visage", "Soins du corps", "Maquillage",
                "Parfums", "Soins des cheveux", "Manucure",
                "Rasage", "Accessoires beauté", "Hygiène", "Protection solaire",
            ],
        },
        "Jardinage": {
            "description": "Outils et accessoires de jardinage",
            "subcategories": [
                "Outils de jardin", "Arrosage", "Pots et jardinières",
                "Graines", "Terreau", "Engrais", "Tondeuses",
                "Équipement extérieur", "Éclairage de jardin", "Protection",
            ],
        },
        "Livres": {
            "description": "Livres, ouvrages et supports de lecture",
            "subcategories": [
                "Romans", "Littérature", "Scolaire", "Informatique",
                "Sciences", "Histoire", "Langues", "Bandes dessinées",
                "Jeunesse", "Développement personnel",
            ],
        },
        "Jouets": {
            "description": "Jouets, jeux et activités pour enfants",
            "subcategories": [
                "Jeux de construction", "Jeux éducatifs", "Poupées",
                "Véhicules jouets", "Jeux de société", "Peluches",
                "Jeux créatifs", "Jeux d'extérieur", "Puzzles",
                "Jouets électroniques",
            ],
        },
        "Santé": {
            "description": "Articles de bien-être et de santé non réglementés",
            "subcategories": [
                "Premiers secours", "Hygiène", "Thermomètres",
                "Aides à la mobilité", "Soins à domicile", "Protection",
                "Bien-être", "Accessoires médicaux", "Orthopédie",
                "Rangement médical",
            ],
        },
        "Animaux": {
            "description": "Produits et accessoires pour animaux",
            "subcategories": [
                "Chiens", "Chats", "Oiseaux", "Poissons",
                "Rongeurs", "Alimentation animale", "Jouets pour animaux",
                "Litière", "Transport", "Toilettage",
            ],
        },
        "Bricolage": {
            "description": "Outils, matériaux et accessoires de bricolage",
            "subcategories": [
                "Outils à main", "Outils électriques", "Visserie",
                "Peinture", "Plomberie", "Électricité", "Quincaillerie",
                "Sécurité", "Mesure", "Adhésifs",
            ],
        },
        "Musique": {
            "description": "Instruments de musique et accessoires",
            "subcategories": [
                "Guitares", "Claviers", "Percussions", "Instruments à vent",
                "Instruments à cordes", "Audio professionnel",
                "Accessoires instrument", "Partitions", "Microphones",
                "Casques audio",
            ],
        },
        "Bureau": {
            "description": "Fournitures et équipements de bureau",
            "subcategories": [
                "Papeterie", "Stylos", "Cahiers", "Classement",
                "Mobilier de bureau", "Impression", "Agrafeuses",
                "Calculatrices", "Accessoires de bureau", "Organisation",
            ],
        },
        "Bagages": {
            "description": "Bagages et accessoires de voyage",
            "subcategories": [
                "Valises", "Sacs de voyage", "Sacs à dos",
                "Trousses", "Étiquettes de bagages", "Organisateurs",
                "Bagages cabine", "Housses", "Accessoires de voyage",
                "Sacs professionnels",
            ],
        },
        "Montres": {
            "description": "Montres et accessoires horlogers",
            "subcategories": [
                "Montres homme", "Montres femme", "Montres enfant",
                "Montres sport", "Montres connectées", "Bracelets",
                "Boîtes à montres", "Réveils", "Accessoires horlogers",
                "Montres classiques",
            ],
        },
        "Photographie": {
            "description": "Appareils photo et équipements photographiques",
            "subcategories": [
                "Appareils photo", "Objectifs", "Trépieds", "Éclairage",
                "Sacs photo", "Cartes mémoire", "Filtres",
                "Accessoires vidéo", "Imprimantes photo", "Nettoyage optique",
            ],
        },
    }

    def handle(self, *args, **options):
        created_categories = 0
        updated_categories = 0
        created_subcategories = 0
        updated_subcategories = 0

        for category_name, details in self.categories_data.items():
            category, created = Category.objects.update_or_create(
                name=category_name,
                defaults={"description": details["description"]},
            )
            if created:
                created_categories += 1
            else:
                updated_categories += 1

            for subcategory_name in details["subcategories"]:
                _, subcategory_created = SubCategory.objects.update_or_create(
                    name=subcategory_name,
                    defaults={"category": category},
                )
                if subcategory_created:
                    created_subcategories += 1
                else:
                    updated_subcategories += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Initialization completed. "
                f"Categories: {created_categories} created, "
                f"{updated_categories} updated. "
                f"Subcategories: {created_subcategories} created, "
                f"{updated_subcategories} updated."
            )
        )

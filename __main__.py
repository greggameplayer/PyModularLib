from PyModularLib.FilterChain import FilterChain
from PyModularLib.Filters import WordWrapFilter, BoxFilter, EmailFilter
from PyModularLib.FancyTable import FancyTable


# Structure de condition : {'condition': 'length >=/<=/==/!=/>/< votrenb', 'valid': [vos filtres quand c'est true], 'invalid': [vos filtres quand c'est false]}
# Structure de groupe : {'group': 'le nom de votre groupe'} à déclarer dans le deuxième argument de la fonction FilterChain comme ci-dessous

# FilterChain( Tableau des filtres ou modules ( group, condition ), Dictionnaire des groupes )

mainChain = FilterChain(
    [{'condition': 'length >= 100', 'valid': [{'group': 'Basic mail'}], 'invalid': [BoxFilter(FancyTable.CBLUE)]}],
    {'Basic mail': [WordWrapFilter(20), BoxFilter(FancyTable.CRED), EmailFilter('gregoire.hage@gmail.com',
                                                                                   'greggameplayer@hotmail.fr',
                                                                                   'Salut')]})
print(mainChain.execute("gg"))

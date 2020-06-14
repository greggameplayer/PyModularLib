from PyModularLib.FilterChain import FilterChain
from PyModularLib.Filters import WordWrapFilter, BoxFilter, EmailFilter

mainChain = FilterChain([{'group': 'Basic mail'}],
                        {'Basic mail': [WordWrapFilter(20), BoxFilter(), EmailFilter('gregoire.hage@gmail.com',
                                                                                     'greggameplayer@hotmail.fr',
                                                                                     'Salut')]})
print(mainChain.execute("bonjour à tous comment ça va les petits loustics"))
